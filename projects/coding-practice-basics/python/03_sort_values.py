import sys

data = list(map(int, sys.stdin.buffer.read().split()))
if not data:
    raise SystemExit

n = data[0]
values = data[1:1 + n]
values.sort()
print(*values)
