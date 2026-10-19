"""직접 학습하는 점자 역점역 Transformer: `python train.py --help`부터 시작하세요.

예시 (명령을 실행해야만 학습합니다. 파일을 열거나 import만 해서는 학습하지 않습니다):
  python train.py --device cuda --epochs 16 --batch-size 16 --grad-accum 2
  python train.py --resume checkpoints/날짜/training_state.pt

한 epoch는 사용하기로 정한 train 문장을 한 번씩 보는 것입니다. batch16은 한 번에
16문장을 계산한다는 뜻이고, grad-accum2는 두 batch의 기울기를 모아 한 번 갱신하는
뜻입니다. 마지막에 batch가 하나만 남아도 버리지 않고 정확한 토큰 수로 나눕니다.

교차 엔트로피: L = -Σ log p(정답 다음 토큰 | 점자, 이전 정답 토큰) / 정답 토큰 수.
gradient(기울기)는 각 가중치를 조금 움직일 때 L이 얼마나 변하는지를 말합니다.
backward()가 연쇄법칙으로 기울기를 계산하고 AdamW optimizer.step()이 숫자를
수정합니다. learning rate는 이 수정의 크기를 조절합니다. 너무 크면 불안정하고
너무 작으면 학습이 느립니다. 실제 최적 값은 검증 데이터로 비교해야 합니다.

validation loss도 이전 정답을 주는 teacher forcing으로 계산합니다. 낮은 loss가
항상 가장 낮은 실제 번역 CER를 보장하지 않습니다. `evaluate.py`는 정답을 주지
않는 실제 생성으로 시험합니다. test는 모델 선택에 반복 사용하지 않는 것이 좋습니다.

AMP는 CUDA 일부 계산을 float16으로 수행해 속도/메모리를 줄입니다. 가중치는
float32로 유지합니다. GradScaler는 작은 기울기 소실을 줄이고 비정상 값이 생긴
업데이트를 건너뜁니다. CPU 학습은 float32이며 AMP를 켜지 않습니다.

resume는 마지막 '완료된 epoch'부터 이어갑니다. optimizer의 모멘텀, scheduler,
AMP scaler, Python/torch RNG까지 복원합니다. --init-checkpoint는 모델 숫자만
가져와 새 optimizer/일정/실험으로 시작하는 별개의 기능입니다. 두 기능을 구분하세요.
같은 seed라도 다른 GPU, 라이브러리 버전, 비결정적 CUDA 연산 때문에 모든 환경에서
비트 단위 동일 결과를 보장하지는 않습니다. --deterministic은 재현 제약을 강화합니다.

공식 문서: https://docs.pytorch.org/docs/stable/notes/amp_examples.html
https://docs.pytorch.org/docs/stable/notes/randomness.html
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import time
from contextlib import nullcontext
from datetime import datetime
from pathlib import Path

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader, Sampler

from model import (PAD, BrailleTransformer, ModelConfig, PairDataset, Vocabulary,
                   collate_pairs, read_jsonl, sha256_file)

PROJECT = Path(__file__).resolve().parent


def write_json(path: Path, value: dict | list) -> None:
    """쓰기 도중 종료되면 이전 파일을 유지하도록 임시 파일을 완성한 뒤 교체합니다."""
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    os.replace(temporary, path)


def atomic_torch_save(value: object, path: Path) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    torch.save(value, temporary)
    os.replace(temporary, path)


class LengthBucketSampler(Sampler[list[int]]):
    """비슷한 길이를 묶어 PAD 계산을 줄이되 epoch마다 새 순서로 학습합니다.

    1. seed+epoch로 문장 index를 섞습니다.
    2. 작은 pool 안에서 길이순으로 정렬하고 batch를 만듭니다.
    3. batch 순서도 다시 섞습니다. 한 epoch에서 모든 문장을 한 번씩 씁니다.
    전역 random 상태와 별도의 Random 객체를 써서 dropout RNG와 섞이지 않습니다.
    마지막 작은 batch를 drop하지 않습니다. validation에는 무작위 섞기를 끕니다.
    """
    def __init__(self, dataset: PairDataset, batch_size: int, seed: int, shuffle: bool):
        self.lengths = [max(len(x["source"]), len(x["target"])) for x in dataset.items]
        self.batch_size, self.seed, self.shuffle, self.epoch = batch_size, seed, shuffle, 0

    def set_epoch(self, epoch: int) -> None:
        self.epoch = epoch

    def __len__(self) -> int:
        return math.ceil(len(self.lengths) / self.batch_size)

    def __iter__(self):
        indices = list(range(len(self.lengths)))
        rng = random.Random(self.seed + self.epoch)
        if self.shuffle:
            rng.shuffle(indices)
        pool_size = self.batch_size * 50 if self.shuffle else len(indices)
        batches = []
        for start in range(0, len(indices), pool_size):
            pool = sorted(indices[start:start + pool_size], key=lambda index: self.lengths[index])
            batches.extend(pool[i:i + self.batch_size] for i in range(0, len(pool), self.batch_size))
        if self.shuffle:
            rng.shuffle(batches)
        yield from batches


def batch_windows(loader: DataLoader, accumulation: int):
    """일단 CPU batch들을 accumulation개 모읍니다. GPU graph를 저장하지 않습니다.

    batch마다 길이가 다르므로 평균 loss를 무조건 accumulation으로 나누면 토큰마다
    가중치가 달라집니다. 미리 이 묶음의 유효한 정답 토큰 수를 센 뒤 모든 loss sum을
    그 같은 수로 나누면, 하나의 큰 batch에서 평균을 낸 것과 같은 가중치가 됩니다.
    dropout/부동소수점 반올림 때문에 실제 계산값이 큰 batch와 완전히 같지는 않습니다.
    """
    group = []
    for batch in loader:
        group.append(batch)
        if len(group) == accumulation:
            yield group
            group = []
    if group:
        yield group


def autocast_context(device: torch.device, use_amp: bool):
    return torch.autocast(device_type="cuda", dtype=torch.float16) if use_amp else nullcontext()


@torch.inference_mode()
def validation_loss(model: BrailleTransformer, loader: DataLoader,
                    device: torch.device, use_amp: bool) -> tuple[float, int]:
    model.eval()  # dropout를 끕니다. 학습 때는 train()으로 다시 켭니다.
    total_loss, total_tokens = 0.0, 0
    for batch in loader:
        source = batch["source"].to(device, non_blocking=True)
        target = batch["target"].to(device, non_blocking=True)
        # 입력: BOS, 정답1, 정답2 ... / label: 정답1, 정답2 ... EOS
        labels = target[:, 1:]
        with autocast_context(device, use_amp):
            logits = model(source, target[:, :-1])
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                labels.reshape(-1), ignore_index=PAD, reduction="sum")
        loss_value = float(loss)
        if not math.isfinite(loss_value):
            raise FloatingPointError("검증 loss가 NaN/Inf입니다. 학습률 또는 AMP 설정을 확인하세요.")
        total_loss += loss_value
        total_tokens += int(labels.ne(PAD).sum())
    return total_loss / total_tokens, total_tokens


def save_history(run_dir: Path, history: list[dict]) -> None:
    write_json(run_dir / "history.json", history)
    if history:
        with (run_dir / "history.csv").open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(history[0]))
            writer.writeheader()
            writer.writerows(history)


def rng_state(device: torch.device) -> dict:
    return {"python": random.getstate(), "torch_cpu": torch.get_rng_state(),
        "torch_cuda": torch.cuda.get_rng_state_all() if device.type == "cuda" else None}


def restore_rng(state: dict, device: torch.device) -> None:
    random.setstate(state["python"])
    torch.set_rng_state(state["torch_cpu"].cpu())
    if device.type == "cuda" and state["torch_cuda"] is not None:
        torch.cuda.set_rng_state_all([x.cpu() for x in state["torch_cuda"]])


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--data-dir", type=Path, default=PROJECT / "data" / "processed")
    p.add_argument("--run-dir", type=Path, help="새 폴더. 생략하면 checkpoints/시간을 만듭니다.")
    p.add_argument("--resume", type=Path, help="완료된 epoch의 training_state.pt. 같은 실험 폴더에서 재개")
    p.add_argument("--init-checkpoint", type=Path, help="config/vocab/best.pt 폴더. optimizer는 새로 시작")
    p.add_argument("--epochs", type=int, default=16, help="scheduler 전체 일정; resume 때 바꾸지 마세요")
    p.add_argument("--stop-after-epochs", type=int, default=0, help="이번 호출에서 완료할 epoch 수; 0=끝까지")
    p.add_argument("--batch-size", type=int, default=16)
    p.add_argument("--grad-accum", type=int, default=2)
    p.add_argument("--learning-rate", type=float, default=5e-4)
    p.add_argument("--weight-decay", type=float, default=0.01)
    p.add_argument("--warmup-ratio", type=float, default=0.05)
    p.add_argument("--clip-grad", type=float, default=1.0)
    p.add_argument("--patience", type=int, default=4)
    p.add_argument("--min-delta", type=float, default=0.0)
    p.add_argument("--d-model", type=int, default=256)
    p.add_argument("--encoder-layers", type=int, default=3)
    p.add_argument("--decoder-layers", type=int, default=3)
    p.add_argument("--heads", type=int, default=8)
    p.add_argument("--ffn-dim", type=int, default=1024)
    p.add_argument("--dropout", type=float, default=0.1)
    p.add_argument("--max-source-length", type=int, default=560, help="BOS/EOS 포함; 자르지 않음")
    p.add_argument("--max-target-length", type=int, default=560, help="NFD 자모 및 BOS/EOS 포함")
    p.add_argument("--length-policy", choices=["error", "filter"], default="error")
    p.add_argument("--train-samples", type=int, default=0, help="smoke용 앞 N행; 0=전체")
    p.add_argument("--validation-samples", type=int, default=0, help="smoke용 앞 N행; 0=전체")
    p.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    p.add_argument("--no-amp", action="store_true")
    p.add_argument("--seed", type=int, default=20261006)
    p.add_argument("--cpu-threads", type=int, default=4)
    p.add_argument("--deterministic", action="store_true")
    p.add_argument("--log-every", type=int, default=20, help="optimizer window 단위 진행 출력")
    return p


def main() -> None:
    args = parser().parse_args()
    if args.resume and args.init_checkpoint:
        raise ValueError("--resume와 --init-checkpoint는 동시에 사용할 수 없습니다.")
    for name in ("epochs", "batch_size", "grad_accum", "patience", "cpu_threads", "log_every"):
        if getattr(args, name) < 1:
            raise ValueError(f"{name}은 1 이상이어야 합니다.")
    if args.learning_rate <= 0 or not 0 <= args.warmup_ratio < 1:
        raise ValueError("learning-rate>0, 0<=warmup-ratio<1이어야 합니다.")
    if args.train_samples < 0 or args.validation_samples < 0 or args.stop_after_epochs < 0:
        raise ValueError("sample 수와 stop-after-epochs는 음수일 수 없습니다.")
    torch.set_num_threads(args.cpu_threads)
    # nn.Transformer fused eval fastpath를 끄면 학습/검증의 AMP dtype 경로가 같습니다.
    # attention 내부의 PyTorch SDPA는 계속 사용 가능합니다.
    torch.backends.mha.set_fastpath_enabled(False)
    requested_device = args.device
    device = torch.device("cuda" if args.device == "auto" and torch.cuda.is_available()
        else "cpu" if args.device == "auto" else args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA를 요청했지만 사용할 수 없습니다. CPU로 몰래 바꾸지 않습니다.")
    use_amp = device.type == "cuda" and not args.no_amp
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(args.seed)
    if args.deterministic:
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")
        torch.use_deterministic_algorithms(True)
    torch.backends.cudnn.benchmark = False

    data_dir = args.data_dir.resolve()
    train_path, validation_path = data_dir / "train.jsonl", data_dir / "validation.jsonl"
    # test는 여기서 읽지도 않습니다. 최종 평가 때 evaluate.py에서만 읽습니다.
    train_rows, validation_rows = read_jsonl(train_path), read_jsonl(validation_path)
    full_train_rows = train_rows
    if args.train_samples:
        train_rows = train_rows[:args.train_samples]
    if args.validation_samples:
        validation_rows = validation_rows[:args.validation_samples]
    resume_state = None
    if args.resume:
        state_path = args.resume.resolve()
        run_dir = state_path.parent
        if args.run_dir and args.run_dir.resolve() != run_dir:
            raise ValueError("resume는 원래 실험 폴더에서 실행합니다. 새 실험은 --init-checkpoint를 쓰세요.")
        resume_state = torch.load(state_path, map_location="cpu", weights_only=True)
        saved_config = json.loads((run_dir / "config.json").read_text(encoding="utf-8"))
        vocab = Vocabulary.load(run_dir / "vocab.json")
    else:
        run_dir = (args.run_dir or PROJECT / "checkpoints" / datetime.now().strftime("%Y%m%d_%H%M%S_%f")).resolve()
        if run_dir.exists() and any(run_dir.iterdir()):
            raise FileExistsError(f"새 실험 폴더가 비어 있지 않습니다: {run_dir}")
        run_dir.mkdir(parents=True, exist_ok=True)
        if args.init_checkpoint:
            # 같은 문자 개수라도 ID 순서가 바뀌면 기존 가중치의 의미가 달라집니다.
            # 초기화 학습도 추론과 마찬가지로 원래 학습 사전의 내용 hash를 확인합니다.
            initial_config = json.loads((args.init_checkpoint / "config.json").read_text(encoding="utf-8"))
            expected_vocab_hash = initial_config.get("data", {}).get("vocab_sha256")
            if not expected_vocab_hash or sha256_file(args.init_checkpoint / "vocab.json") != expected_vocab_hash:
                raise ValueError("init-checkpoint의 vocab.json이 학습 당시와 다릅니다. "
                    "문자 개수가 같아도 ID 순서가 바뀐 어휘로 기존 가중치를 초기화할 수 없습니다.")
            vocab = Vocabulary.load(args.init_checkpoint / "vocab.json")
        else:
            # smoke subset을 요청해도 학습 split 전체의 문자 사전만 사용합니다.
            # 검증/시험의 문자는 어떤 경우에도 사전 구성에 쓰지 않습니다.
            vocab = Vocabulary.from_training_rows(full_train_rows)
        vocab.save(run_dir / "vocab.json")

    model_config = ModelConfig(len(vocab.source_tokens), len(vocab.target_tokens),
        args.d_model, args.heads, args.encoder_layers, args.decoder_layers, args.ffn_dim,
        args.dropout, args.max_source_length, args.max_target_length)
    if args.init_checkpoint:
        original = json.loads((args.init_checkpoint / "config.json").read_text(encoding="utf-8"))["model"]
        if original != model_config.to_dict():
            raise ValueError("init-checkpoint의 architecture/vocab/길이 설정과 CLI 설정이 달라집니다.")
    train_data = PairDataset(train_rows, vocab, args.max_source_length, args.max_target_length, args.length_policy)
    validation_data = PairDataset(validation_rows, vocab, args.max_source_length, args.max_target_length, args.length_policy)
    train_sampler = LengthBucketSampler(train_data, args.batch_size, args.seed, True)
    validation_sampler = LengthBucketSampler(validation_data, args.batch_size, args.seed, False)
    train_loader = DataLoader(train_data, batch_sampler=train_sampler, collate_fn=collate_pairs,
        num_workers=0, pin_memory=device.type == "cuda")
    validation_loader = DataLoader(validation_data, batch_sampler=validation_sampler, collate_fn=collate_pairs,
        num_workers=0, pin_memory=device.type == "cuda")
    updates_per_epoch = math.ceil(len(train_loader) / args.grad_accum)
    total_updates = updates_per_epoch * args.epochs
    warmup_updates = int(total_updates * args.warmup_ratio)
    training_config = {name: getattr(args, name) for name in (
        "epochs", "batch_size", "grad_accum", "learning_rate", "weight_decay", "warmup_ratio",
        "clip_grad", "patience", "min_delta", "seed", "deterministic", "length_policy",
        "train_samples", "validation_samples", "cpu_threads")}
    training_config.update({"device": str(device), "amp": use_amp,
        "updates_per_epoch": updates_per_epoch, "total_updates": total_updates,
        "warmup_updates": warmup_updates, "sampler": "shuffled_length_pools_v1"})
    data_config = {"directory": str(data_dir), "train_sha256": sha256_file(train_path),
        "validation_sha256": sha256_file(validation_path), "vocab_sha256": sha256_file(run_dir / "vocab.json"),
        "vocab_source": "full train split only", "train": train_data.stats, "validation": validation_data.stats}
    config = {"format_version": 1, "task": "unicode_6dot_braille_to_korean_nfd",
        "model": model_config.to_dict(), "training": training_config, "data": data_config,
        "environment": {"torch": str(torch.__version__), "cuda_runtime": torch.version.cuda,
            "requested_device": requested_device, "device": str(device),
            "gpu": torch.cuda.get_device_name(device) if device.type == "cuda" else None},
        "initial_checkpoint": str(args.init_checkpoint.resolve()) if args.init_checkpoint else None}
    if resume_state:
        # 설정이 달라지면 scheduler/RNG 재개의 의미가 달라지므로 명시적으로 거절합니다.
        for key in ("model", "training", "data"):
            if saved_config[key] != config[key]:
                raise ValueError(f"resume 설정이 저장 당시와 다릅니다: {key}. 원래 CLI 설정을 지정하세요.")
        if saved_config["environment"]["torch"] != str(torch.__version__):
            raise ValueError("엄격한 resume에는 저장 당시와 같은 torch 버전이 필요합니다.")
        for filename, hash_key in (("last.pt", "last_sha256"), ("best.pt", "best_sha256")):
            if sha256_file(run_dir / filename) != resume_state[hash_key]:
                raise ValueError(f"{filename}이 training_state 저장 당시와 달라졌습니다.")
    else:
        write_json(run_dir / "config.json", config)
    write_json(run_dir / "data_stats.json", data_config)

    model = BrailleTransformer(model_config).to(device)
    if args.init_checkpoint:
        model.load_state_dict(torch.load(args.init_checkpoint / "best.pt", map_location="cpu", weights_only=True))
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate,
        betas=(0.9, 0.98), weight_decay=args.weight_decay)

    def lr_factor(step: int) -> float:
        if warmup_updates and step < warmup_updates:
            return (step + 1) / warmup_updates
        progress = min(1.0, max(0.0, (step - warmup_updates) / max(1, total_updates - warmup_updates)))
        return 0.1 + 0.9 * 0.5 * (1.0 + math.cos(math.pi * progress))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_factor)
    scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
    history, best_loss, best_epoch, bad_epochs, completed_epoch, global_update = [], math.inf, 0, 0, 0, 0
    if resume_state:
        model.load_state_dict(torch.load(run_dir / "last.pt", map_location="cpu", weights_only=True))
        optimizer.load_state_dict(resume_state["optimizer"])
        scheduler.load_state_dict(resume_state["scheduler"])
        scaler.load_state_dict(resume_state["scaler"])
        history = resume_state["history"]
        best_loss, best_epoch = resume_state["best_loss"], resume_state["best_epoch"]
        bad_epochs, completed_epoch = resume_state["bad_epochs"], resume_state["completed_epoch"]
        global_update = resume_state["global_update"]
        restore_rng(resume_state["rng"], device)
    parameter_count = sum(p.numel() for p in model.parameters())
    print(json.dumps({"event": "ready", "run_dir": str(run_dir), "parameters": parameter_count,
        "train_examples": len(train_data), "validation_examples": len(validation_data),
        "source_vocab": len(vocab.source_tokens), "target_vocab": len(vocab.target_tokens),
        "device": str(device), "model_parameter_device": str(next(model.parameters()).device),
        "amp": use_amp, "resume_completed_epoch": completed_epoch,
        "gpu": config["environment"]["gpu"]}, ensure_ascii=False), flush=True)
    started_call = time.perf_counter()
    call_epochs = 0
    if bad_epochs >= args.patience:
        print("이 실험은 이미 early stopping으로 종료됐습니다. 새 학습은 --init-checkpoint를 쓰세요.", flush=True)
        return

    for epoch in range(completed_epoch + 1, args.epochs + 1):
        epoch_start = time.perf_counter()
        train_sampler.set_epoch(epoch)
        model.train()
        if device.type == "cuda":
            torch.cuda.reset_peak_memory_stats(device)
        loss_sum, token_count, skipped_updates, windows_done = 0.0, 0, 0, 0
        for group in batch_windows(train_loader, args.grad_accum):
            # labels는 target[:,1:]입니다. BOS를 빼고 EOS를 포함한 유효 토큰을 셉니다.
            group_tokens = sum(int(batch["target"][:, 1:].ne(PAD).sum()) for batch in group)
            optimizer.zero_grad(set_to_none=True)
            for batch in group:
                source = batch["source"].to(device, non_blocking=True)
                target = batch["target"].to(device, non_blocking=True)
                labels = target[:, 1:]
                with autocast_context(device, use_amp):
                    logits = model(source, target[:, :-1])
                    batch_loss_sum = F.cross_entropy(logits.reshape(-1, logits.size(-1)),
                        labels.reshape(-1), ignore_index=PAD, reduction="sum")
                    normalized_loss = batch_loss_sum / group_tokens
                # graph는 이 microbatch의 backward에서 해제됩니다. retain_graph는 불필요합니다.
                scaler.scale(normalized_loss).backward()
                value = float(batch_loss_sum.detach())
                if not math.isfinite(value):
                    raise FloatingPointError("학습 loss가 NaN/Inf입니다. 학습률/입력/AMP를 확인하세요.")
                loss_sum += value
                token_count += int(labels.ne(PAD).sum())
            # clipping 전에 unscale하지 않으면 확대된 gradient를 잘못 잘라 버립니다.
            scaler.unscale_(optimizer)
            grad_norm = float(nn.utils.clip_grad_norm_(model.parameters(), args.clip_grad))
            old_scale = scaler.get_scale()
            scaler.step(optimizer)
            scaler.update()
            if scaler.get_scale() < old_scale:
                skipped_updates += 1
            else:
                scheduler.step()
                global_update += 1
            windows_done += 1
            if windows_done % args.log_every == 0 or windows_done == updates_per_epoch:
                elapsed = time.perf_counter() - epoch_start
                print(json.dumps({"event": "progress", "epoch": epoch,
                    "window": windows_done, "windows": updates_per_epoch,
                    "train_loss": loss_sum / token_count, "lr": optimizer.param_groups[0]["lr"],
                    "seconds": round(elapsed, 2), "epoch_eta_seconds": round(elapsed / windows_done *
                        (updates_per_epoch - windows_done), 2), "grad_norm": grad_norm,
                    "skipped_updates": skipped_updates}, ensure_ascii=False), flush=True)
        train_seconds = time.perf_counter() - epoch_start
        validation_start = time.perf_counter()
        val_loss, val_tokens = validation_loss(model, validation_loader, device, use_amp)
        validation_seconds = time.perf_counter() - validation_start
        improved = val_loss < best_loss - args.min_delta
        if improved:
            best_loss, best_epoch, bad_epochs = val_loss, epoch, 0
        else:
            bad_epochs += 1
        record = {"epoch": epoch, "train_loss": loss_sum / token_count,
            "validation_loss": val_loss, "train_tokens": token_count,
            "validation_tokens": val_tokens, "learning_rate": optimizer.param_groups[0]["lr"],
            "global_updates": global_update, "skipped_updates": skipped_updates,
            "train_seconds": train_seconds, "validation_seconds": validation_seconds,
            "epoch_seconds": time.perf_counter() - epoch_start, "best_epoch": best_epoch,
            "best_validation_loss": best_loss, "is_best": improved,
            "gpu_peak_allocated_mib": torch.cuda.max_memory_allocated(device) / 2**20 if device.type == "cuda" else 0.0}
        history.append(record)
        # CPU Tensor로 저장하면 CUDA가 없는 PC도 map_location='cpu'로 읽을 수 있습니다.
        # state_dict에는 학습된 숫자만 있습니다. 앱에는 optimizer를 넣을 필요가 없습니다.
        weights = {key: tensor.detach().cpu() for key, tensor in model.state_dict().items()}
        atomic_torch_save(weights, run_dir / "last.pt")
        if improved:
            atomic_torch_save(weights, run_dir / "best.pt")
        last_hash, best_hash = sha256_file(run_dir / "last.pt"), sha256_file(run_dir / "best.pt")
        state = {"format_version": 1, "completed_epoch": epoch,
            "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(),
            "scaler": scaler.state_dict(), "rng": rng_state(device), "history": history,
            "best_loss": best_loss, "best_epoch": best_epoch, "bad_epochs": bad_epochs,
            "global_update": global_update, "last_sha256": last_hash, "best_sha256": best_hash}
        atomic_torch_save(state, run_dir / "training_state.pt")
        save_history(run_dir, history)
        write_json(run_dir / "summary.json", {"run_dir": str(run_dir), "parameters": parameter_count,
            "completed_epochs": epoch, "best_epoch": best_epoch, "best_validation_loss": best_loss,
            "best_sha256": best_hash, "last_sha256": last_hash, "device": str(device),
            "training_config": training_config, "data": data_config,
            "call_seconds": time.perf_counter() - started_call,
            "early_stopped": bad_epochs >= args.patience,
            "warning": "validation loss is teacher-forced, not autoregressive test quality"})
        print(json.dumps({"event": "epoch_complete", **record,
            "best_checkpoint": str(run_dir / "best.pt")}, ensure_ascii=False), flush=True)
        call_epochs += 1
        if bad_epochs >= args.patience:
            print(f"EARLY_STOP: {args.patience} epoch 동안 검증 loss 개선 없음. best epoch={best_epoch}", flush=True)
            break
        if args.stop_after_epochs and call_epochs >= args.stop_after_epochs:
            print("STOP_AFTER_EPOCHS: 완료된 epoch 상태 저장. 같은 설정으로 --resume 가능.", flush=True)
            break
    print(json.dumps({"event": "finished", "run_dir": str(run_dir), "best_epoch": best_epoch,
        "best_validation_loss": best_loss if math.isfinite(best_loss) else None,
        "seconds": time.perf_counter() - started_call}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
