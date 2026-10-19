"""Explicit download of the pinned official base model; never runs on import."""
from pathlib import Path
import argparse
import json
import os

def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=root / "configs/train.json")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    os.environ.setdefault("HF_HOME", str(root / ".cache/huggingface"))
    from huggingface_hub import snapshot_download
    snapshot_download(repo_id=config["base_model"], revision=config["base_revision"],
                      allow_patterns=["config.json", "generation_config.json", "pytorch_model.bin", "vocab.json", "sentencepiece.bpe.model", "tokenizer_config.json", "special_tokens_map.json"])

if __name__ == "__main__":
    main()
