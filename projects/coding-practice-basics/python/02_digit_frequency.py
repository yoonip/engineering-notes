import sys

digits = sys.stdin.buffer.readline().strip()
frequency = [0] * 10

for ch in digits:
    if ord("0") <= ch <= ord("9"):
        frequency[ch - ord("0")] += 1

print(*frequency)
