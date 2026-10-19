"""M2M100 + LoRA: final grouped-split training loop, with a portable CLI.

Importing this module does not read data, load a model or start training.
The first model download is a separate explicit step (fetch_model.py).
"""
from pathlib import Path
import argparse
import json
import os

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/train.json")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data/processed/tatoeba_en_ko_grouped_v1")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--init-adapter", type=Path, help="Weights only; optimizer/scheduler restart")
    args = parser.parse_args()
    CONFIG = json.loads(args.config.read_text(encoding="utf-8"))
    DATA_DIR = args.data_dir.expanduser().resolve()
    RESUME_ADAPTER = args.init_adapter
    for name in ("train.tsv", "validation.tsv", "test.tsv", "split_manifest.json"):
        if not (DATA_DIR / name).is_file():
            raise FileNotFoundError(f"Missing local data file: {name}")
    manifest = json.loads((DATA_DIR / "split_manifest.json").read_text(encoding="utf-8"))
    if any(manifest.get("normalized_overlap", {}).values()):
        raise ValueError("Split manifest reports overlapping normalized sentences")
    # Keep an explicitly chosen HF_HOME; cache files are never part of source exports.
    os.environ.setdefault("HF_HOME", str(ROOT / ".cache/huggingface"))
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    import csv
    import gc
    import hashlib
    import math
    import random
    import subprocess
    import time
    from datetime import datetime
    from itertools import islice
    from importlib.metadata import version

    import torch
    from torch.utils.data import DataLoader, Dataset
    from peft import LoraConfig, PeftConfig, PeftModel, TaskType, get_peft_model
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, get_cosine_schedule_with_warmup

    for key in ("batch_size", "grad_accum", "max_length", "epochs", "lora_rank"):
        if CONFIG[key] < 1:
            raise ValueError(f"{key}는 1 이상이어야 합니다.")
    for key in ("train_samples", "validation_samples"):
        if CONFIG[key] < 0:
            raise ValueError(f"{key}는 0 이상이어야 합니다.")
    if CONFIG["require_cuda"] and not torch.cuda.is_available():
        raise RuntimeError("GPU 커널을 선택하세요. CPU 실험은 require_cuda=False로 명시적으로 바꿀 수 있습니다.")

    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    USE_AMP = DEVICE.type == "cuda"
    BASE_DTYPE = torch.float16 if USE_AMP else torch.float32
    random.seed(CONFIG["seed"])
    torch.manual_seed(CONFIG["seed"])
    if USE_AMP:
        torch.cuda.manual_seed_all(CONFIG["seed"])
        torch.backends.cuda.matmul.allow_tf32 = True

    RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    RUN_DIR = args.run_dir.expanduser().resolve() if args.run_dir else ROOT / "checkpoints" / RUN_ID
    ADAPTER_DIR = RUN_DIR / "adapter"
    RUN_DIR.mkdir(parents=True, exist_ok=False)
    print(json.dumps(CONFIG, indent=2, ensure_ascii=False))
    print("이번 실험:", RUN_DIR)
    print("최고 검증 성능의 가중치를 저장할 곳:", ADAPTER_DIR)
    print("같은 seed라도 GPU·라이브러리 버전에 따라 미세한 차이가 날 수 있습니다.")


    def read_pairs(path):
        with Path(path).open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        if not rows or not {"source", "target"}.issubset(rows[0]):
            raise ValueError(f"source와 target 열이 있는 TSV가 필요합니다: {path}")
        if any(not row["source"].strip() or not row["target"].strip() for row in rows):
            raise ValueError(f"빈 문장이 있습니다: {path}")
        for row_number, row in enumerate(rows, start=1):
            row.setdefault("source_id", f"local:{Path(path).name}:source:{row_number}")
            row.setdefault("target_id", f"local:{Path(path).name}:target:{row_number}")
        return rows


    def choose_rows(rows, limit, seed):
        return random.Random(seed).sample(rows, min(limit, len(rows))) if limit else list(rows)


    all_train_rows = read_pairs(DATA_DIR / "train.tsv")
    all_validation_rows = read_pairs(DATA_DIR / "validation.tsv")
    all_test_rows = read_pairs(DATA_DIR / "test.tsv")
    train_rows = choose_rows(all_train_rows, CONFIG["train_samples"], CONFIG["seed"])
    validation_rows = choose_rows(all_validation_rows, CONFIG["validation_samples"], CONFIG["seed"] + 1)
    print(f"원본 train / validation / test: {len(all_train_rows):,} / {len(all_validation_rows):,} / {len(all_test_rows):,}")
    print(f"이번 학습 / 검증: {len(train_rows):,} / {len(validation_rows):,}")



    def normalized_sentences(rows, column):
        import unicodedata
        return {" ".join(unicodedata.normalize("NFKC", row[column]).casefold().split()) for row in rows}


    for split_name, rows in (("validation", all_validation_rows), ("test", all_test_rows)):
        for column in ("source", "target"):
            overlap = normalized_sentences(all_train_rows, column) & normalized_sentences(rows, column)
            if overlap:
                raise ValueError(f"train/{split_name} split overlap in {column}: {len(overlap)}")

    for column in ("source", "target"):
        if normalized_sentences(all_validation_rows, column) & normalized_sentences(all_test_rows, column):
            raise ValueError(f"validation/test split overlap in {column}")


    tokenizer = AutoTokenizer.from_pretrained(
        CONFIG["base_model"], src_lang="en", tgt_lang="ko",
        local_files_only=CONFIG["local_files_only"], revision=CONFIG["base_revision"],
    )


    def truncation_counts(rows):
        source_lengths = tokenizer([row["source"] for row in rows], truncation=False)["input_ids"]
        target_lengths = tokenizer(text_target=[row["target"] for row in rows], truncation=False)["input_ids"]
        return {
            "source_truncated": sum(len(ids) > CONFIG["max_length"] for ids in source_lengths),
            "target_truncated": sum(len(ids) > CONFIG["max_length"] for ids in target_lengths),
        }


    TRUNCATION_COUNTS = {"train": truncation_counts(train_rows), "validation": truncation_counts(validation_rows)}
    print("max_length로 잘릴 문장 수:", TRUNCATION_COUNTS)


    class TranslationPairs(Dataset):
        def __init__(self, rows):
            self.rows = rows

        def __len__(self):
            return len(self.rows)

        def __getitem__(self, index):
            row = self.rows[index]
            return row["source"], row["target"]


    def collate_pairs(rows):
        sources, targets = zip(*rows)
        batch = tokenizer(
            list(sources), padding=True, truncation=True,
            max_length=CONFIG["max_length"], return_tensors="pt",
        )
        target_ids = tokenizer(
            text_target=list(targets), padding=True, truncation=True,
            max_length=CONFIG["max_length"], return_tensors="pt",
        )["input_ids"]
        batch["labels"] = target_ids.masked_fill(target_ids == tokenizer.pad_token_id, -100)
        return batch


    train_loader = DataLoader(
        TranslationPairs(train_rows), batch_size=CONFIG["batch_size"], shuffle=True,
        generator=torch.Generator().manual_seed(CONFIG["seed"]),
        collate_fn=collate_pairs, num_workers=0, pin_memory=USE_AMP,
    )
    validation_loader = DataLoader(
        TranslationPairs(validation_rows), batch_size=CONFIG["batch_size"], shuffle=False,
        collate_fn=collate_pairs, num_workers=0, pin_memory=USE_AMP,
    )
    sample_batch = collate_pairs([(train_rows[0]["source"], train_rows[0]["target"])])
    print("미니배치 하나의 tensor 크기:", {name: tuple(tensor.shape) for name, tensor in sample_batch.items()})


    model = AutoModelForSeq2SeqLM.from_pretrained(
        CONFIG["base_model"], dtype=BASE_DTYPE,
        local_files_only=CONFIG["local_files_only"], revision=CONFIG["base_revision"],
    )
    if RESUME_ADAPTER is not None:
        RESUME_ADAPTER = Path(RESUME_ADAPTER).expanduser().resolve()
        resume_config = PeftConfig.from_pretrained(str(RESUME_ADAPTER), local_files_only=True)
        if resume_config.base_model_name_or_path != CONFIG["base_model"]:
            raise ValueError("이전 어댑터의 base_model과 현재 CONFIG['base_model']이 다릅니다.")
        model = PeftModel.from_pretrained(model, str(RESUME_ADAPTER), is_trainable=True, local_files_only=True)
        print("기존 어댑터 가중치로 시작:", RESUME_ADAPTER)
        print("기존 LoRA 구조를 사용하며 optimizer와 epoch 상태는 새로 시작합니다.")
    else:
        lora_config = LoraConfig(
            task_type=TaskType.SEQ_2_SEQ_LM,
            target_modules=["q_proj", "v_proj"],
            r=CONFIG["lora_rank"], lora_alpha=CONFIG["lora_alpha"],
            lora_dropout=CONFIG["lora_dropout"], bias="none",
        )
        model = get_peft_model(model, lora_config)

    for parameter in model.parameters():
        if parameter.requires_grad:
            parameter.data = parameter.data.float()
    del parameter
    model.config.use_cache = False
    model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model = model.to(DEVICE)
    model.print_trainable_parameters()
    print("학습 파라미터 자료형:", {parameter.dtype for parameter in model.parameters() if parameter.requires_grad})
    if USE_AMP:
        print(f"현재 PyTorch GPU 메모리: {torch.cuda.memory_allocated() / 2**30:.2f} GiB")


    def file_sha256(path):
        digest = hashlib.sha256()
        with Path(path).open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()


    def write_json(path, value):
        Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


    def validation_loss(current_model):
        current_model.eval()
        total_loss, total_tokens = 0.0, 0
        with torch.inference_mode():
            for cpu_batch in validation_loader:
                token_count = int(cpu_batch["labels"].ne(-100).sum())
                batch = {name: tensor.to(DEVICE, non_blocking=USE_AMP) for name, tensor in cpu_batch.items()}
                with torch.autocast(device_type=DEVICE.type, dtype=torch.float16, enabled=USE_AMP):
                    loss = current_model(**batch).loss
                total_loss += float(loss.float().item()) * token_count
                total_tokens += token_count
        if not math.isfinite(total_loss) or total_tokens == 0:
            raise RuntimeError("검증 loss가 유효하지 않습니다. 데이터와 learning_rate를 확인하세요.")
        return total_loss / total_tokens


    def run_training():
        if (ADAPTER_DIR / "adapter_config.json").exists():
            raise RuntimeError("이 실험에는 이미 결과가 있습니다. 커널을 재시작하고 새 실험으로 실행하세요.")

        trainable_parameters = [parameter for parameter in model.parameters() if parameter.requires_grad]
        optimizer = torch.optim.AdamW(trainable_parameters, lr=CONFIG["learning_rate"])
        scaler = torch.amp.GradScaler("cuda", enabled=USE_AMP)
        history = []
        best_loss = float("inf")
        experiment = {
            "run_id": RUN_ID,
            "status": "running",
            "created_at": datetime.now().astimezone().isoformat(),
            "base_model": CONFIG["base_model"],
            "base_model_commit": getattr(model.config, "_commit_hash", None),
            "adapter_path": str(ADAPTER_DIR.resolve()),
            "data_path": str(DATA_DIR.resolve()),
            "config": dict(CONFIG),
            "resume_adapter": str(RESUME_ADAPTER) if RESUME_ADAPTER is not None else None,
            "resume_includes_optimizer": False,
            "effective_lora_config": json.loads(json.dumps(model.peft_config["default"].to_dict(), default=list)),
            "train_examples": len(train_rows),
            "validation_examples": len(validation_rows),
            "data_sha256": {name: file_sha256(DATA_DIR / name) for name in ("train.tsv", "validation.tsv", "test.tsv")},
            "truncation_counts": TRUNCATION_COUNTS,
            "torch_version": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "package_versions": {name: version(name) for name in ("transformers", "peft", "sentencepiece")},
            "device": str(DEVICE),
            "gpu": torch.cuda.get_device_name(0) if USE_AMP else None,
            "loss_reduction": "mean over non-padding target tokens",
            "split_caveat": "Connected components of source/target IDs and normalized text; exact cross-split overlap zero. Pretraining overlap unknown.",
        }
        write_json(RUN_DIR / "experiment.json", experiment)
        windows_per_epoch = math.ceil(len(train_loader) / CONFIG["grad_accum"])
        total_updates = windows_per_epoch * CONFIG["epochs"]
        scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=max(1, round(total_updates * .03)), num_training_steps=total_updates)
        experiment["scheduler"] = {"type": "cosine", "warmup_fraction": .03, "total_updates": total_updates}
        experiment["split_manifest"] = json.loads((DATA_DIR / "split_manifest.json").read_text(encoding="utf-8"))
        experiment["baseline_validation_loss"] = validation_loss(model)
        experiment["total_parameters"] = sum(p.numel() for p in model.parameters())
        experiment["trainable_parameters"] = sum(p.numel() for p in model.parameters() if p.requires_grad)
        write_json(RUN_DIR / "experiment.json", experiment)
        print("BASELINE validation loss:", experiment["baseline_validation_loss"], flush=True)
        print(f"학습 시작: {DEVICE}, {len(train_rows):,}쌍, epoch당 최대 {windows_per_epoch}회 갱신", flush=True)

        try:
            for epoch in range(1, CONFIG["epochs"] + 1):
                started = time.perf_counter()
                model.train()
                model.config.use_cache = False
                if USE_AMP:
                    torch.cuda.reset_peak_memory_stats()
                train_loss_sum, train_token_count = 0.0, 0
                optimizer_windows, skipped_updates = 0, 0
                train_iterator = iter(train_loader)

                while True:
                    # 마지막 묶음이 grad_accum보다 작아도 실제 토큰 수로 정규화합니다.
                    cpu_window = list(islice(train_iterator, CONFIG["grad_accum"]))
                    if not cpu_window:
                        break
                    window_tokens = sum(int(batch["labels"].ne(-100).sum()) for batch in cpu_window)
                    optimizer.zero_grad(set_to_none=True)

                    for cpu_batch in cpu_window:
                        batch_tokens = int(cpu_batch["labels"].ne(-100).sum())
                        batch = {name: tensor.to(DEVICE, non_blocking=USE_AMP) for name, tensor in cpu_batch.items()}
                        with torch.autocast(device_type=DEVICE.type, dtype=torch.float16, enabled=USE_AMP):
                            loss = model(**batch).loss
                        if not torch.isfinite(loss).item():
                            raise RuntimeError("loss가 NaN/Inf입니다. learning_rate와 입력을 확인하세요.")
                        train_loss_sum += float(loss.detach().float().item()) * batch_tokens
                        train_token_count += batch_tokens
                        scaler.scale(loss * (batch_tokens / window_tokens)).backward()

                    scaler.unscale_(optimizer)
                    torch.nn.utils.clip_grad_norm_(trainable_parameters, CONFIG["max_grad_norm"])
                    previous_scale = scaler.get_scale()
                    scaler.step(optimizer)
                    scaler.update()
                    if scaler.get_scale() < previous_scale:
                        skipped_updates += 1  # AMP overflow이면 학습률 스케줄도 멈춥니다.
                    else:
                        scheduler.step()
                    optimizer.zero_grad(set_to_none=True)
                    optimizer_windows += 1
                    if optimizer_windows % 50 == 0 or optimizer_windows == windows_per_epoch:
                        average = train_loss_sum / train_token_count
                        print(f"epoch {epoch}/{CONFIG['epochs']} | 갱신 묶음 {optimizer_windows}/{windows_per_epoch} | 평균 loss {average:.4f}", flush=True)

                epoch_validation_loss = validation_loss(model)
                improved = epoch_validation_loss < best_loss
                record = {
                    "epoch": epoch,
                    "train_loss": train_loss_sum / train_token_count,
                    "validation_loss": epoch_validation_loss,
                    "elapsed_seconds": round(time.perf_counter() - started, 2),
                    "optimizer_windows": optimizer_windows,
                    "skipped_updates": skipped_updates,
                    "target_tokens": train_token_count,
                    "peak_gpu_gib": round(torch.cuda.max_memory_allocated() / 2**30, 3) if USE_AMP else 0,
                    "saved_best": improved,
                    "learning_rate_end": scheduler.get_last_lr()[0],
                }
                history.append(record)
                if improved:
                    best_loss = epoch_validation_loss
                    model.save_pretrained(ADAPTER_DIR, safe_serialization=True)
                    tokenizer.save_pretrained(ADAPTER_DIR)
                    experiment["best_epoch"] = epoch
                    experiment["best_validation_loss"] = best_loss
                    experiment["adapter_sha256"] = file_sha256(ADAPTER_DIR / "adapter_model.safetensors")
                    print("최고 검증 모델 저장:", ADAPTER_DIR, flush=True)

                experiment["last_completed_epoch"] = epoch
                write_json(RUN_DIR / "history.json", history)
                with (RUN_DIR / "history.csv").open("w", encoding="utf-8-sig", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=list(record))
                    writer.writeheader()
                    writer.writerows(history)
                write_json(RUN_DIR / "experiment.json", experiment)
                print(json.dumps(record, ensure_ascii=False, indent=2), flush=True)
                if len(history) >= 3 and not any(r["saved_best"] for r in history[-2:]):
                    experiment["early_stopping"] = "Two completed epochs without validation-loss improvement"
                    break

            experiment["status"] = "completed"
        except KeyboardInterrupt:
            experiment["status"] = "interrupted"
            print("사용자가 학습을 중단했습니다. 완료된 epoch의 저장 결과를 확인하세요.")
            raise
        except Exception:
            experiment["status"] = "failed"
            raise
        finally:
            optimizer.zero_grad(set_to_none=True)
            model.eval()
            write_json(RUN_DIR / "experiment.json", experiment)
        return history, experiment


    history, experiment = run_training()
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axis = plt.subplots(figsize=(8, 4))
    for key in ("train_loss", "validation_loss"):
        axis.plot([r["epoch"] for r in history], [r[key] for r in history], "o-", label=key)
    axis.axhline(experiment["baseline_validation_loss"], color="gray", linestyle="--", label="Base validation")
    axis.set(xlabel="Epoch", ylabel="Token-weighted cross entropy", title="Grouped split / M2M100 LoRA")
    axis.set_xticks([r["epoch"] for r in history])
    axis.legend(); axis.grid(alpha=.2); fig.tight_layout()
    fig.savefig(RUN_DIR / "loss.png", dpi=180)
    print("EXTENDED_RUN_DIR=" + str(RUN_DIR), flush=True)
    print("BEST_ADAPTER=" + str(ADAPTER_DIR), flush=True)


if __name__ == "__main__":
    main()
