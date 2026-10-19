"""직접 학습한 가중치로 6점 점자를 한글로 바꾸는 CPU 앱.

python app.py --checkpoint "학습실험폴더"
python app.py --checkpoint "학습실험폴더" --text "⠁" --self-check result.json
점 번호: 왼쪽 위부터 1,2,3 / 오른쪽 위부터 4,5,6입니다.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
from pathlib import Path
import queue
import sys
import threading
import tkinter as tk
from tkinter import filedialog, font, ttk

MODEL_FILES = ("config.json", "vocab.json", "best.pt")
BRAILLE_FONT, KOREAN_FONT = "Segoe UI Symbol", "Malgun Gothic"


def application_dir():
    return Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent


def default_checkpoint():
    """외부 model이 있으면 우선 사용하고, onefile 내부 모델은 그다음에 찾습니다.

    PyInstaller onefile은 실행할 때 묶인 파일을 임시 _MEIPASS 폴더에 풉니다.
    외부 model이 불완전하면 오류로 알립니다. 내장 모델로 몰래 바꾸지 않습니다.
    """
    external = application_dir() / "model"
    if external.exists():
        return external
    embedded_root = getattr(sys, "_MEIPASS", None)
    if embedded_root is not None:
        embedded = Path(embedded_root) / "model"
        if embedded.exists():
            return embedded
    return None


def validate_model(path):
    missing = [name for name in MODEL_FILES if not (path / name).is_file()]
    if missing:
        raise FileNotFoundError("학습 폴더에 필요한 파일이 없습니다: " + ", ".join(missing))


def model_hashes(path):
    result = {}
    for name in MODEL_FILES:
        digest = hashlib.sha256()
        with (path / name).open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        result[name] = digest.hexdigest()
    return result


def validate_braille(text):
    if not text.strip():
        raise ValueError("점자 문장을 입력하세요.")
    if len(text) > 10000:
        raise ValueError("입력이 너무 깁니다. 문장 단위로 나누어 입력하세요.")
    bad = sorted({char for char in text if not ("\u2800" <= char <= "\u283f" or char.isspace())})
    if bad:
        details = ", ".join(f"{char!r}(U+{ord(char):04X})" for char in bad[:8])
        raise ValueError("6점 Unicode 점자와 공백만 입력할 수 있습니다: " + details)


class BrailleApp:
    def __init__(self, window, checkpoint=None):
        self.window, self.translator, self.busy = window, None, False
        self.events = queue.Queue()
        window.title("직접 학습한 역점역 · 점자 → 한글 · CPU")
        window.geometry("1020x830")
        window.minsize(870, 740)
        outer = ttk.Frame(window, padding=18)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="점자 → 한글", font=(KOREAN_FONT, 21, "bold")).pack(anchor="w")
        ttk.Label(outer, text="저장한 학습 가중치를 CPU에서 읽어 번역합니다. 인터넷·GPU가 필요하지 않습니다.").pack(anchor="w", pady=5)
        row = ttk.Frame(outer)
        row.pack(fill="x", pady=6)
        self.choose = ttk.Button(row, text="학습 가중치 폴더 선택", command=self.choose_model)
        self.choose.pack(side="left")
        self.path_label = tk.StringVar(value="config.json · vocab.json · best.pt가 있는 실험 폴더를 선택하세요.")
        ttk.Label(outer, textvariable=self.path_label, wraplength=950).pack(anchor="w", pady=5)

        keyboard = ttk.LabelFrame(outer, text="6점 키보드 · 왼쪽 1·2·3 / 오른쪽 4·5·6", padding=8)
        keyboard.pack(fill="x", pady=8)
        self.dots = {number: tk.BooleanVar(value=False) for number in range(1, 7)}
        for number in range(1, 7):
            # Unicode braille U+2800의 bit0..5가 점1..6에 정확하게 대응합니다.
            ttk.Checkbutton(keyboard, text=f"{number}점", variable=self.dots[number], command=self.preview).grid(
                row=(number - 1) % 3, column=0 if number <= 3 else 1, padx=14, pady=2)
        self.canvas = tk.Canvas(keyboard, width=75, height=95, highlightthickness=0, bg="white")
        self.canvas.grid(row=0, column=2, rowspan=3, padx=16)
        self.symbol = tk.StringVar()
        ttk.Label(keyboard, textvariable=self.symbol, font=(BRAILLE_FONT, 38)).grid(row=0, column=3, rowspan=2, padx=10)
        self.codepoint = tk.StringVar()
        ttk.Label(keyboard, textvariable=self.codepoint).grid(row=2, column=3)
        buttons = ttk.Frame(keyboard)
        buttons.grid(row=0, column=4, rowspan=3, padx=12)
        ttk.Button(buttons, text="선택한 점자 넣기", command=self.insert_cell).pack(fill="x", pady=2)
        ttk.Button(buttons, text="띄어쓰기", command=lambda: self.insert_text(" ")).pack(fill="x", pady=2)
        ttk.Button(buttons, text="줄바꿈", command=lambda: self.insert_text("\n")).pack(fill="x", pady=2)
        self.preview()

        ttk.Label(outer, text="Unicode 점자 입력 · 붙여넣기 가능 · Ctrl+Enter로 번역").pack(anchor="w")
        self.input = tk.Text(outer, height=5, font=(BRAILLE_FONT, 22), wrap="word", undo=True)
        self.input.pack(fill="both", expand=True, pady=6)
        line = ttk.Frame(outer)
        line.pack(fill="x", pady=5)
        ttk.Button(line, text="입력 지우기", command=lambda: self.input.delete("1.0", "end")).pack(side="left")
        self.translate_button = ttk.Button(line, text="학습한 가중치로 역점역", state="disabled", command=self.translate)
        self.translate_button.pack(side="right")
        ttk.Label(outer, text="한글 출력").pack(anchor="w")
        self.output = tk.Text(outer, height=5, font=(KOREAN_FONT, 14), wrap="word", state="disabled")
        self.output.pack(fill="both", expand=True, pady=6)
        self.status = tk.StringVar(value="학습 가중치 폴더를 선택하세요. 실제 추론 결과는 학습 자료와 문장 길이에 따라 달라집니다.")
        ttk.Label(outer, textvariable=self.status, wraplength=950).pack(anchor="w", pady=8)
        if BRAILLE_FONT not in set(font.families(window)):
            self.status.set("Segoe UI Symbol 글꼴이 없습니다. 점번호/그림으로 점자를 확인하고 해당 글꼴을 설치하세요.")
        window.bind("<Control-Return>", lambda _: self.translate())
        window.after(100, self.poll)
        if checkpoint:
            self.load_model(Path(checkpoint))

    def preview(self):
        code = 0x2800 | sum(1 << (n - 1) for n, selected in self.dots.items() if selected.get())
        self.symbol.set(chr(code))
        self.codepoint.set(f"U+{code:04X}")
        self.canvas.delete("all")
        for n in range(1, 7):
            x, y = (20 if n <= 3 else 52), 18 + ((n - 1) % 3) * 28
            self.canvas.create_oval(x-7, y-7, x+7, y+7, fill="#173657" if self.dots[n].get() else "#e3e8ef", outline="#7a8797")

    def insert_text(self, text):
        self.input.insert("insert", text)
        self.input.focus_set()

    def insert_cell(self):
        self.insert_text(self.symbol.get())

    def worker(self, event, function, *args):
        def run():
            try:
                self.events.put((event, function(*args)))
            except Exception as error:
                self.events.put(("error", str(error)))
        threading.Thread(target=run, daemon=True).start()

    def choose_model(self):
        selected = filedialog.askdirectory(title="config.json / vocab.json / best.pt가 있는 학습 폴더")
        if selected:
            self.load_model(Path(selected))

    def load_model(self, path):
        if self.busy:
            return
        self.busy = True
        self.translate_button.configure(state="disabled")
        self.choose.configure(state="disabled")
        self.translator = None
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")
        self.path_label.set(str(path.resolve()))
        self.status.set("선택한 학습 가중치를 CPU에 읽고 있습니다…")
        def load():
            validate_model(path)
            gc.collect()
            import torch
            torch.set_num_threads(min(4, os.cpu_count() or 1))
            from inference import BrailleTranslator
            return BrailleTranslator(path, device="cpu").load()
        self.worker("loaded", load)

    def translate(self):
        if self.busy or self.translator is None:
            return
        text = self.input.get("1.0", "end-1c")
        try:
            validate_braille(text)
        except ValueError as error:
            self.status.set(str(error))
            return
        self.busy = True
        self.translate_button.configure(state="disabled")
        self.choose.configure(state="disabled")
        self.status.set("CPU에서 학습한 가중치로 역점역하고 있습니다…")
        self.worker("translated", self.translator.translate, text)

    def poll(self):
        try:
            while True:
                event, value = self.events.get_nowait()
                if event == "loaded":
                    self.translator = value
                    self.status.set("준비 완료 · CPU · 선택한 config / vocab / best.pt 적용")
                elif event == "translated":
                    self.output.configure(state="normal")
                    self.output.delete("1.0", "end")
                    self.output.insert("1.0", value["translation"])
                    self.output.configure(state="disabled")
                    notes = " / ".join(map(str, value.get("warnings", [])))
                    self.status.set(f"완료 · CPU · {value.get('seconds', 0):.3f}초" + (" · " + notes if notes else ""))
                else:
                    self.status.set("오류: " + value)
                self.busy = False
                self.choose.configure(state="normal")
                self.translate_button.configure(state="normal" if self.translator else "disabled")
        except queue.Empty:
            pass
        self.window.after(100, self.poll)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, default=default_checkpoint())
    parser.add_argument("--text", "--check-text", dest="text")
    parser.add_argument("--self-check", "--check-output", dest="self_check", type=Path)
    args = parser.parse_args()
    if args.self_check:
        if args.checkpoint is None:
            parser.error("--self-check에는 --checkpoint, exe 옆 model 또는 exe에 묶인 모델이 필요합니다.")
        checkpoint = args.checkpoint.resolve()
        validate_model(checkpoint)
        before = model_hashes(checkpoint)
        import torch
        torch.set_num_threads(min(4, os.cpu_count() or 1))
        from inference import BrailleTranslator
        translator = BrailleTranslator(checkpoint, device="cpu").load()
        result = {"status": "loaded", "checkpoint": str(checkpoint), "model_sha256": before,
                  "torch": str(torch.__version__), "cuda_runtime": torch.version.cuda,
                  "device": "cpu", "inference_executed": args.text is not None,
                  "model_directory_files": sorted(p.name for p in checkpoint.iterdir() if p.is_file())}
        if args.text is not None:
            validate_braille(args.text)
            result["inference"] = translator.translate(args.text)
        if model_hashes(checkpoint) != before:
            raise RuntimeError("모델을 읽는 동안 파일이 바뀌어 검증 결과를 저장하지 않습니다.")
        args.self_check.parent.mkdir(parents=True, exist_ok=True)
        args.self_check.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        if sys.stdout is not None:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        root = tk.Tk()
        BrailleApp(root, args.checkpoint)
        root.mainloop()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
