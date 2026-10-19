"""Evaluate a two-token attention example and its causal mask."""
import json
import math
import platform
from pathlib import Path


def row_attention(query, keys, values, visible):
    scores = [sum(a * b for a, b in zip(query, key)) / math.sqrt(len(query))
              for key in keys[:visible]]
    offset = max(scores)
    exps = [math.exp(score - offset) for score in scores]
    weights = [value / sum(exps) for value in exps]
    output = [sum(weight * value[col] for weight, value in zip(weights, values))
              for col in range(len(values[0]))]
    return weights, output


def evaluate():
    keys = [[1.0, 0.0], [0.0, 1.0]]
    values = [[10.0, 0.0], [0.0, 20.0]]
    weights, output = row_attention([1.0, 0.0], keys, values, 2)
    causal_weights, causal_output = row_attention([1.0, 0.0], keys, values, 1)
    assert math.isclose(sum(weights), 1.0)
    assert all(0 <= w <= 1 for w in weights)
    assert math.isclose(weights[0], 1 / (1 + math.exp(-1 / math.sqrt(2))))
    assert causal_weights == [1.0] and causal_output == values[0]
    shifted = [key[:] for key in keys]
    shifted[1] = [900.0, -900.0]
    assert row_attention([1.0, 0.0], shifted, values, 1) == (causal_weights, causal_output)
    return {'python': platform.python_version(), 'query': [1, 0], 'keys': keys,
            'values': values, 'weights': weights, 'output': output,
            'causal_weights': causal_weights, 'causal_output': causal_output,
            'checks': ['normalization', 'nonnegative weights', 'closed-form value',
                       'causal first token', 'future-key invariance']}


if __name__ == '__main__':
    result = evaluate()
    Path(__file__).with_name('attention_result.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
