import sys

data = list(map(int, sys.stdin.buffer.read().split()))
if not data:
    raise SystemExit

n = data[0]
cost = data[1:1 + n]
best = [0] * n

best[0] = cost[0]
if n >= 2:
    best[1] = cost[0] + cost[1]

for i in range(2, n):
    best[i] = min(best[i - 1], best[i - 2]) + cost[i]

print(best[-1])
