"""학습된 숫자를 꺼내 직접 읽을 수 있게 내보냅니다. 모델을 다시 학습하지 않습니다.

  python export_weights.py --checkpoint checkpoints/실험 --output-dir exports/my_weights

weights_state_dict.pt: 모든 학습 가중치의 이름→Tensor 대응표(실제 재사용 가능).
weights_sample.csv: 각 Tensor의 shape, 개수, 평균/표준편차/범위와 앞의 몇 값.
config.json/vocab.json: 같은 구조와 토큰 번호로 다시 불러오는 데 필요한 설명서.
best.pt: inference.py가 바로 읽을 수 있는 동일 가중치 파일.

Tensor는 다차원 숫자 배열입니다. 예를 들어 embedding.weight의 한 행은 한 문자에
대응하는 D개의 학습 숫자입니다. 그 숫자 하나에 사람이 읽을 수 있는 한국어 의미가
따로 붙는 것은 아닙니다. 수백만 값을 CSV로 전부 펴면 읽기 어렵고 파일만 커지므로
전체는 .pt에, 사람이 살펴볼 표본은 CSV에 담습니다. CSV만으로 모델 복원은 안 됩니다.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path

import torch

from model import sha256_file


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--sample-per-tensor", type=int, default=8)
    args = parser.parse_args()
    if args.sample_per_tensor < 1 or args.sample_per_tensor > 100:
        raise ValueError("sample-per-tensor는 1..100 범위입니다.")
    checkpoint = args.checkpoint.resolve()
    output_dir = (args.output_dir or checkpoint / ("export_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))).resolve()
    if output_dir == checkpoint or (output_dir.exists() and any(output_dir.iterdir())):
        raise ValueError("원본 모델을 덮지 않도록 비어 있는 새 출력 폴더를 지정하세요.")
    output_dir.mkdir(parents=True, exist_ok=True)
    weights_path = checkpoint / "best.pt"
    # 학습이 계속되는 동안 best가 교체될 수도 있으므로 한 번 복사한 snapshot에서만
    # CSV, 별칭 .pt, hash를 만듭니다. 서로 다른 epoch의 파일/표를 섞지 않습니다.
    snapshot_path = output_dir / "best.pt"
    shutil.copy2(weights_path, snapshot_path)
    snapshot_hash = sha256_file(snapshot_path)
    for name in ("config.json", "vocab.json"):
        shutil.copy2(checkpoint / name, output_dir / name)
    config = json.loads((output_dir / "config.json").read_text(encoding="utf-8"))
    if sha256_file(output_dir / "vocab.json") != config["data"]["vocab_sha256"]:
        raise ValueError("학습 당시 vocab 파일과 다릅니다. 올바른 묶음에서 내보내세요.")
    weights = torch.load(snapshot_path, map_location="cpu", weights_only=True)
    if not isinstance(weights, dict) or not all(isinstance(key, str) and isinstance(value, torch.Tensor) for key, value in weights.items()):
        raise ValueError("best.pt가 순수 state_dict 형식이 아닙니다.")
    records = []
    for name, tensor in weights.items():
        flat = tensor.detach().float().reshape(-1)
        records.append({"name": name, "shape": json.dumps(list(tensor.shape)),
            "dtype": str(tensor.dtype), "number_of_values": tensor.numel(),
            "mean": float(flat.mean()), "std_population": float(flat.std(unbiased=False)),
            "minimum": float(flat.min()), "maximum": float(flat.max()),
            "first_values": json.dumps(flat[:args.sample_per_tensor].tolist())})
    # best.pt 자체가 raw state_dict입니다. copy는 값과 파일 hash까지 그대로 유지합니다.
    shutil.copy2(snapshot_path, output_dir / "weights_state_dict.pt")
    with (output_dir / "weights_sample.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    metadata = {"source_checkpoint": str(checkpoint), "output_directory": str(output_dir),
        "sha256": snapshot_hash, "tensor_count": len(records),
        "total_values": sum(tensor.numel() for tensor in weights.values()),
        "file_bytes": snapshot_path.stat().st_size, "torch_version": str(torch.__version__),
        "format": "raw state_dict; no optimizer; no pretrained base dependency",
        "csv_is_sample_only": True}
    (output_dir / "export_metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "README.txt").write_text(
        "best.pt와 weights_state_dict.pt는 동일한 전체 학습 가중치입니다.\n"
        "weights_sample.csv는 설명용 표본이며 이 CSV만으로 추론할 수 없습니다.\n"
        "inference.py --checkpoint 이_폴더 --text 점자 --device cpu 로 재사용합니다.\n"
        "배포에는 Python/PyTorch 실행환경 또는 이를 포함한 앱이 별도로 필요합니다.\n",
        encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
