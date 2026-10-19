"""GPU가 없는 PC용 영한 번역기. 학습된 LoRA를 CPU에서만 추론합니다.

python cpu_app.py --checkpoint "학습폴더/adapter" --check "Hello."
선택 옵션: --quantization int8 (Linear 계층의 동적 양자화), --threads 4
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk

BASE_MODEL = "facebook/m2m100_418M"
MAX_INPUT_TOKENS, MAX_NEW_TOKENS = 256, 128


def find_root() -> Path:
    return Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent


class CPUTranslator:
    def __init__(self, checkpoint: Path, base_model: str, quantization="none", threads=4, num_beams=4):
        self.checkpoint, self.base_model = checkpoint, base_model
        self.quantization, self.threads, self.num_beams = quantization, threads, num_beams
        self.quantized_layers, self.quantized_engine = 0, None
        self.adapter_sha256 = None
        self.base_revision = "55c2e61bbf05dfb8d7abccdc3fae6fc8512fd636"

    def load(self, progress=lambda text: None) -> str:
        if not (self.checkpoint / "adapter_config.json").is_file() or not any(
            (self.checkpoint / name).is_file() for name in ("adapter_model.safetensors", "adapter_model.bin")
        ):
            raise FileNotFoundError(f"학습된 어댑터 파일을 찾을 수 없습니다: {self.checkpoint}")
        weights = next(self.checkpoint / name for name in ("adapter_model.safetensors", "adapter_model.bin")
                       if (self.checkpoint / name).is_file())
        digest = hashlib.sha256()
        with weights.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        self.adapter_sha256 = digest.hexdigest()
        progress("1/3 · CPU 번역 엔진을 준비하고 있습니다…")
        import torch
        from peft import PeftModel
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.torch = torch
        torch.set_num_threads(self.threads)
        progress("2/3 · 기본 모델과 학습한 가중치를 읽고 있습니다…")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model, src_lang="en", tgt_lang="ko", local_files_only=True, revision=self.base_revision
        )
        base = AutoModelForSeq2SeqLM.from_pretrained(
            self.base_model, dtype=torch.float32, local_files_only=True, revision=self.base_revision
        ).cpu().eval()
        # LoRA를 먼저 적용하고 병합해야 양자화에도 내가 학습한 변화가 포함됩니다.
        adapted = PeftModel.from_pretrained(base, str(self.checkpoint)).cpu().eval()
        self.model = adapted.merge_and_unload(safe_merge=True).eval()
        progress("3/3 · CPU 추론을 준비하고 있습니다…")
        if self.quantization == "int8":
            engines = torch.backends.quantized.supported_engines
            engine = next((name for name in ("x86", "onednn", "fbgemm") if name in engines), None)
            if engine is None:
                raise RuntimeError("이 CPU 런타임은 INT8을 지원하지 않습니다. START_STANDARD.cmd로 실행하세요.")
            torch.backends.quantized.engine = engine
            # 공식 torch 2.14 API: Linear만 동적 qint8로 변환. 원본 파일은 수정하지 않습니다.
            self.model = torch.ao.quantization.quantize_dynamic(
                self.model, {torch.nn.Linear}, dtype=torch.qint8, inplace=True
            ).eval()
            self.quantized_engine = engine
            self.quantized_layers = sum(
                isinstance(layer, torch.ao.nn.quantized.dynamic.Linear) for layer in self.model.modules()
            )
            if self.quantized_layers == 0:
                raise RuntimeError("INT8 변환된 Linear 계층이 없어 실행을 중단합니다.")
        mode = "INT8" if self.quantization == "int8" else "FP32"
        return f"CPU 전용 · {mode} · {self.threads} 스레드 · 학습 가중치 적용 완료"

    def translate(self, text: str) -> dict:
        text = text.strip()
        if not text:
            raise ValueError("영어 문장을 입력하세요.")
        if len(text) > 6000:
            raise ValueError("입력이 너무 깁니다. 몇 문장씩 나누어 입력하세요.")
        tokens = self.tokenizer(text, return_tensors="pt", truncation=False)
        count = tokens["input_ids"].shape[1]
        if count > MAX_INPUT_TOKENS:
            raise ValueError(f"현재 {count} 토큰입니다. {MAX_INPUT_TOKENS} 토큰 이하로 문장을 나누세요.")
        start = time.perf_counter()
        with self.torch.inference_mode():
            output = self.model.generate(
                **tokens, forced_bos_token_id=self.tokenizer.get_lang_id("ko"),
                max_new_tokens=MAX_NEW_TOKENS, num_beams=self.num_beams,
            )
        if output.shape[1] >= MAX_NEW_TOKENS + 1 and output[0, -1].item() != self.tokenizer.eos_token_id:
            raise ValueError("번역 출력이 128 토큰 제한에 도달했습니다. 원문을 더 짧게 나누세요.")
        return {"translation": self.tokenizer.decode(output[0], skip_special_tokens=True),
                "seconds": round(time.perf_counter() - start, 3), "input_tokens": count}


class CPUApp:
    def __init__(self, root, translator):
        self.root, self.translator, self.ready = root, translator, False
        self.events = queue.Queue()
        root.title("영한 번역기 · GPU 없이 실행")
        root.geometry("900x690")
        root.minsize(750, 600)
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="영어 → 한국어", font=("Malgun Gothic", 21, "bold")).pack(anchor="w")
        ttk.Label(frame, text="CPU로 번역합니다. 인터넷과 GPU가 필요하지 않습니다.").pack(anchor="w", pady=5)
        ttk.Label(frame, text="기본 모델: facebook/m2m100_418M + 직접 학습한 LoRA", wraplength=830).pack(anchor="w")
        ttk.Label(frame, text=f"학습 가중치: {translator.checkpoint}", wraplength=830).pack(anchor="w", pady=5)
        ttk.Label(frame, text="영어 입력 · Ctrl+Enter로 번역").pack(anchor="w", pady=(10, 0))
        self.source = tk.Text(frame, height=7, wrap="word", font=("Malgun Gothic", 12))
        self.source.pack(fill="both", expand=True, pady=5)
        self.button = ttk.Button(frame, text="번역하기", state="disabled", command=self.start_translation)
        self.button.pack(anchor="e", pady=8)
        ttk.Label(frame, text="한국어 번역 결과").pack(anchor="w")
        self.output = tk.Text(frame, height=7, wrap="word", font=("Malgun Gothic", 12), state="disabled")
        self.output.pack(fill="both", expand=True, pady=5)
        self.status = tk.StringVar(value="모델을 준비하고 있습니다. 처음 실행은 시간이 걸릴 수 있습니다…")
        ttk.Label(frame, textvariable=self.status, wraplength=830).pack(anchor="w", pady=8)
        root.bind("<Control-Return>", lambda _: self.start_translation())
        root.after(100, self.poll)
        self.run("loaded", translator.load, lambda text: self.events.put(("progress", text)))

    def run(self, event, function, *args):
        def worker():
            try:
                self.events.put((event, function(*args)))
            except Exception as error:
                self.events.put(("error", str(error)))
        threading.Thread(target=worker, daemon=True).start()

    def start_translation(self):
        if not self.ready or str(self.button["state"]) == "disabled":
            return
        self.button.configure(state="disabled")
        self.status.set("CPU로 번역 중입니다… 문장 길이와 PC 속도에 따라 시간이 걸립니다.")
        self.run("translated", self.translator.translate, self.source.get("1.0", "end"))

    def poll(self):
        try:
            while True:
                event, value = self.events.get_nowait()
                if event == "loaded":
                    self.ready, self.runtime_label = True, value
                    self.status.set(value)
                elif event == "translated":
                    self.output.configure(state="normal")
                    self.output.delete("1.0", "end")
                    self.output.insert("1.0", value["translation"])
                    self.output.configure(state="disabled")
                    self.status.set(f"완료 · {value['seconds']}초 · {self.runtime_label}")
                elif event == "progress":
                    self.status.set(value)
                    continue
                else:
                    self.status.set(f"오류: {value}")
                self.button.configure(state="normal" if self.ready else "disabled")
        except queue.Empty:
            pass
        self.root.after(100, self.poll)


def main():
    root = find_root()
    # 설치된 라이브러리에도 오프라인 실행을 명시합니다. 입력 문장을 외부로 보내지 않습니다.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ.setdefault("HF_HOME", str(root / ".cache/huggingface"))
    config_path = root / "cpu_app_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.is_file() else {}
    bundled = (root / "model/base").is_dir()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--base-model", default=str(root / "model/base") if bundled else BASE_MODEL)
    parser.add_argument("--base-revision", default="55c2e61bbf05dfb8d7abccdc3fae6fc8512fd636")
    parser.add_argument("--quantization", choices=("none", "int8"), default=config.get("quantization", "none"))
    parser.add_argument("--threads", type=int, default=config.get("threads", min(4, os.cpu_count() or 1)))
    parser.add_argument("--num-beams", type=int, default=config.get("num_beams", 4))
    parser.add_argument("--check", "--check-text", dest="check", metavar="ENGLISH")
    parser.add_argument("--check-output", type=Path)
    args = parser.parse_args()
    if args.threads < 1 or not 1 <= args.num_beams <= 8:
        parser.error("threads는 1 이상, num-beams는 1~8로 지정하세요.")
    if args.check_output is not None and args.check is None:
        parser.error("--check-output은 --check와 함께 사용하세요.")
    translator = CPUTranslator(args.checkpoint.resolve(), args.base_model, args.quantization, args.threads, args.num_beams)
    translator.base_revision = args.base_revision
    if args.check is not None:
        started = time.perf_counter()
        label = translator.load()
        result = {"runtime": label, "device": "cpu", "torch": translator.torch.__version__,
                  "cuda_runtime": translator.torch.version.cuda, "checkpoint": str(translator.checkpoint),
                  "adapter_sha256": translator.adapter_sha256,
                  "quantization": args.quantization, "quantized_linear_layers": translator.quantized_layers,
                  "quantized_engine": translator.quantized_engine,
                  "load_seconds": round(time.perf_counter() - started, 3), "input": args.check,
                  **translator.translate(args.check)}
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.check_output:
            args.check_output.parent.mkdir(parents=True, exist_ok=True)
            args.check_output.write_text(text, encoding="utf-8")
        if sys.stdout is not None:
            print(text)
    else:
        window = tk.Tk()
        CPUApp(window, translator)
        window.mainloop()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
