import sys  # 단계와 모듈러 읽기
exponent, modulus = map(int, sys.stdin.read().split())  # 피보나치 조건
def multiply(left, right):  # 2×2 행렬 내적
    result = [[0, 0], [0, 0]]  # 입력과 별개인 영행렬
    for i in range(2):  # 결과 행
        for j in range(2):  # 결과 열
            for k in range(2):  # 내적의 공통 좌표
                result[i][j] = (result[i][j] + left[i][k] * right[k][j]) % modulus  # 나머지를 유지한 곱 누적
    return result  # 새 행렬 반환
answer = [[1, 0], [0, 1]]  # 0단계 단위 전이
base = [[1, 1], [1, 0]]  # 한 단계의 점화
while exponent:  # 이진수 자리 처리
    if exponent & 1:  # 필요한 길이의 전이 선택
        answer = multiply(answer, base)  # 현재 결과에 합성
    base = multiply(base, base)  # 다음 자리의 제곱
    exponent >>= 1  # 처리한 자리 제거
print(answer[1][0] % modulus)  # 초기 벡터에서 F_N인 성분
