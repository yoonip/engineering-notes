"""정답 한국어를 모델에 주지 않고 held-out 점자를 실제 생성해 평가합니다.

  python evaluate.py --checkpoint checkpoints/실험 --device cuda --batch-size 32
  python evaluate.py --checkpoint checkpoints/실험 --max-examples 128 --output-dir logs/quick
  python evaluate.py --checkpoint checkpoints/실험 --data-dir data/다른분할 --data-manifest data/다른_manifest.json

분할 파일은 prepare_data.py가 기록한 manifest의 SHA-256과 같아야 합니다.
--data-dir을 바꾸었으면 그 전처리 실행의 --data-manifest도 함께 지정하세요.
manifest 안의 절대 경로 대신 파일 내용 해시를 비교하므로 동일한 분할의 이동은 가능합니다.

CER = 글자 단위 편집거리 합 / 정답 글자 수 합입니다. 편집거리는 삽입/삭제/치환
각각을 1로 셉니다. 낮을수록 좋고 0이면 모든 글자가 맞습니다. 삽입이 많으면 1을
넘을 수도 있습니다. 1-CER를 무조건 '정확도'라고 부르면 안 됩니다.
여기서는 NFC 한국어(완성 음절) CER와 NFD 자모 CER를 따로 냅니다. '각'→'간'은
음절에서는 1글자 오류지만 자모에서는 종성 하나만 다릅니다. 공백/숫자/기호도 셉니다.
문장 exact match는 공백까지 완전히 같은 문장의 비율입니다.

validation loss는 teacher forcing 지표이고 이 파일은 autoregressive 생성 지표입니다.
두 지표를 같은 '정확도'로 섞지 마세요. test 점수를 보고 설정을 계속 고르면 test도
사실상 검증 데이터가 됩니다. 탐색에는 --split validation을 쓰고 최종 test는 아껴 두세요.
"""
from __future__ import annotations

import argparse
import csv
import json
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

import torch
from torch import nn

from inference import BrailleTranslator, normalize_braille_input
from model import EOS, PAD, UNK, greedy_generate, read_jsonl, sha256_file, uncombined_jamo_count

try:
    from rapidfuzz.distance import Levenshtein
    def edit_distance(left: str, right: str) -> int:
        return int(Levenshtein.distance(left, right))
    DISTANCE_IMPLEMENTATION = "rapidfuzz.distance.Levenshtein"
except ImportError:
    def edit_distance(left: str, right: str) -> int:
        """추가 패키지가 없어도 작동하는 동적 계획법. 긴 쪽×짧은 쪽 시간입니다."""
        if len(left) < len(right):
            left, right = right, left
        previous = list(range(len(right) + 1))
        for i, char_left in enumerate(left, 1):
            current = [i]
            for j, char_right in enumerate(right, 1):
                current.append(min(current[-1] + 1, previous[j] + 1,
                    previous[j - 1] + int(char_left != char_right)))
            previous = current
        return previous[-1]
    DISTANCE_IMPLEMENTATION = "python_dynamic_programming"


def aggregate(records: list[dict]) -> dict:
    characters = sum(row["reference_characters"] for row in records)
    jamo_characters = sum(row["reference_nfd_characters"] for row in records)
    errors = sum(row["character_errors"] for row in records)
    jamo_errors = sum(row["nfd_character_errors"] for row in records)
    return {"examples": len(records), "CER": errors / characters,
        "CER_percent": 100 * errors / characters, "NFD_CER": jamo_errors / jamo_characters,
        "NFD_CER_percent": 100 * jamo_errors / jamo_characters,
        "exact_match_rate": sum(row["exact_match"] for row in records) / len(records),
        "exact_match_count": sum(row["exact_match"] for row in records),
        "character_errors": errors, "reference_characters": characters,
        "nfd_character_errors": jamo_errors, "reference_nfd_characters": jamo_characters,
        "ended_with_eos_rate": sum(row["ended_with_eos"] for row in records) / len(records),
        "length_cap_count": sum(not row["ended_with_eos"] for row in records),
        "unknown_source_tokens": sum(row["unknown_source_tokens"] for row in records),
        "unknown_reference_tokens": sum(row["unknown_reference_tokens"] for row in records),
        "unknown_generated_tokens": sum(row["unknown_generated_tokens"] for row in records),
        "uncombined_jamo_characters": sum(row["uncombined_jamo_characters"] for row in records),
        "uncombined_jamo_sentence_rate": sum(row["uncombined_jamo_characters"] > 0 for row in records) / len(records)}


def verify_data_manifest(path: Path, split: str, data_hash: str, training_data: dict) -> dict:
    """시험 파일 이름만 믿지 않고 전처리 때 확정한 분할 내용과 비교합니다.

    manifest의 train/validation도 학습 config와 연결하여 다른 전처리 실행의
    test를 우연히 섞지 않습니다. manifest는 prepare_data.py의 원본 기록을 쓰며,
    평가가 통과하도록 파일 해시를 수동으로 고쳐 쓰면 분할 검증의 의미가 없어집니다.
    """
    path = path.resolve()
    if not path.is_file():
        raise FileNotFoundError(f"전처리 manifest가 없습니다: {path}. "
            "prepare_data.py가 만든 파일을 --data-manifest로 지정하세요.")
    manifest_hash = sha256_file(path)
    manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    outputs = manifest.get("outputs") if isinstance(manifest, dict) else None
    if not isinstance(outputs, dict):
        raise ValueError("data manifest에 outputs.train/validation/test 분할 기록이 필요합니다.")
    hashes = {}
    for name in ("train", "validation", "test"):
        entry = outputs.get(name)
        value = entry.get("sha256") if isinstance(entry, dict) else None
        if (not isinstance(value, str) or len(value) != 64
                or any(char not in "0123456789abcdefABCDEF" for char in value)):
            raise ValueError(f"data manifest의 outputs.{name}.sha256이 올바르지 않습니다.")
        hashes[name] = value.lower()
    for name in ("train", "validation"):
        if hashes[name] != training_data[f"{name}_sha256"]:
            raise ValueError(f"data manifest의 {name} 분할이 학습 당시와 다릅니다. "
                "이 체크포인트를 학습한 전처리 실행의 manifest를 사용하세요.")
    if data_hash != hashes[split]:
        raise ValueError(f"{split} 파일이 전처리 manifest의 SHA-256과 다릅니다. "
            "변경된 시험/검증 자료를 원래 분할의 평가로 저장하지 않습니다.")
    return {"data_manifest_path": str(path), "data_manifest_sha256": manifest_hash,
        "data_manifest_split_sha256": hashes[split], "data_manifest_verified": True}


@torch.inference_mode()
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parent / "data" / "processed")
    parser.add_argument("--data-manifest", type=Path,
        default=Path(__file__).resolve().parent / "data_manifest.json",
        help="prepare_data.py의 manifest; 기본은 프로젝트/data_manifest.json. 다른 분할은 해당 manifest도 지정")
    parser.add_argument("--split", choices=["validation", "test"], default="test")
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-examples", type=int, default=0, help="0=전체; 앞 N개로 빠른 점검")
    parser.add_argument("--max-new-tokens", type=int, help="생략하면 모델 target 한도-1")
    parser.add_argument("--cpu-threads", type=int, default=4)
    parser.add_argument("--output-dir", type=Path, help="기본 checkpoint/evaluation_분할")
    args = parser.parse_args()
    if args.batch_size < 1 or args.max_examples < 0:
        raise ValueError("batch-size>=1, max-examples>=0이어야 합니다.")
    output_dir = args.output_dir or args.checkpoint / ("evaluation_" + args.split)
    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir = args.data_dir.resolve()
    data_path = data_dir / f"{args.split}.jsonl"
    data_hash = sha256_file(data_path)
    translator = BrailleTranslator(args.checkpoint, args.device, args.cpu_threads).load()
    # 같은 폴더의 train/validation 내용이 학습 때와 같은지 확인합니다. 파일 이름만
    # 맞춘 다른 분할을 원래의 held-out 결과라고 보고하지 않습니다.
    training_data = translator.config["data"]
    for split in ("train", "validation"):
        if sha256_file(data_dir / f"{split}.jsonl") != training_data[f"{split}_sha256"]:
            raise ValueError(f"{split} split이 학습 당시와 다릅니다. 원래 분할로 평가하세요.")
    manifest_evidence = verify_data_manifest(args.data_manifest, args.split, data_hash, training_data)
    rows = read_jsonl(data_path)
    full_count = len(rows)
    if args.max_examples:
        rows = rows[:args.max_examples]
    limit = translator.model_config.max_target_length - 1 if args.max_new_tokens is None else args.max_new_tokens
    if not 1 <= limit <= translator.model_config.max_target_length - 1:
        raise ValueError("max-new-tokens가 모델 출력 길이 범위를 벗어났습니다.")
    encoded = []
    for index, row in enumerate(rows):
        normalized, input_warnings = normalize_braille_input(row["braille"])
        tokens = translator.vocab.encode_source(normalized)
        if len(tokens) > translator.model_config.max_source_length:
            raise ValueError(f"id={row.get('id', index)}: 입력 {len(tokens)}토큰이 모델 길이를 초과합니다. "
                "test를 자동 제외하거나 자르지 않습니다.")
        encoded.append({"index": index, "tokens": tokens, "warnings": input_warnings})
    # 길이순 batch는 정답을 사용하지 않습니다. 짧은 문장이 긴 문장을 기다리며 PAD를
    # 많이 계산하는 것을 줄일 뿐이며, 출력 TSV는 원래 데이터 순서로 되돌립니다.
    encoded.sort(key=lambda item: len(item["tokens"]))
    records = []
    if translator.device.type == "cuda":
        torch.cuda.synchronize(translator.device)
        torch.cuda.reset_peak_memory_stats(translator.device)
    started = time.perf_counter()
    for start in range(0, len(encoded), args.batch_size):
        batch = encoded[start:start + args.batch_size]
        source = nn.utils.rnn.pad_sequence([torch.tensor(item["tokens"], dtype=torch.long) for item in batch],
            batch_first=True, padding_value=PAD).to(translator.device)
        with translator.amp_context():
            ids, ended = greedy_generate(translator.model, source, limit)
        ids, ended = ids.cpu().tolist(), ended.cpu().tolist()
        for item, generated, has_eos in zip(batch, ids, ended):
            index = item["index"]
            row = rows[index]
            reference = unicodedata.normalize("NFC", row["korean"])
            prediction = translator.vocab.decode_target(generated)
            ref_nfd, pred_nfd = unicodedata.normalize("NFD", reference), unicodedata.normalize("NFD", prediction)
            records.append({"index": index, "id": row.get("id", index),
                "document_id": row.get("document_id", ""), "group": row.get("group", ""),
                "category": row.get("category", ""), "category_code": row.get("category_code", ""),
                "braille": row["braille"], "reference": reference, "prediction": prediction,
                "exact_match": reference == prediction, "character_errors": edit_distance(reference, prediction),
                "reference_characters": len(reference), "nfd_character_errors": edit_distance(ref_nfd, pred_nfd),
                "reference_nfd_characters": len(ref_nfd), "ended_with_eos": has_eos,
                "source_tokens": len(item["tokens"]), "output_tokens": sum(t not in (PAD, EOS) for t in generated),
                "unknown_source_tokens": item["tokens"].count(UNK),
                "unknown_reference_tokens": translator.vocab.encode_target(reference).count(UNK),
                "unknown_generated_tokens": generated.count(UNK),
                "uncombined_jamo_characters": uncombined_jamo_count(prediction),
                "input_warnings": " | ".join(item["warnings"])})
        completed = min(start + args.batch_size, len(encoded))
        if (start // args.batch_size) % 10 == 0 or completed == len(encoded):
            elapsed = time.perf_counter() - started
            print(json.dumps({"event": "evaluation_progress", "examples": completed,
                "total": len(encoded), "seconds": round(elapsed, 2),
                "eta_seconds": round(elapsed / completed * (len(encoded) - completed), 2)}, ensure_ascii=False), flush=True)
    if translator.device.type == "cuda":
        torch.cuda.synchronize(translator.device)
    elapsed = time.perf_counter() - started
    if sha256_file(data_path) != data_hash or sha256_file(args.checkpoint / "best.pt") != translator.weights_sha256:
        raise RuntimeError("평가 중 모델 또는 데이터 파일이 바뀌었습니다. 결과를 같은 실험의 점수로 저장하지 않습니다.")
    if sha256_file(args.data_manifest) != manifest_evidence["data_manifest_sha256"]:
        raise RuntimeError("평가 중 전처리 manifest가 바뀌었습니다. 결과를 저장하지 않습니다.")
    records.sort(key=lambda row: row["index"])
    grouped = defaultdict(list)
    for record in records:
        grouped[record["category_code"]].append(record)
    metrics = {"schema_version": 1, "split": args.split, "full_split_examples": full_count,
        "evaluated_all_rows": len(rows) == full_count, "filtered_examples": 0,
        "normalization": "NFC output/reference; NFD auxiliary CER; spaces retained",
        "generation": "autoregressive greedy; no reference tokens supplied",
        **aggregate(records), "by_category": {key: aggregate(value) for key, value in grouped.items()},
        "checkpoint": str(args.checkpoint.resolve()), "weights_sha256": translator.weights_sha256,
        "data_path": str(data_path), "data_sha256": data_hash,
        **manifest_evidence,
        "config_sha256": sha256_file(args.checkpoint / "config.json"),
        "vocab_sha256": sha256_file(args.checkpoint / "vocab.json"),
        "torch_version": str(torch.__version__), "device": str(translator.device),
        "installed_cuda_runtime": torch.version.cuda, "cuda_used": translator.device.type == "cuda",
        "amp": translator.device.type == "cuda", "batch_size": args.batch_size,
        "num_beams": 1, "max_new_tokens": limit, "seconds": elapsed,
        "examples_per_second": len(rows) / elapsed,
        "gpu_peak_allocated_mib": torch.cuda.max_memory_allocated(translator.device) / 2**20 if translator.device.type == "cuda" else 0,
        "edit_distance_implementation": DISTANCE_IMPLEMENTATION,
        "limitations": ["CER includes spaces, numbers and punctuation; it can exceed 1.",
            "Uncombined jamo are valid Unicode; the count is a potential composition-error indicator.",
            "Reference OOV characters cannot be emitted directly by the train-only target vocabulary.",
            "Teacher-forced validation loss and autoregressive test quality are different measurements."]}
    with (output_dir / "predictions.tsv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(records)
    (output_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"event": "evaluation_complete", **{key: metrics[key] for key in (
        "examples", "CER", "NFD_CER", "exact_match_rate", "ended_with_eos_rate", "seconds")},
        "metrics_path": str((output_dir / "metrics.json").resolve())}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
