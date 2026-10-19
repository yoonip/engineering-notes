"""Reproducible 8x8 MNIST MLP training and conductance export.

Requires numpy and Pillow. This is software training, not SPICE simulation.
Run from any working directory; outputs stay beside this script.
"""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import platform
import struct
import time
import urllib.request
import numpy as np
from PIL import Image, __version__ as pillow_version

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESOURCES = {
    "train-images-idx3-ubyte.gz": "f68b3c2dcbeaaa9fbdd348bbdeb94873",
    "train-labels-idx1-ubyte.gz": "d53e105ee54ea40749a09fcbcd1e9432",
    "t10k-images-idx3-ubyte.gz": "9fb629c4189551a2d022fa330f9573f3",
    "t10k-labels-idx1-ubyte.gz": "ec29112dd5afa0611ce80d1b7f02629c",
}
BASE = "https://ossci-datasets.s3.amazonaws.com/mnist/"

def get_data():
    DATA.mkdir(exist_ok=True)
    manifest = {}
    for name, expected in RESOURCES.items():
        p = DATA / name
        if not p.exists():
            print("Downloading", name, flush=True)
            with urllib.request.urlopen(BASE + name, timeout=60) as source:
                p.write_bytes(source.read())
        blob = p.read_bytes()
        if hashlib.md5(blob).hexdigest() != expected:
            raise ValueError("MNIST checksum mismatch: " + str(p))
        manifest[name] = {"md5": expected, "sha256": hashlib.sha256(blob).hexdigest(), "url": BASE + name}
    return manifest

def read_idx(name):
    blob = gzip.decompress((DATA / name).read_bytes())
    magic, n = struct.unpack(">II", blob[:8])
    if magic == 2051:
        rows, cols = struct.unpack(">II", blob[8:16])
        return np.frombuffer(blob, dtype=np.uint8, offset=16).reshape(n, rows, cols)
    if magic == 2049:
        return np.frombuffer(blob, dtype=np.uint8, offset=8).copy()
    raise ValueError("Unexpected IDX magic")

def downsample(images):
    return np.stack([np.asarray(Image.fromarray(im).resize((8, 8), Image.Resampling.BOX)) for im in images]).reshape(-1, 64).astype(np.float32) / 255.0

def logits(x, params):
    w1, b1, w2, b2 = params
    return np.maximum(x @ w1 + b1, 0) @ w2 + b2

def accuracy(x, y, params):
    return float(np.mean(logits(x, params).argmax(axis=1) == y))

def quantize(w, levels):
    # Split-magnitude quantization: exact zero, +/- k*wmax/(levels-1).
    wmax = float(np.max(np.abs(w)))
    k = np.floor(np.abs(w.astype(np.float64)) / wmax * (levels - 1) + 0.5)
    return np.sign(w) * k * wmax / (levels - 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20261011)
    args = parser.parse_args()
    start = time.perf_counter()
    manifest = get_data()
    raw_train = read_idx("train-images-idx3-ubyte.gz")
    raw_test = read_idx("t10k-images-idx3-ubyte.gz")
    xall, xtest = downsample(raw_train), downsample(raw_test)
    yall, ytest = read_idx("train-labels-idx1-ubyte.gz"), read_idx("t10k-labels-idx1-ubyte.gz")
    x, y, xv, yv = xall[:50000], yall[:50000], xall[50000:], yall[50000:]
    rng = np.random.default_rng(args.seed)
    params = [
        (rng.standard_normal((64, 50)) * np.sqrt(2 / 64)).astype(np.float32),
        np.zeros(50, np.float32),
        (rng.standard_normal((50, 10)) * np.sqrt(2 / 50)).astype(np.float32),
        np.zeros(10, np.float32),
    ]
    m, v = [np.zeros_like(p) for p in params], [np.zeros_like(p) for p in params]
    history, best, best_val, step = [], None, -1.0, 0
    for epoch in range(args.epochs):
        order = rng.permutation(len(x))
        total_loss = 0.0
        for offset in range(0, len(x), 256):
            idx = order[offset:offset + 256]
            xb, yb = x[idx], y[idx]
            w1, b1, w2, b2 = params
            z1 = xb @ w1 + b1
            h = np.maximum(z1, 0)
            z = h @ w2 + b2
            expz = np.exp(z - z.max(axis=1, keepdims=True))
            p = expz / expz.sum(axis=1, keepdims=True)
            total_loss += float(-np.log(np.maximum(p[np.arange(len(idx)), yb], 1e-30)).sum())
            p[np.arange(len(idx)), yb] -= 1
            dz = p / len(idx)
            dh = (dz @ w2.T) * (z1 > 0)
            grads = [xb.T @ dh, dh.sum(axis=0), h.T @ dz, dz.sum(axis=0)]
            step += 1
            for j, grad in enumerate(grads):
                m[j] = 0.9 * m[j] + 0.1 * grad
                v[j] = 0.999 * v[j] + 0.001 * grad * grad
                params[j] -= 0.003 * (m[j] / (1 - 0.9 ** step)) / (np.sqrt(v[j] / (1 - 0.999 ** step)) + 1e-8)
        val = accuracy(xv, yv, params)
        history.append({"epoch": epoch + 1, "loss": total_loss / len(x), "validation_accuracy": val})
        if val > best_val:
            best_val, best, best_epoch = val, [p.copy() for p in params], epoch + 1
        print(f"epoch={epoch+1:02d} loss={total_loss/len(x):.6f} validation={val:.4%}", flush=True)
    w1, b1, w2, b2 = best
    np.savez(ROOT / "model.npz", w1=w1, b1=b1, w2=w2, b2=b2)
    np.savez(ROOT / "inputs.npz", x_test=xtest, y_test=ytest, x_validation=xv, y_validation=yv)
    curves = []
    for levels in (6, 16, 64, 256):
        quant_params = [quantize(w1, levels), b1, quantize(w2, levels), b2]
        curves.append({"states_per_device": levels, "validation_accuracy": accuracy(xv, yv, quant_params), "test_accuracy": accuracy(xtest, ytest, quant_params)})
    # Fixed sample rule, independent of prediction. No selection for a successful result.
    index5 = int(np.flatnonzero(ytest == 5)[0])
    for index in [index5] + [int(np.flatnonzero(ytest == c)[0]) for c in range(10) if c != 5]:
        Image.fromarray(raw_test[index]).resize((224, 224), Image.Resampling.NEAREST).save(ROOT / f"test_{index:05d}_28.png")
        Image.fromarray(np.rint(xtest[index].reshape(8, 8) * 255).astype(np.uint8)).resize((224, 224), Image.Resampling.NEAREST).save(ROOT / f"test_{index:05d}_8.png")
    stats = {
        "execution_kind": "Executed NumPy software training; SPICE status recorded separately",
        "date_timezone": "2026-10-11 Asia/Seoul", "python": platform.python_version(),
        "numpy": np.__version__, "pillow": pillow_version, "seed": args.seed,
        "architecture": "64-50-10 MLP, ReLU hidden, linear logits, biases enabled",
        "resize": "Pillow BOX, 28x28 uint8 to 8x8 uint8; divide by 255; flatten row-major",
        "train_count": 50000, "validation_count": 10000, "test_count": 10000,
        "optimizer": "Adam lr=0.003 beta1=0.9 beta2=0.999 eps=1e-8 batch=256",
        "epochs": args.epochs, "selected_epoch": best_epoch, "validation_accuracy": best_val,
        "software_test_accuracy": accuracy(xtest, ytest, best),
        "quantization": curves, "history": history, "dataset": manifest,
        "sample_rule": "first test sample whose true label is 5; no prediction filtering",
        "sample_index": index5, "sample_true_label": int(ytest[index5]),
        "sample_logits": logits(xtest[index5:index5+1], best)[0].astype(float).tolist(),
        "sample_prediction": int(logits(xtest[index5:index5+1], best)[0].argmax()),
        "duration_seconds": time.perf_counter() - start,
    }
    (ROOT / "training_results.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: stats[k] for k in ["selected_epoch", "software_test_accuracy", "sample_index", "sample_prediction", "duration_seconds"]}), flush=True)

if __name__ == "__main__":
    main()
