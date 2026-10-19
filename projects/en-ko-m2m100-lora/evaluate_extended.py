"""같은 그룹 시험 자료에서 기본 모델과 새 어댑터를 평가합니다.

검증 loss로 어댑터를 선택한 뒤에만 실행하세요. 시험 점수를 보고 epoch나
학습률을 다시 선택하면 시험 자료를 검증 자료처럼 쓰게 됩니다.
출력에 데이터/가중치 SHA-256, 생성 설정, 지표 서명, 각 번역문을 저장합니다.
"""
from pathlib import Path
import argparse
import csv
import gc
import hashlib
import json
import os
import time
from importlib.metadata import version

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("HF_HOME", str(ROOT / ".cache/huggingface"))
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch
import sacrebleu
from peft import PeftModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer



def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for data in iter(lambda: handle.read(1048576), b""):
            digest.update(data)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--data-dir", type=Path, help="Moved local splits; content hash must still match")
    args = parser.parse_args()
    run = args.run_dir.resolve()
    experiment = json.loads((run / "experiment.json").read_text(encoding="utf-8"))
    if experiment["status"] != "completed":
        raise RuntimeError("학습이 완료된 실험만 평가합니다.")
    if args.batch_size < 1:
        parser.error("batch-size must be positive")
    data = (args.data_dir or Path(experiment["data_path"])) / "test.tsv"
    if sha256(data) != experiment["data_sha256"]["test.tsv"]:
        raise RuntimeError("실험 이후 시험 데이터가 바뀌었습니다. 동일 자료 평가를 중단합니다.")
    if sha256(run / "adapter/adapter_model.safetensors") != experiment["adapter_sha256"]:
        raise RuntimeError("실험 이후 최적 어댑터 파일이 바뀌었습니다. 평가를 중단합니다.")
    with data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    revision = experiment.get("base_model_commit")
    tokenizer = AutoTokenizer.from_pretrained(experiment["base_model"], revision=revision, src_lang="en", tgt_lang="ko", local_files_only=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(experiment["base_model"], revision=revision, dtype=dtype, local_files_only=True).to(device).eval()
    generation = {"num_beams": 4, "max_new_tokens": 128, "max_input_tokens": 256, "forced_language": "ko"}

    def predict(texts, label):
        predictions = []
        capped = 0
        started = time.perf_counter()
        batch_size = args.batch_size if device == "cuda" else min(args.batch_size, 2)
        for start in range(0, len(texts), batch_size):
            batch = tokenizer(texts[start:start + batch_size], return_tensors="pt", padding=True, truncation=False)
            if batch["input_ids"].shape[1] > generation["max_input_tokens"]:
                raise RuntimeError("시험 입력이 최대 길이를 초과합니다. 조용히 자르지 않습니다.")
            with torch.inference_mode(), torch.autocast(device_type=device, dtype=torch.float16, enabled=device == "cuda"):
                ids = model.generate(**batch.to(device), forced_bos_token_id=tokenizer.get_lang_id("ko"), max_new_tokens=128, num_beams=4)
            for seq in ids:
                non_pad = seq[seq.ne(tokenizer.pad_token_id)]
                capped += int(len(non_pad) > 0 and int(non_pad[-1]) != tokenizer.eos_token_id)
            predictions.extend(tokenizer.batch_decode(ids, skip_special_tokens=True))
            if start % (batch_size * 20) == 0 or start + batch_size >= len(texts):
                print(f"{label}: {min(start + batch_size, len(texts))}/{len(texts)}", flush=True)
        return predictions, {"seconds": round(time.perf_counter() - started, 3), "output_cap_count": capped}

    out = run / "evaluation"
    out.mkdir(exist_ok=True)
    predictions = {}
    result = {
        "base_model": experiment["base_model"],
        "base_model_commit": experiment["base_model_commit"],
        "adapter_sha256": sha256(run / "adapter/adapter_model.safetensors"),
        "data_sha256": sha256(data), "examples": len(rows),
        "best_epoch": experiment["best_epoch"], "generation": generation,
        "device": device, "dtype": str(dtype), "batch_size": args.batch_size if device == "cuda" else min(args.batch_size, 2),
        "versions": {name: version(name) for name in ("torch", "transformers", "peft", "sacrebleu")},
        "limits": "Tatoeba short sentences; no exact current-finetuning split overlap. Unknown original pretraining overlap. Single reference. Not a general professional-translation benchmark.",
    }
    for name in ("base", "best"):
        if name == "best":
            model = PeftModel.from_pretrained(model, str(run / "adapter"), local_files_only=True).to(device).eval()
        model.config.use_cache = True
        predictions[name], runtime = predict([r["source"] for r in rows], name)
        bleu = sacrebleu.metrics.BLEU(tokenize="13a")
        chrf = sacrebleu.metrics.CHRF()
        refs = [[r["target"] for r in rows]]
        result[name] = {
            "BLEU": bleu.corpus_score(predictions[name], refs).score,
            "chrF": chrf.corpus_score(predictions[name], refs).score,
            "BLEU_signature": str(bleu.get_signature()), "chrF_signature": str(chrf.get_signature()),
            **runtime,
        }
        (out / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    result["delta"] = {metric: result["best"][metric] - result["base"][metric] for metric in ("BLEU", "chrF")}
    (out / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    with (out / "predictions.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[*rows[0], "base_prediction", "best_prediction"], delimiter="\t")
        writer.writeheader()
        for i, row in enumerate(rows):
            writer.writerow({**row, "base_prediction": predictions["base"][i], "best_prediction": predictions["best"][i]})
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    del model
    gc.collect()
    if device == "cuda":
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
