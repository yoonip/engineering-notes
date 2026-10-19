"""Train the small decoder-only Transformer and export its RTL weights.

This is an educational, deterministic NumPy implementation, not a PyTorch
checkpoint converter. It manually computes the forward pass, cross-entropy,
reverse-mode gradients, and Adam updates for a one-head Transformer with
V=13, D=8, FFN=16, and context length 8. Curated examples teach weather
responses conditioned on a forecast-bin token. The trained float arrays are rounded to signed Q8.8;
the Python Q8.8 forward pass checks the exact token sequences before export.

Python and NumPy are needed only to retrain. The exported SystemVerilog embeds
the integer parameters and performs inference without Python or PyTorch.
"""
from __future__ import annotations
import numpy as np
from pathlib import Path

V = 13
D = 8
F = 16
T = 8
EOS_ID = 11
SQRT_D = np.sqrt(D)
EPSILON = 4.0 / 256.0
SEQUENCES = [
    [1, 2, 4, 6, 7, 8, 9, 11],  # rain query, high forecast -> rain chance high
    [1, 2, 5, 6, 7, 8, 10, 11], # rain query, low forecast -> rain chance low
    [1, 3, 4, 12, 8, 10, 11],   # clear query, high rain chance -> clear chance low
    [1, 3, 5, 12, 8, 9, 11],    # clear query, low rain chance -> clear chance high
]


def softmax(x):
    x = x - np.max(x, axis=-1, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=-1, keepdims=True)


def layer_norm(x, gamma, beta):
    mean = np.mean(x, axis=-1, keepdims=True)
    centered = x - mean
    var = np.mean(centered * centered, axis=-1, keepdims=True)
    inv = 1.0 / np.sqrt(var + EPSILON)
    normalized = centered * inv
    return normalized * gamma + beta, (normalized, inv, gamma)


def layer_norm_backward(dy, cache):
    normalized, inv, gamma = cache
    dxhat = dy * gamma
    n = dxhat.shape[-1]
    dx = (inv / n) * (
        n * dxhat
        - np.sum(dxhat, axis=-1, keepdims=True)
        - normalized * np.sum(dxhat * normalized, axis=-1, keepdims=True)
    )
    return dx, np.sum(dy * normalized, axis=0), np.sum(dy, axis=0)


def init_params(rng):
    scale = 0.16
    p = {
        "emb": rng.normal(0, scale, (V, D)),
        "pos": rng.normal(0, scale, (T, D)),
        "g1": np.ones(D), "b1n": np.zeros(D),
        "g2": np.ones(D), "b2n": np.zeros(D),
        "g3": np.ones(D), "b3n": np.zeros(D),
        "wq": rng.normal(0, 0.20, (D, D)),
        "wk": rng.normal(0, 0.20, (D, D)),
        "wv": rng.normal(0, 0.20, (D, D)),
        "wo": rng.normal(0, 0.20, (D, D)),
        "w1": rng.normal(0, 0.20, (D, F)),
        "b1": np.zeros(F),
        "w2": rng.normal(0, 0.20, (F, D)),
        "b2": np.zeros(D),
        "lm": rng.normal(0, 0.20, (D, V)),
        "lmb": np.zeros(V),
    }
    return p


def forward(p, ids):
    """Float reference: logits for the next token at every prefix position."""
    n = len(ids)
    x = p["emb"][ids] + p["pos"][:n]
    n1, c1 = layer_norm(x, p["g1"], p["b1n"])
    q, k, v = n1 @ p["wq"], n1 @ p["wk"], n1 @ p["wv"]
    scores = q @ k.T / SQRT_D
    scores = np.where(np.triu(np.ones((n, n), dtype=bool), 1), -1e9, scores)
    attn = softmax(scores)
    ctx = attn @ v
    attn_out = ctx @ p["wo"]
    r1 = x + attn_out
    n2, c2 = layer_norm(r1, p["g2"], p["b2n"])
    pre = n2 @ p["w1"] + p["b1"]
    act = np.maximum(pre, 0)
    ffn = act @ p["w2"] + p["b2"]
    r2 = r1 + ffn
    n3, c3 = layer_norm(r2, p["g3"], p["b3n"])
    logits = n3 @ p["lm"] + p["lmb"]
    cache = (ids, x, c1, q, k, v, attn, ctx, c2, pre, act, c3, n3)
    return logits, cache


def loss_and_grad(p, seq):
    """Cross-entropy and manually derived gradients for one training sequence."""
    ids = np.asarray(seq[:-1], dtype=np.int64)
    target = np.asarray(seq[1:], dtype=np.int64)
    logits, c = forward(p, ids)
    probs = softmax(logits)
    # BOS, intent, and forecast-bin are input prompt tokens. Train only on the
    # response following that three-token prefix.
    answer_positions = np.arange(2, len(target))
    loss = -np.mean(np.log(probs[answer_positions, target[answer_positions]] + 1e-12))
    dlog = probs
    dlog[np.arange(len(target)), target] -= 1
    dlog[:2, :] = 0.0
    dlog /= len(answer_positions)

    (ids, x, c1, q, k, v, attn, ctx, c2, pre, act, c3, n3) = c
    g = {name: np.zeros_like(value) for name, value in p.items()}
    g["lm"] = n3.T @ dlog
    g["lmb"] = np.sum(dlog, axis=0)
    dn3 = dlog @ p["lm"].T
    dr2, g["g3"], g["b3n"] = layer_norm_backward(dn3, c3)

    # FFN and its residual path.
    dr1 = dr2.copy()
    g["w2"] = act.T @ dr2
    g["b2"] = np.sum(dr2, axis=0)
    dact = dr2 @ p["w2"].T
    dpre = dact * (pre > 0)
    g["w1"] = c2[0].T @ dpre
    g["b1"] = np.sum(dpre, axis=0)
    dn2 = dpre @ p["w1"].T
    dln2, g["g2"], g["b2n"] = layer_norm_backward(dn2, c2)
    dr1 += dln2

    # Attention residual, output projection, weighted values, softmax, Q/K/V.
    dattn_out = dr1
    g["wo"] = ctx.T @ dattn_out
    dctx = dattn_out @ p["wo"].T
    datt = dctx @ v.T
    dv = attn.T @ dctx
    ds = attn * (datt - np.sum(datt * attn, axis=-1, keepdims=True))
    ds[np.triu_indices(len(ids), 1)] = 0.0
    dq = ds @ k / SQRT_D
    dk = ds.T @ q / SQRT_D
    n1 = c1[0]
    g["wq"] = n1.T @ dq
    g["wk"] = n1.T @ dk
    g["wv"] = n1.T @ dv
    dn1 = dq @ p["wq"].T + dk @ p["wk"].T + dv @ p["wv"].T
    dx_attn, g["g1"], g["b1n"] = layer_norm_backward(dn1, c1)
    dx = dr1 + dx_attn

    # Embedding and position tables receive the residual-path gradients.
    g["pos"][:len(ids)] += dx
    for pos, tok in enumerate(ids):
        g["emb"][tok] += dx[pos]
    return loss, g


def train():
    """Train reproducibly with NumPy's Adam operations and a fixed random seed."""
    rng = np.random.default_rng(1234)
    p = init_params(rng)
    m = {k: np.zeros_like(v) for k, v in p.items()}
    v = {k: np.zeros_like(val) for k, val in p.items()}
    lr, beta1, beta2, eps = 0.012, 0.9, 0.999, 1e-8
    step = 0
    # Each epoch visits each tiny prompt/answer sequence once. Prompt-token
    # prediction is masked; training starts with the first answer token.
    for epoch in range(2500):
        total = 0.0
        for seq in SEQUENCES:
            loss, grad = loss_and_grad(p, seq)
            total += loss
            step += 1
            for name in p:
                m[name] = beta1*m[name] + (1-beta1)*grad[name]
                v[name] = beta2*v[name] + (1-beta2)*(grad[name]*grad[name])
                mh = m[name] / (1-beta1**step)
                vh = v[name] / (1-beta2**step)
                p[name] -= lr * mh / (np.sqrt(vh) + eps)
        if epoch % 500 == 499:
            print(f"epoch={epoch+1} mean_loss={total/len(SEQUENCES):.6f}")
    return p


EXP_LUT = [4096,3186,2477,1928,1500,1167,907,705,549,427,332,259,
           201,157,122,95,74,58,45,35,27,21,17,13,10,8,6,5,4,3,2,2,1]


def trunc_div(a, b):
    if a < 0:
        return -(abs(a) // abs(b))
    return a // b


def q8(x):
    return np.clip(np.rint(np.asarray(x) * 256), -32768, 32767).astype(np.int64)


def int_sqrt(number):
    n = int(number)
    bit_value = 1 << 30
    result_value = 0
    for _ in range(16):
        if n >= result_value + bit_value:
            n -= result_value + bit_value
            result_value = (result_value >> 1) + bit_value
        else:
            result_value >>= 1
        bit_value >>= 2
    return result_value


def ln_q8(x, gamma, beta):
    mean = trunc_div(sum(int(v) for v in x), D)
    ds = [int(v) - mean for v in x]
    var = trunc_div(sum((v*v) >> 8 for v in ds), D)
    sigma = int_sqrt((var + 4) << 8)
    out = []
    for i, d in enumerate(ds):
        norm = trunc_div(d << 8, sigma) if sigma else 0
        out.append(((norm * int(gamma[i])) >> 8) + int(beta[i]))
    return out


def linear_q8(x, w, bias=None):
    result = []
    for col in range(w.shape[1]):
        acc = sum((int(x[row]) * int(w[row, col])) >> 8 for row in range(w.shape[0]))
        if bias is not None:
            acc += int(bias[col])
        result.append(acc)
    return result


def forward_q8(p, ids):
    n = len(ids)
    # Match RTL exactly: quantize each learned table entry first, then add the
    # token and position vectors in the Q8.8 activation domain.
    emb_q, pos_q = q8(p["emb"]), q8(p["pos"])
    x = [[int(v) for v in (emb_q[tok] + pos_q[pos])] for pos, tok in enumerate(ids)]
    norm1 = [ln_q8(row, q8(p["g1"]), q8(p["b1n"])) for row in x]
    q = [linear_q8(row, q8(p["wq"])) for row in norm1]
    k = [linear_q8(row, q8(p["wk"])) for row in norm1]
    v = [linear_q8(row, q8(p["wv"])) for row in norm1]
    attention = [[0]*D for _ in range(n)]
    for t in range(n):
        score_row = []
        for j in range(t+1):
            dot = sum((q[t][d]*k[j][d]) >> 8 for d in range(D))
            score_row.append((dot * 90) >> 8)
        maximum = max(score_row)
        exps = []
        for score in score_row:
            index = min(32, max(0, (maximum-score) >> 6))
            exps.append(EXP_LUT[index])
        denominator = sum(exps)
        probs = [(e*256)//denominator for e in exps]
        for d in range(D):
            attention[t][d] = sum(trunc_div(probs[j]*v[j][d], 256) for j in range(t+1))
    postattn = []
    for t in range(n):
        projected = linear_q8(attention[t], q8(p["wo"]))
        postattn.append([x[t][d]+projected[d] for d in range(D)])

    hidden = []
    for row in postattn:
        norm2 = ln_q8(row, q8(p["g2"]), q8(p["b2n"]))
        pre = linear_q8(norm2, q8(p["w1"]), q8(p["b1"]))
        act = [max(0, v0) for v0 in pre]
        ff = linear_q8(act, q8(p["w2"]), q8(p["b2"]))
        residual = [row[d]+ff[d] for d in range(D)]
        hidden.append(ln_q8(residual, q8(p["g3"]), q8(p["b3n"])))
    logits = linear_q8(hidden[-1], q8(p["lm"]), q8(p["lmb"]))
    return logits


def generate(p, prefix, quantized=False):
    ids = list(prefix)
    generated = []
    for _ in range(6):
        if quantized:
            logits = forward_q8(p, ids)
        else:
            logits, _ = forward(p, ids)
            logits = logits[-1]
        token = int(np.argmax(logits))
        if token == EOS_ID:
            break
        generated.append(token)
        ids.append(token)
    return generated


def packed_localparam(name, values):
    q = q8(values).reshape(-1).astype(int).tolist()
    words = [f"16'h{(value & 0xffff):04X}" for value in reversed(q)]
    lines = [f"    localparam logic [{len(q)*16-1}:0] {name} = {{"]
    for start in range(0, len(words), 8):
        comma = "," if start + 8 < len(words) else ""
        lines.append("        " + ", ".join(words[start:start+8]) + comma)
    lines.append("    };\n")
    return "\n".join(lines)


def export_sv(p):
    # Pack row-major Q8.8 parameters into one generated RTL file. Packed ROMs
    # keep the browser demo self-contained: no external .mem files are needed.
    tables = [
        ("EMB_ROM", p["emb"]), ("POS_ROM", p["pos"]),
        ("GAMMA1_ROM", p["g1"]), ("BETA1_ROM", p["b1n"]),
        ("GAMMA2_ROM", p["g2"]), ("BETA2_ROM", p["b2n"]),
        ("GAMMA3_ROM", p["g3"]), ("BETA3_ROM", p["b3n"]),
        ("WQ_ROM", p["wq"]), ("WK_ROM", p["wk"]),
        ("WV_ROM", p["wv"]), ("WO_ROM", p["wo"]),
        ("W1_ROM", p["w1"]), ("B1_ROM", p["b1"]),
        ("W2_ROM", p["w2"]), ("B2_ROM", p["b2"]),
        ("LM_ROM", p["lm"]), ("LMB_ROM", p["lmb"]),
    ]
    text = "\n".join(packed_localparam(name, value) for name, value in tables)
    root = Path(__file__).resolve().parent
    # The working copy stores this script under work/; the deliverable copy
    # stores it at the package root. Support both locations without edits.
    if root.name == "work":
        root = root.parent
    template_path = root / "rtl" / "tiny_gpt_template.sv"
    output_path = root / "rtl" / "tiny_gpt.sv"
    template = template_path.read_text(encoding="utf-8")
    marker = "    // GENERATED_WEIGHT_ROMS"
    if template.count(marker) != 1:
        raise RuntimeError("Expected exactly one GENERATED_WEIGHT_ROMS marker in template")
    output_path.write_text(template.replace(marker, text.rstrip()), encoding="utf-8")

    # Keep a human-readable copy of the exact signed integer values used by RTL.
    qparams = {
        "format": "signed Q8.8",
        "scale": 256,
        "model": {"vocab_size": V, "d_model": D, "ffn_size": F, "max_context": T,
                  "decoder_layers": 1, "attention_heads": 1},
        "token_ids": {
            "PAD": 0, "BOS": 1, "ASK_RAIN": 2, "ASK_CLEAR": 3,
            "FORECAST_HIGH": 4, "FORECAST_LOW": 5,
            "BI_GA": 6, "OL": 7, "GANEUNGSEONGI": 8,
            "NOPSEUBNIDA": 9, "NAJSEUBNIDA": 10, "EOS": 11, "MALGEUL": 12,
        },
        "parameters": {name: q8(value).astype(int).tolist() for name, value in tables},
    }
    weights_dir = root / "weights"
    weights_dir.mkdir(parents=True, exist_ok=True)
    (weights_dir / "trained_weights_q8.json").write_text(
        __import__("json").dumps(qparams, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    params = train()
    expected = {
        (2, 4): [6, 7, 8, 9],
        (2, 5): [6, 7, 8, 10],
        (3, 4): [12, 8, 10],
        (3, 5): [12, 8, 9],
    }
    for (qid, forecast_id), expected_ids in expected.items():
        prefix = [1, qid, forecast_id]
        float_ids = generate(params, prefix)
        fixed_ids = generate(params, prefix, quantized=True)
        print("prompt", prefix, "float generation:", float_ids)
        print("prompt", prefix, "Q8.8 generation:", fixed_ids)
        if fixed_ids != expected_ids:
            raise RuntimeError(f"Q8.8 export check failed for prompt {prefix}: {fixed_ids}")
    export_sv(params)
