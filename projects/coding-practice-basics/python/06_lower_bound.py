import sys
from bisect import bisect_left

data = list(map(int, sys.stdin.buffer.read().split()))
if not data:
    raise SystemExit

n, q = data[:2]
values = data[2:2 + n]
queries = data[2 + n:2 + n + q]

for target in queries:
    index = bisect_left(values, target)
    print(index if index < n and values[index] == target else -1)
