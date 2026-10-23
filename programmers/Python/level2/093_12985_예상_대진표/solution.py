def solution(n, a, b):
    rounds = 0
    # 다음 라운드 번호가 같아질 때까지 진행.
    while a != b:
        a = (a + 1) // 2
        # 상대의 다음 라운드 번호도 같은 방식으로 계산.
        b = (b + 1) // 2
        rounds += 1
    return rounds
