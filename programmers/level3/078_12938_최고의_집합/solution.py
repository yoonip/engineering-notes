# 자연수 개수와 만들 합을 받음.
def solution(n, s):
    # 각 원소가 최소 1이어야 하므로 합이 개수보다 작으면 불가능.
    if s < n:
        # 문제에서 지정한 불가능 표시 반환.
        return [-1]
    # 두 변수에 언패킹 대입해 고르게 나눌 기준값 계산.
    quotient, remainder = divmod(s, n)
    # 작은 값부터 배치해 오름차순 결과 생성.
    return [quotient] * (n - remainder) + [quotient + 1] * remainder
