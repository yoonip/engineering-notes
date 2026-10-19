#!/usr/bin/env python3
"""DDR training-window analysis and exact zero-error BER upper bound."""
import json
import math


def longest_window(passed_taps):
    """Select the longest contiguous window, not min/max of disjoint islands."""
    taps = sorted(set(passed_taps))
    if not taps:
        return {'pass': False, 'reason': 'NO_PASS_TAP'}
    windows = []
    start = previous = taps[0]
    for tap in taps[1:]:
        if tap != previous + 1:
            windows.append((start, previous))
            start = tap
        previous = tap
    windows.append((start, previous))
    left, right = max(windows, key=lambda pair: pair[1] - pair[0])
    # Tie-break chooses first/lowest interval. A real PHY supplies its own rule.
    chosen = (left + right) // 2
    return {'pass': True, 'left_tap': left, 'right_tap': right,
            'passing_tap_count': right-left+1, 'chosen_tap': chosen,
            'margin_steps': min(chosen-left, right-chosen), 'all_windows': windows}


def zero_error_upper(bits, confidence=0.95):
    if bits <= 0 or not 0 < confidence < 1:
        raise ValueError('positive bits and 0<confidence<1 required')
    # (1-p)^N = 1-confidence; stable for very large N.
    return -math.expm1(math.log1p(-confidence) / bits)


if __name__ == '__main__':
    report = {'lane0': longest_window(range(12,37)),
              'lane1': longest_window(range(20,25)),
              'split': longest_window([1,2,3,9,10]),
              'ber_upper_95_for_3e12_bits': zero_error_upper(3_000_000_000_000),
              'seconds_at_10gbit_s': 3e12 / 10e9}
    print(json.dumps(report, indent=2))
