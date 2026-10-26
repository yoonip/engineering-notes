"""Small, offline numerical experiments. No released model weights are loaded."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
from pathlib import Path


def kv_bytes(layers, kv_heads, head_dim, tokens, batch=1, bytes_per_value=2):
    """Count the K and V arrays for full attention, excluding allocation overhead."""
    values = (layers, kv_heads, head_dim, tokens, batch, bytes_per_value)
    if any(value <= 0 for value in values):
        raise ValueError("All dimensions must be positive.")
    return 2 * layers * kv_heads * head_dim * tokens * batch * bytes_per_value


def memory_experiment():
    configurations = [
        {
            "id": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
            "layers": 28, "kv_heads": 2, "head_dim": 128,
            "parameters_approx": 1_500_000_000,
            "source": "https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B/raw/main/config.json",
        },
        {
            "id": "Qwen/Qwen3-0.6B",
            "layers": 28, "kv_heads": 8, "head_dim": 128,
            "parameters_approx": 600_000_000,
            "source": "https://huggingface.co/Qwen/Qwen3-0.6B/raw/main/config.json",
        },
    ]
    rows = []
    for config in configurations:
        for tokens in (4096, 16384, 32768):
            rows.append({
                "id": config["id"], "tokens": tokens,
                "weight_bf16_GiB_approx": round(config["parameters_approx"] * 2 / 2**30, 6),
                "weight_int4_GiB_ideal_approx": round(config["parameters_approx"] / 2 / 2**30, 6),
                "kv_bf16_GiB": round(kv_bytes(config["layers"], config["kv_heads"], config["head_dim"], tokens) / 2**30, 6),
            })
    return {"configuration_checked": "2026-10-19", "configurations": configurations, "rows": rows}


def recursive_state_experiment():
    """A scalar state schedule inspired by x/y/z iteration, not the TRM network."""
    x = 1.0
    rows = []
    for latent_gain in (0.5, 1.2):
        y, z = 0.0, 0.0
        for outer_step in range(1, 9):
            for _ in range(3):
                z = latent_gain * z + 0.25 * (x + y)
            y = 0.5 * y + 0.25 * z
            rows.append({
                "latent_gain": latent_gain, "outer_step": outer_step,
                "shared_scalar_coefficients": 4,
                "state_updates": outer_step * 4,
                "y": round(y, 9), "z": round(z, 9),
            })
    return {"input_x": x, "inner_steps": 3, "rows": rows}


def softmax(logits):
    maximum = max(logits)
    values = [math.exp(value - maximum) for value in logits]
    total = sum(values)
    return [value / total for value in values]


def teacher(x):
    return softmax([-2 * x, 1.0, 2 * x])


def student(weights, x):
    return softmax([bias + slope * x for bias, slope in weights])


def train_student(inputs, soft_targets, steps=1200):
    weights = [[0.0, 0.0] for _ in range(3)]
    for _ in range(steps):
        gradient = [[0.0, 0.0] for _ in range(3)]
        for x in inputs:
            target = teacher(x)
            if not soft_targets:
                best = max(range(3), key=target.__getitem__)
                target = [float(index == best) for index in range(3)]
            prediction = student(weights, x)
            for index in range(3):
                error = prediction[index] - target[index]
                gradient[index][0] += error / len(inputs)
                gradient[index][1] += error * x / len(inputs)
        for index in range(3):
            for column in range(2):
                weights[index][column] -= 0.2 * gradient[index][column]
    return weights


def distillation_experiment():
    train_x = [-2.0, -1.0, -0.4, 0.0, 0.4, 1.0, 2.0]
    test_x = [-1.95 + index * 0.1 for index in range(40)]
    rows = []
    for use_soft in (False, True):
        weights = train_student(train_x, use_soft)
        divergences = []
        agreements = []
        for x in test_x:
            target = teacher(x)
            prediction = student(weights, x)
            divergences.append(sum(p * math.log(p / q) for p, q in zip(target, prediction)))
            agreements.append(max(range(3), key=target.__getitem__) == max(range(3), key=prediction.__getitem__))
        rows.append({
            "target": "teacher_probabilities" if use_soft else "teacher_argmax",
            "train_points": len(train_x), "held_out_points": len(test_x),
            "gradient_steps": 1200, "learning_rate": 0.2,
            "mean_KL_teacher_to_student": round(sum(divergences) / len(divergences), 9),
            "argmax_agreement": round(sum(agreements) / len(agreements), 6),
            "weights": [[round(value, 9) for value in row] for row in weights],
        })
    return {"seed": "deterministic; no random number generator", "rows": rows}


def uniform_quantize(values, bits):
    if bits < 2:
        raise ValueError("Use at least two bits.")
    low, high = min(values), max(values)
    if low == high:
        return values.copy()
    levels = 2**bits - 1
    scale = (high - low) / levels
    return [low + round((value - low) / scale) * scale for value in values]


def quantization_experiment():
    weights = [math.sin(index * 0.37) for index in range(64)]
    vector = [math.cos(index * 0.19) for index in range(64)]
    reference = sum(w * x for w, x in zip(weights, vector))
    rows = []
    for bits in (4, 8):
        reconstructed = uniform_quantize(weights, bits)
        output = sum(w * x for w, x in zip(reconstructed, vector))
        rows.append({
            "bits": bits, "ideal_payload_bytes": len(weights) * bits // 8,
            "max_weight_error": round(max(abs(a - b) for a, b in zip(weights, reconstructed)), 9),
            "dot_absolute_error": round(abs(output - reference), 9),
        })
    return {"values": 64, "reference_dot": round(reference, 9), "rows": rows}


def run():
    return {
        "scope": "Offline educational arithmetic, not inference or training of any released model",
        "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(), "platform": sys.platform},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "memory_estimates": memory_experiment(),
        "recursive_state": recursive_state_experiment(),
        "teacher_student": distillation_experiment(),
        "uniform_quantization": quantization_experiment(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(args.output)
