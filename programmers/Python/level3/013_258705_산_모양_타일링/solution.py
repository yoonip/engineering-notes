def solution(n, tops):
    # 문제에서 요구한 나머지 기준 저장.
    modulus = 10007
    joined, free = 0, 1
    # 위쪽 삼각형의 유무 0 또는 1을 왼쪽부터 순회.
    for top in tops:
        next_joined = (joined + free) % modulus
        # 이전 끝이 묶였으면 1+top개, 단독이면 왼쪽과 묶는 방법까지 2+top개로 확장.
        next_free = ((1 + top) * joined + (2 + top) * free) % modulus
        joined, free = next_joined, next_free
    return (joined + free) % modulus
