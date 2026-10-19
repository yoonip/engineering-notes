import os

# 이 device의 계약: 최대 256byte 입력의 unsigned byte 합과 길이를 반환.
payload = bytes([1, 2, 3, 250])
fd = os.open("/dev/valdemo", os.O_WRONLY)
try:
    written = os.write(fd, payload)
    if written != len(payload):
        raise RuntimeError(f"short write: {written}")
finally:
    os.close(fd)

# 새 open은 offset=0에서 시작한다.
with open("/dev/valdemo", "rb", buffering=0) as device:
    line = device.read(96).decode("ascii").strip()

fields = dict(part.split("=", 1) for part in line.split())
assert int(fields["length"]) == len(payload), line
assert int(fields["sum"]) == sum(payload), line
print("PASS", line)
