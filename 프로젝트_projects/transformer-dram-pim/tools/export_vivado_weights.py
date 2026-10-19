"""학습한 Q8.8 checkpoint를 Vivado $readmemh 형식으로 내보낸다."""

from pathlib import Path
import argparse
import json
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from model.gpt_q88 import load_checkpoint, write_mem_files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("output/tiny_gpt_full_ops_qat/tiny_gpt_qat_q88.json"),
    )
    parser.add_argument("--output", type=Path, default=Path("build/vivado_weights"))
    args = parser.parse_args()

    model = load_checkpoint(args.checkpoint)
    write_mem_files(model, args.output)

    # 이 top은 full-ops checkpoint 한 종류를 대상으로 하므로, 예상한 구조와
    # 다른 가중치 파일을 조용히 Vivado에 넘기지 않도록 파일 개수와 단어 수를 확인한다.
    config = model["config"]
    expected = {
        "token_embedding.mem": config["vocab_size"] * config["d_model"],
        "position_embedding.mem": config["context_length"] * config["d_model"],
        "lm_head.mem": config["d_model"] * config["vocab_size"],
        "lm_bias.mem": config["vocab_size"],
    }
    d_model = config["d_model"]
    d_ff = config["d_ff"]
    layer_words = {
        "wq": d_model * d_model,
        "wk": d_model * d_model,
        "wv": d_model * d_model,
        "wo": d_model * d_model,
        "w1": d_model * d_ff,
        "w2": d_ff * d_model,
        "bq": d_model,
        "bk": d_model,
        "bv": d_model,
        "bo": d_model,
        "b1": d_ff,
        "b2": d_model,
        "ln1_gamma": d_model,
        "ln1_beta": d_model,
        "ln2_gamma": d_model,
        "ln2_beta": d_model,
    }
    for layer_index in range(config["layers"]):
        for tensor_name, word_count in layer_words.items():
            expected[f"layer_{layer_index}_{tensor_name}.mem"] = word_count

    problems = []
    for filename, expected_words in expected.items():
        path = args.output / filename
        if not path.is_file():
            problems.append(f"누락 파일: {path}")
            continue
        actual_words = sum(1 for line in path.open(encoding="ascii") if line.strip())
        if actual_words != expected_words:
            problems.append(
                f"{filename}: {actual_words} words (expected {expected_words})"
            )
    if problems:
        raise SystemExit("\n".join(problems))

    manifest = {
        "checkpoint": str(args.checkpoint.resolve()),
        "config": config,
        "q_format": model.get("q_format", config.get("q_format", "signed Q8.8, 16-bit")),
        "files": {name: words for name, words in expected.items()},
    }
    (args.output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"exported {len(expected)} memory files to {args.output.resolve()}")
    print(json.dumps(config, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
