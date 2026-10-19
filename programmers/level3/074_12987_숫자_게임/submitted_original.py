def solution(A, B):
    opponents = sorted(A)
    wins = 0
    for number in sorted(B):
        if wins < len(opponents) and number > opponents[wins]:
            wins += 1
    return wins

# 전체 코드 줄별 설명
# def solution(A, B):  # def는 함수 정의. 두 팀의 숫자 목록을 받음.
#     opponents = sorted(A)  # sorted는 새 정렬 리스트 반환. A의 작은 숫자부터 이길 상대 후보로 사용.
#     wins = 0  # 얻은 승점이자 아직 이기지 않은 가장 작은 상대의 인덱스.
#     for number in sorted(B):  # for로 B의 숫자도 작은 순서대로 사용.
#         if wins < len(opponents) and number > opponents[wins]:  # len은 길이, and는 모두 참, []는 인덱스 조회. 남은 가장 작은 상대를 이길 수 있는지 검사.
#             wins += 1  # +=는 더해 저장. 이길 수 있으면 매칭하고 다음 상대를 가리킴. 같으면 승점이 없으므로 > 사용.
#     return wins  # 최대 승점 반환.

# 풀이 요약
# B의 작은 숫자로 이길 수 있는 가장 작은 A부터 이긴다. 못 이기는 B는 어떤 남은 상대도 이길 수 없으므로 승리 후보에서 버려도 된다.
# 예: 정렬한 A=[1,3,5,7], B=[2,2,6,8]은 2>1, 6>3, 8>5로 세 번 승리한다. 남은 숫자끼리는 패배 경기로 배치하면 된다.
# 매칭할 A의 원래 순서는 그 상대 위치에 B를 배치하면 되므로 정렬해도 최대 승점은 같다. 시간 O(N log N), 공간 O(N).
# 