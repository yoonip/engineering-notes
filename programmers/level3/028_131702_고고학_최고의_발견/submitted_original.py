from itertools import product

def solution(clockHands):
    n = len(clockHands)
    answer = 3 * n * n + 1
    for first in product(range(4), repeat=n):
        previous = [0] * n
        current = list(first)
        cost = sum(current)
        for r in range(n):
            if cost >= answer:
                break
            needed = [(-clockHands[r][c] - previous[c] - current[c] - (current[c - 1] if c else 0) - (current[c + 1] if c + 1 < n else 0)) % 4 for c in range(n)]
            if r == n - 1:
                if not any(needed):
                    answer = cost
                break
            cost += sum(needed)
            previous, current = current, needed
    return answer

# 전체 코드 줄별 설명
# from itertools import product  # itertools의 product를 import. 각 자리에서 0~3을 중복 선택하는 모든 조합 생성.
# 
# def solution(clockHands):  # def는 함수 정의. clockHands는 각 시계의 0~3 방향이 담긴 정사각형 격자.
#     n = len(clockHands)  # len은 격자의 한 변 길이.
#     answer = 3 * n * n + 1  # =는 대입. 각 시계는 4번 돌리면 원래대로이므로 최솟값은 최대 3N² 이내.
#     for first in product(range(4), repeat=n):  # range(4)는 0,1,2,3. repeat=n으로 첫 행의 회전 횟수 4^n가지를 모두 생성.
#         previous = [0] * n  # []와 * 반복. 격자 위쪽의 없는 행을 0회 회전으로 처리.
#         current = list(first)  # list는 튜플을 목록으로 변환. 현재 행의 각 시계 회전 횟수.
#         cost = sum(current)  # sum은 합계. 첫 행에 사용한 전체 회전 수.
#         for r in range(n):  # 위에서 아래로 각 행을 12시 방향으로 맞춤.
#             if cost >= answer:  # if는 조건문, >=는 이상. 이미 찾은 답을 개선할 수 없으면 중단.
#                 break  # break는 현재 첫 행 후보의 행 탐색 종료.
#             needed = [(-clockHands[r][c] - previous[c] - current[c] - (current[c - 1] if c else 0) - (current[c + 1] if c + 1 < n else 0)) % 4 for c in range(n)]  # 리스트 내포. 원래 방향+위·현재·현재 좌우 회전을 상쇄하려면 아래 칸을 몇 번 돌려야 하는지 계산. %4는 0~3의 회전 수.
#             if r == n - 1:  # ==는 같음. 마지막 행 아래에는 더 돌릴 시계가 없음.
#                 if not any(needed):  # any는 하나라도 참인지 검사, not은 부정. 모든 추가 필요 횟수가 0인지 확인.
#                     answer = cost  # 모든 행이 맞춰졌으므로 더 작은 비용을 정답으로 갱신.
#                 break  # 마지막 행 검사를 끝냈으므로 현재 후보 종료.
#             cost += sum(needed)  # +=는 더해 저장. 강제로 결정된 다음 행 회전 수를 비용에 추가.
#             previous, current = current, needed  # 두 변수 동시 대입으로 한 행 아래로 진행.
#     return answer  # return으로 모든 첫 행 후보 중 최소 회전 수 반환.

# 풀이 요약
# 첫 행의 회전 횟수만 0~3으로 모두 정하면, 각 행을 0으로 맞추기 위한 다음 행의 회전 횟수가 강제로 결정됩니다.
# 원래 방향과 위·현재·좌우 회전의 합을 4의 배수로 만드는 아래쪽 회전을 구합니다. 마지막 행에서 아래쪽 회전이 전부 0이어야 유효합니다. 시간 O(4^N N²), 추가 공간 O(N).
# 예: 위 칸에 남은 방향이 3이면 그 아래 시계를 한 번 돌려 위 칸을 0으로 만듭니다. 아래 행들은 이 선택을 순서대로 따라가므로 첫 행만 전수 탐색하면 됩니다.
# 