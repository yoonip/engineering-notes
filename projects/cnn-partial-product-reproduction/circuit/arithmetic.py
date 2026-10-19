"""Signed partial-product column masking, shared by software and CMOS generator.

Domain: two's-complement signed n-bit a,b, 0 <= k <= n-1.
Drop ALL partial products with i+j<k before carry propagation.
This differs from masking a finished product or a dot-product accumulator.
"""
from __future__ import annotations
import numpy as np


def signed_value(word: int, width: int) -> int:
    word &= (1 << width) - 1
    return word - (1 << width) if word & (1 << (width-1)) else word


def column_mask_mul(a, b, n: int, k: int):
    if not 0 <= k <= n-1:
        raise ValueError('mask k must be in 0..n-1; sign columns must stay enabled')
    a, b = np.asarray(a, dtype=np.int64), np.asarray(b, dtype=np.int64)
    if np.any(a < -(1 << (n-1))) or np.any(a >= (1 << (n-1))) or np.any(b < -(1 << (n-1))) or np.any(b >= (1 << (n-1))):
        raise ValueError('operand outside signed n-bit range')
    result = a*b
    for i in range(k):
        result = result - ((a >> i) & 1) * (b & ((1 << (k-i))-1)) * (1 << i)
    return result


def baugh_wooley_mul(a: int, b: int, n: int, k: int) -> int:
    """Independent bit-matrix evaluation of the implemented hardware."""
    if not 0 <= k <= n-1:
        raise ValueError('invalid k')
    word_a, word_b = a & ((1 << n)-1), b & ((1 << n)-1)
    total = (1 << n) + (1 << (2*n-1))
    for i in range(n):
        for j in range(n):
            if i+j < k:
                continue
            term = ((word_a >> i)&1) & ((word_b >> j)&1)
            if (i == n-1) != (j == n-1):
                term ^= 1
            total += term << (i+j)
    return signed_value(total, 2*n)


def make_lut(n: int, k: int) -> np.ndarray:
    vals = np.arange(-(1 << (n-1)), 1 << (n-1), dtype=np.int64)
    return column_mask_mul(vals[:,None], vals[None,:], n, k).astype(np.int32)


def accumulator_width(n: int, terms: int) -> int:
    """Width safe for arbitrary signed products, including (-2^(n-1))^2."""
    if terms < 1:
        raise ValueError('terms must be positive')
    max_sum = terms * (1 << (2*n-2))
    return max_sum.bit_length() + 1


if __name__ == '__main__':
    print('n=6, 784 terms:', accumulator_width(6,784), 'bits')
    print('n=8, 784 terms:', accumulator_width(8,784), 'bits')
