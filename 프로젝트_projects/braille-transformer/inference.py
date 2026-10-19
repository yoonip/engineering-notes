"""학습된 best.pt를 읽어 점자를 한국어로 생성합니다. CPU만 있는 PC도 지원합니다.

  python inference.py --checkpoint checkpoints/실험폴더 --text "⠁⠒" --device cpu

checkpoint는 학습 결과 폴더이며 config.json, vocab.json, best.pt가 필요합니다.
PyTorch 코드와 이 세 파일만 있으면 말뭉치나 CUDA 없이 추론할 수 있습니다.
best.pt는 Python 소스가 아니라 학습한 실수 배열입니다. 모델 구조 코드는 model.py에
있고 그 구조에 맞는 숫자를 load_state_dict가 채웁니다. .eval()은 dropout를 끄고,
inference_mode는 gradient 저장을 끕니다. 둘 다 학습값을 새로 수정하지 않습니다.

실제 추론은 점자만 받습니다. BOS → 첫 자모 → 다음 자모 → ... → EOS입니다.
정답 앞부분을 제공하는 학습/검증 loss와 달리, 여기에는 한국어 정답이 없습니다.
입력이 모델 한도보다 길면 내용을 조용히 버리지 않고 오류를 알려 줍니다.
출력이 한도 안에 EOS를 못 만들면 결과에 warnings와 ended_with_eos=False가 남습니다.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from contextlib import nullcontext
from pathlib import Path

import torch

from model import (BOS, EOS, PAD, UNK, BrailleTransformer, ModelConfig, Vocabulary,
                   greedy_generate, sha256_file, uncombined_jamo_count)


def normalize_braille_input(text: str) -> tuple[str, list[str]]:
    """GUI와 CLI 모두 같은 규칙을 씁니다. 점자 셀을 묵자로 바꾸지는 않습니다.

    학습 원문은 U+2801..U+283F와 ASCII space만 포함했습니다. 사용자가 넣은
    U+2800(빈 점자 셀), 줄바꿈, tab은 명시적으로 ASCII space로 바꾸고 알립니다.
    CRLF는 한 개의 줄바꿈으로 취급합니다. 원래 연속 공백은 합치지 않습니다.
    8점 점자나 일반 한글/영문은 이 모델의 입력 형식이 아니므로 거절합니다.
    """
    if not isinstance(text, str) or not text:
        raise ValueError("Unicode 6점 점자 문자열을 입력하세요.")
    original = text
    text = text.replace("\r\n", "\n")
    text = "".join(" " if character == "\u2800" or character.isspace() else character for character in text)
    invalid = sorted(set(character for character in text if character != " " and not 0x2801 <= ord(character) <= 0x283F))
    if invalid:
        codes = ", ".join(f"{char!r}(U+{ord(char):04X})" for char in invalid[:10])
        raise ValueError(f"6점 Unicode 점자와 공백만 입력할 수 있습니다. 지원하지 않는 문자: {codes}")
    if not text.strip():
        raise ValueError("공백 이외의 점자 셀을 하나 이상 입력하세요.")
    warnings = []
    if text != original:
        warnings.append("빈 점자 셀(U+2800) 또는 줄바꿈/tab 등 공백 문자를 학습 형식인 ASCII space로 바꿨습니다. 연속 공백은 유지했습니다.")
    return text, warnings


@torch.inference_mode()
def beam_generate(model: BrailleTransformer, source: torch.Tensor,
                  max_new_tokens: int, beam_size: int) -> tuple[torch.Tensor, torch.Tensor]:
    """한 문장의 여러 후보를 유지하는 간단한 beam search입니다.

    greedy는 매번 가장 확률 높은 한 토큰만 택합니다. beam은 누적 log 확률이 좋은
    여러 접두사를 남깁니다. beam이 커도 항상 더 정확하다는 뜻은 아닙니다.
    여기서는 길이 페널티 0.6으로 최종 후보 점수를 나눕니다. full test 기본은
    비교 조건을 일정하게 하기 위해 빠른 batched greedy(beam1)를 사용합니다.
    """
    if source.size(0) != 1:
        raise ValueError("beam search는 한 문장만 받습니다. 전체 평가는 greedy batch를 쓰세요.")
    memory, source_padding = model.encode(source)
    sequences = torch.tensor([[BOS]], dtype=torch.long, device=source.device)
    scores = torch.zeros(1, device=source.device)
    finished = torch.zeros(1, dtype=torch.bool, device=source.device)
    for _ in range(max_new_tokens):
        count = sequences.size(0)
        logits = model.decode(sequences, memory.expand(count, -1, -1),
            source_padding.expand(count, -1))[:, -1].float()
        logits[:, PAD] = -torch.inf
        logits[:, BOS] = -torch.inf
        log_probabilities = logits.log_softmax(-1)
        # 완료된 후보는 PAD만 덧붙이며 기존 점수를 유지합니다.
        log_probabilities[finished] = -torch.inf
        log_probabilities[finished, PAD] = 0
        candidates = scores[:, None] + log_probabilities
        new_scores, flat_indices = candidates.flatten().topk(min(beam_size, candidates.numel()))
        parents = flat_indices // logits.size(-1)
        next_tokens = flat_indices % logits.size(-1)
        sequences = torch.cat([sequences[parents], next_tokens[:, None]], dim=1)
        finished = finished[parents] | next_tokens.eq(EOS)
        scores = new_scores
        if bool(finished.all()):
            break
    lengths = sequences[:, 1:].ne(PAD).sum(-1).clamp_min(1)
    adjusted = scores / (((5 + lengths.float()) / 6) ** 0.6)
    best = int(adjusted.argmax())
    return sequences[best:best + 1, 1:], finished[best:best + 1]


class BrailleTranslator:
    """GUI/노트북/CLI가 함께 사용하는 작은 API. load() 후 여러 번 translate()."""
    def __init__(self, checkpoint: str | Path, device: str = "auto", cpu_threads: int = 4):
        self.checkpoint = Path(checkpoint).resolve()
        self.requested_device = device
        if device not in {"auto", "cuda", "cpu"}:
            raise ValueError("device는 auto/cuda/cpu 중 하나입니다.")
        self.device = torch.device("cuda" if device == "auto" and torch.cuda.is_available()
            else "cpu" if device == "auto" else device)
        if self.device.type == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA를 명시했지만 사용할 수 없습니다.")
        self.cpu_threads = cpu_threads
        self.model = None

    def load(self) -> "BrailleTranslator":
        if self.model is not None:
            return self
        for filename in ("config.json", "vocab.json", "best.pt"):
            if not (self.checkpoint / filename).is_file():
                raise FileNotFoundError(f"필수 학습 결과 파일이 없습니다: {self.checkpoint / filename}")
        torch.set_num_threads(self.cpu_threads)
        torch.backends.mha.set_fastpath_enabled(False)
        self.config = json.loads((self.checkpoint / "config.json").read_text(encoding="utf-8"))
        expected_vocab_hash = self.config.get("data", {}).get("vocab_sha256")
        if not expected_vocab_hash:
            raise ValueError("config.json에 학습 당시 vocab_sha256이 없습니다. 원래 학습 묶음을 사용하세요.")
        if sha256_file(self.checkpoint / "vocab.json") != expected_vocab_hash:
            raise ValueError("vocab.json이 학습 당시와 다릅니다. 문자 개수가 같아도 토큰 순서가 다르면 "
                "같은 가중치가 다른 문자를 뜻하므로 추론을 중단합니다.")
        self.vocab = Vocabulary.load(self.checkpoint / "vocab.json")
        self.model_config = ModelConfig(**self.config["model"])
        if (self.model_config.source_vocab_size, self.model_config.target_vocab_size) != (
                len(self.vocab.source_tokens), len(self.vocab.target_tokens)):
            raise ValueError("config의 어휘 크기와 vocab.json이 일치하지 않습니다.")
        self.weights_sha256 = sha256_file(self.checkpoint / "best.pt")
        self.model = BrailleTransformer(self.model_config)
        weights = torch.load(self.checkpoint / "best.pt", map_location="cpu", weights_only=True)
        for name, tensor in weights.items():
            if not bool(torch.isfinite(tensor).all()):
                raise ValueError(f"학습 가중치 {name}에 NaN/Inf가 있습니다. 정상 checkpoint를 사용하세요.")
        # strict=True가 기본입니다. 맞지 않는 키/shape를 무시한 채 실행하지 않습니다.
        self.model.load_state_dict(weights, strict=True)
        self.model.to(self.device).eval()
        return self

    def amp_context(self):
        return torch.autocast("cuda", dtype=torch.float16) if self.device.type == "cuda" else nullcontext()

    @torch.inference_mode()
    def translate(self, text: str, max_new_tokens: int | None = None, beam_size: int = 1) -> dict:
        self.load()
        normalized, warnings = normalize_braille_input(text)
        source_ids = self.vocab.encode_source(normalized)
        if len(source_ids) > self.model_config.max_source_length:
            raise ValueError(f"입력 토큰 {len(source_ids)}개(BOS/EOS 포함)가 모델 한도 "
                f"{self.model_config.max_source_length}개를 넘었습니다. 문장 단위로 나누세요. 자동으로 자르지 않습니다.")
        unknown = source_ids.count(UNK)
        if unknown:
            warnings.append(f"훈련 어휘에 없는 점자 {unknown}개가 UNK로 입력되었습니다.")
        limit = self.model_config.max_target_length - 1 if max_new_tokens is None else max_new_tokens
        if not 1 <= limit <= self.model_config.max_target_length - 1:
            raise ValueError(f"max_new_tokens는 1..{self.model_config.max_target_length - 1}이어야 합니다.")
        if not 1 <= beam_size <= 8:
            raise ValueError("beam_size는 1..8이어야 합니다.")
        source = torch.tensor([source_ids], dtype=torch.long, device=self.device)
        if self.device.type == "cuda":
            torch.cuda.synchronize(self.device)
        started = time.perf_counter()
        with self.amp_context():
            if beam_size == 1:
                generated, ended = greedy_generate(self.model, source, limit)
            else:
                generated, ended = beam_generate(self.model, source, limit, beam_size)
        if self.device.type == "cuda":
            torch.cuda.synchronize(self.device)
        seconds = time.perf_counter() - started
        ids = generated[0].tolist()
        translation = self.vocab.decode_target(ids)
        ended_with_eos = bool(ended[0])
        output_unknown = ids.count(UNK)
        uncombined = uncombined_jamo_count(translation)
        if not ended_with_eos:
            warnings.append(f"출력 한도 {limit}토큰에 도달했지만 EOS가 나오지 않았습니다. 미완성 번역일 수 있습니다.")
        if output_unknown:
            warnings.append(f"출력에 UNK {output_unknown}개가 있어 �로 표시했습니다.")
        if uncombined:
            warnings.append(f"NFC 변환 뒤 독립 자모 {uncombined}개가 남았습니다. 한글 조합이 잘못되었을 수 있습니다.")
        return {"translation": translation, "normalized_input": normalized,
            "input_tokens": len(source_ids), "output_tokens": sum(token not in (PAD, EOS) for token in ids),
            "ended_with_eos": ended_with_eos, "unknown_source_tokens": unknown,
            "unknown_output_tokens": output_unknown, "uncombined_jamo_characters": uncombined,
            "seconds": seconds, "device": str(self.device), "checkpoint": str(self.checkpoint),
            "weights_sha256": self.weights_sha256, "beam_size": beam_size, "warnings": warnings}


def main() -> None:
    # Windows 기본 cp949 콘솔은 Unicode 점자를 출력할 수 없습니다.
    # 파일 저장과 동일한 UTF-8로 명시해 CLI에서도 결과가 사라지지 않게 합니다.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--max-new-tokens", type=int)
    parser.add_argument("--beam-size", type=int, default=1)
    parser.add_argument("--cpu-threads", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    translator = BrailleTranslator(args.checkpoint, args.device, args.cpu_threads).load()
    result = translator.translate(args.text, args.max_new_tokens, args.beam_size)
    serialized = json.dumps(result, ensure_ascii=False, indent=2)
    print(serialized)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")


if __name__ == "__main__":
    main()
