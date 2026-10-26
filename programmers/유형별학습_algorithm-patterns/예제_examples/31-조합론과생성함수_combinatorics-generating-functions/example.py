import sys  # 다항식과 배수 조건 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 정수 토큰 순회
n, m = next(tokens), next(tokens)  # 다항식 길이
a = [next(tokens) for _ in range(n)]  # 첫 계수 배열
b = [next(tokens) for _ in range(m)]  # 둘째 계수 배열
product = [0] * (n + m - 1)  # 결과의 낮은 차수부터 저장
for i in range(n):  # 첫 선택의 크기
    for j in range(m):  # 둘째 선택의 크기
        product[i + j] += a[i] * b[j]  # 독립 선택의 수를 곱해 누적
limit, p, q = next(tokens), next(tokens), next(tokens)  # 포함 배제 입력
x, y = p, q  # 최대공약수 계산 상태
while y:  # 나머지를 반복
    x, y = y, x % y  # 다음 공약수 상태
lcm = p // x * q  # 두 조건의 공배수
union_count = limit // p + limit // q - limit // lcm  # 교집합 중복 제거
print(*product)  # 모든 곱 계수
print(union_count)  # 합집합의 정수 개수
