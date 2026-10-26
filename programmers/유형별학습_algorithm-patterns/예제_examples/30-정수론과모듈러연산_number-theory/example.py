import sys  # 네 정수 입력 읽기
a, b, exponent, modulus = map(int, sys.stdin.read().split())  # 허용 범위의 조건
x, y = a, b  # 원래 밑과 분리한 유클리드 상태
while y:  # 나머지가 0이 될 때까지 반복
    x, y = y, x % y  # 공약수 집합을 보존하는 이동
result = 1 % modulus  # 빈 곱의 나머지
base = a % modulus  # 현재 비트의 거듭제곱
while exponent:  # 지수를 한 비트씩 처리
    if exponent & 1:  # 현재 거듭제곱이 필요한 자리
        result = result * base % modulus  # 선택한 인수 누적
    base = base * base % modulus  # 다음 자리의 제곱
    exponent >>= 1  # 처리한 비트 제거
print("GCD", x)  # 최대공약수
print("POWER", result)  # 모듈러 거듭제곱
