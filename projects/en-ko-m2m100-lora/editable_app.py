"""직접 수정하는 영한 번역 앱: 저장한 LoRA 가중치를 읽어 로컬에서 추론합니다.

실행: python editable_app.py --checkpoint "내_실험_폴더/adapter"
창 없이 실행: python editable_app.py --checkpoint ".../adapter" --check "Hello."
입력/출력 UI는 TranslationApp, 모델 추론 코드는 Translator에서 수정하세요.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import queue
import sys
import threading
import tkinter as tk
from tkinter import ttk

BASE_MODEL = "facebook/m2m100_418M"
MAX_INPUT_TOKENS = 256  # 초과 입력은 조용히 자르지 않고 사용자에게 알립니다.
MAX_NEW_TOKENS = 128


def find_project_root() -> Path:
    return Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent


def validate_checkpoint(checkpoint: Path) -> dict:
    """학습 파일이 없으면 오류를 냅니다. 기본 모델로 대신 번역하지 않습니다."""
    config = checkpoint / "adapter_config.json"
    weights = [checkpoint / "adapter_model.safetensors", checkpoint / "adapter_model.bin"]
    if not config.is_file() or not any(path.is_file() for path in weights):
        raise FileNotFoundError(f"학습된 adapter_config.json과 adapter_model 파일이 필요합니다:\n{checkpoint}")
    return json.loads(config.read_text(encoding="utf-8"))


class Translator:
    """기본 모델 + 내가 저장한 LoRA 어댑터 = 실제 추론에 사용하는 모델."""
    def __init__(self, checkpoint: Path, base_model: str, device: str = "auto"):
        self.checkpoint, self.base_model, self.device = checkpoint, base_model, device
        self.base_revision = "55c2e61bbf05dfb8d7abccdc3fae6fc8512fd636"

    def load(self) -> str:
        validate_checkpoint(self.checkpoint)
        # 느린 import와 모델 로딩을 UI 작업 스레드에서 수행합니다.
        import torch
        from peft import PeftModel
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        self.torch = torch
        if self.device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.device == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA를 사용할 수 없습니다. --device cpu로 실행하거나 드라이버를 확인하세요.")
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model, src_lang="en", tgt_lang="ko", local_files_only=True, revision=self.base_revision
        )
        base = AutoModelForSeq2SeqLM.from_pretrained(
            self.base_model, dtype=dtype, local_files_only=True, revision=self.base_revision
        )
        self.model = PeftModel.from_pretrained(base, str(self.checkpoint)).to(self.device).eval()
        return torch.cuda.get_device_name(0) if self.device == "cuda" else "CPU (GPU보다 느릴 수 있습니다)"

    def translate(self, text: str) -> str:
        text = text.strip()
        if not text:
            raise ValueError("영어 문장을 입력하세요.")
        if len(text) > 6000:
            raise ValueError("입력이 너무 깁니다. 몇 문장씩 나누어 번역하세요.")
        inputs = self.tokenizer(text, return_tensors="pt", truncation=False)
        count = inputs["input_ids"].shape[1]
        if count > MAX_INPUT_TOKENS:
            raise ValueError(f"입력이 {count} 토큰입니다. {MAX_INPUT_TOKENS} 토큰 이하로 나누어 입력하세요.")
        inputs = inputs.to(self.device)
        with self.torch.inference_mode():
            output = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.get_lang_id("ko"),
                max_new_tokens=MAX_NEW_TOKENS,
                num_beams=4,  # 속도를 우선하면 1로 바꾸어 비교하세요.
            )
        if output.shape[1] >= MAX_NEW_TOKENS + 1 and output[0, -1].item() != self.tokenizer.eos_token_id:
            raise ValueError("번역 출력 길이 제한에 도달했습니다. 원문을 더 짧게 나누어 주세요.")
        return self.tokenizer.decode(output[0], skip_special_tokens=True)


class TranslationApp:
    """Tkinter 화면은 주 스레드에서만 변경하고, 결과는 queue로 받습니다."""
    def __init__(self, root: tk.Tk, translator: Translator):
        self.root, self.translator = root, translator
        self.events = queue.Queue()
        root.title("내가 학습한 영한 번역기")
        root.geometry("880x660")
        root.minsize(720, 580)
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="영어 → 한국어", font=("Malgun Gothic", 20, "bold")).pack(anchor="w")
        ttk.Label(frame, text=f"사용하는 학습 가중치: {translator.checkpoint}", wraplength=820).pack(anchor="w", pady=8)
        ttk.Label(frame, text="영어 입력 · Ctrl+Enter로 번역").pack(anchor="w")
        self.source = tk.Text(frame, height=7, wrap="word", font=("Malgun Gothic", 12))
        self.source.pack(fill="both", expand=True, pady=6)
        self.source.insert("1.0", "The weather is clear today.")
        self.button = ttk.Button(frame, text="번역하기", command=self.start_translation, state="disabled")
        self.button.pack(anchor="e", pady=8)
        ttk.Label(frame, text="한국어 번역 결과").pack(anchor="w")
        self.result = tk.Text(frame, height=7, wrap="word", font=("Malgun Gothic", 12), state="disabled")
        self.result.pack(fill="both", expand=True, pady=6)
        self.status = tk.StringVar(value="기본 모델과 선택한 학습 가중치를 읽는 중입니다…")
        ttk.Label(frame, textvariable=self.status, wraplength=820).pack(anchor="w", pady=8)
        self.ready = False
        root.bind("<Control-Return>", lambda _: self.start_translation())
        root.after(100, self.poll_events)
        self.run_worker("loaded", translator.load)

    def run_worker(self, event: str, function, *args):
        def work():
            try:
                self.events.put((event, function(*args)))
            except Exception as error:
                self.events.put(("error", str(error)))
        threading.Thread(target=work, daemon=True).start()

    def start_translation(self):
        if not self.ready or str(self.button["state"]) == "disabled":
            return
        self.button.configure(state="disabled")
        self.status.set("학습된 가중치로 번역 중입니다…")
        self.run_worker("translated", self.translator.translate, self.source.get("1.0", "end"))

    def poll_events(self):
        try:
            while True:
                event, value = self.events.get_nowait()
                if event == "loaded":
                    self.ready = True
                    self.device_name = value
                    self.status.set(f"준비 완료 · {value} · 선택한 LoRA 가중치 적용 완료")
                elif event == "translated":
                    self.result.configure(state="normal")
                    self.result.delete("1.0", "end")
                    self.result.insert("1.0", value)
                    self.result.configure(state="disabled")
                    self.status.set(f"번역 완료 · {self.device_name}")
                else:
                    self.status.set(f"오류: {value}")
                self.button.configure(state="normal" if self.ready else "disabled")
        except queue.Empty:
            pass
        self.root.after(100, self.poll_events)


def main():
    root = find_project_root()
    os.environ.setdefault("HF_HOME", str(root / ".cache/huggingface"))
    parser = argparse.ArgumentParser(description=__doc__)
    bundled = (root / "model" / "base").is_dir()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--base-model", default=str(root / "model/base") if bundled else BASE_MODEL)
    parser.add_argument("--base-revision", default="55c2e61bbf05dfb8d7abccdc3fae6fc8512fd636")
    parser.add_argument("--device", choices=("auto", "cuda", "cpu"), default="auto")
    parser.add_argument("--check", metavar="ENGLISH", help="GUI 없이 실제 가중치를 로딩하여 한 문장을 번역")
    parser.add_argument("--check-output", type=Path, help="--check의 결과를 JSON으로 저장 (windowed exe 확인용)")
    args = parser.parse_args()
    if args.check_output is not None and args.check is None:
        parser.error("--check-output은 --check와 함께 사용하세요.")
    translator = Translator(args.checkpoint.expanduser().resolve(), args.base_model, args.device)
    translator.base_revision = args.base_revision
    if args.check is not None:
        device = translator.load()
        result = json.dumps({"checkpoint": str(translator.checkpoint), "device": device,
                             "input": args.check, "translation": translator.translate(args.check)}, ensure_ascii=False)
        if args.check_output is not None:
            args.check_output.parent.mkdir(parents=True, exist_ok=True)
            args.check_output.write_text(result, encoding="utf-8")
        if sys.stdout is not None:
            print(result)
    else:
        window = tk.Tk()
        TranslationApp(window, translator)
        window.mainloop()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
