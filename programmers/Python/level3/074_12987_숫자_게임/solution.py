# 두 팀의 숫자 목록을 받음.
def solution(A, B):
    # A의 작은 숫자부터 이길 상대 후보로 사용.
    opponents = sorted(A)
    # 얻은 승점이자 아직 이기지 않은 가장 작은 상대의 인덱스.
    wins = 0
    # for로 B의 숫자도 작은 순서대로 사용.
    for number in sorted(B):
        # 남은 가장 작은 상대를 이길 수 있는지 검사.
        if wins < len(opponents) and number > opponents[wins]:
            # 같으면 승점이 없으므로 > 사용.
            wins += 1
    # 최대 승점 반환.
    return wins
