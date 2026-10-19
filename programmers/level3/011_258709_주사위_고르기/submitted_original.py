from collections import Counter
from itertools import combinations
from functools import lru_cache

def solution(dice):
    n = len(dice)

    @lru_cache(None)
    def distribution(indices):
        if not indices:
            return Counter({0: 1})
        previous = distribution(indices[:-1])
        counts = Counter()
        for total, count in previous.items():
            for face in dice[indices[-1]]:
                counts[total + face] += count
        return counts

    best = -1
    answer = []
    for selected in combinations(range(n), n // 2):
        other = tuple(i for i in range(n) if i not in selected)
        left, right = distribution(selected), distribution(other)
        cumulative = [0]
        for value in range(501):
            cumulative.append(cumulative[-1] + right[value])
        wins = sum(count * cumulative[value] for value, count in left.items())
        if wins > best:
            best = wins
            answer = [i + 1 for i in selected]
    return answer

# 전체 코드 줄별 설명
# from collections import Counter  # collections의 Counter를 import. 주사위 합마다 나오는 경우의 수를 저장하는 빈도표.
# from itertools import combinations  # itertools의 combinations는 순서를 무시하고 중복 없이 고르는 조합 생성.
# from functools import lru_cache  # functools의 lru_cache는 같은 인수로 구한 결과를 재사용하는 캐시 도구.
# 
# def solution(dice):  # def는 함수 정의. dice는 주사위별 여섯 면의 값 목록.
#     n = len(dice)  # len은 주사위 개수.
# 
#     @lru_cache(None)  # @는 데코레이터 적용. None은 캐시 용량 제한 없음.
#     def distribution(indices):  # 선택한 주사위 번호 튜플에 대한 합별 경우의 수를 구하는 재귀 함수.
#         if not indices:  # not은 부정. 빈 튜플이면 주사위를 고르지 않은 상태.
#             return Counter({0: 1})  # {}는 딕셔너리. 아무것도 굴리지 않은 합 0은 한 가지.
#         previous = distribution(indices[:-1])  # [:-1]은 마지막 원소 제외 슬라이스. 마지막 주사위를 빼고 작은 문제 계산.
#         counts = Counter()  # 결과를 담을 새로운 빈 Counter 생성. 캐시된 previous는 수정하지 않음.
#         for total, count in previous.items():  # items는 (합, 경우의 수) 쌍을 제공.
#             for face in dice[indices[-1]]:  # [-1]은 마지막 원소. 마지막 주사위의 여섯 면을 순회.
#                 counts[total + face] += count  # +=는 더해 저장. 이 면을 더한 새 합의 경우의 수 누적.
#         return counts  # return으로 합별 분포 반환. 같은 주사위 조합이면 캐시 재사용.
# 
#     best = -1  # 지금까지 가장 큰 승리 경우의 수 초기화.
#     answer = []  # []는 정답 주사위 번호 리스트.
#     for selected in combinations(range(n), n // 2):  # range는 0~n-1, //는 정수 나눗셈. A가 가져갈 절반의 모든 조합 순회.
#         other = tuple(i for i in range(n) if i not in selected)  # not in은 미포함 검사. B가 가져갈 나머지 번호를 불변 튜플로 생성.
#         left, right = distribution(selected), distribution(other)  # A·B의 합별 경우의 수를 언패킹으로 저장.
#         cumulative = [0]  # cumulative[v]는 B의 합이 v보다 작은 경우의 수.
#         for value in range(501):  # 면 최댓값 100·최대 5개이므로 합은 500 이하.
#             cumulative.append(cumulative[-1] + right[value])  # append는 끝에 하나 추가. Counter의 없는 합은 0으로 조회됨.
#         wins = sum(count * cumulative[value] for value, count in left.items())  # sum은 합계. A의 각 합 경우의 수 × 그보다 작은 B 합 경우의 수.
#         if wins > best:  # if는 조건문, >는 초과. 승률의 분모가 같으므로 승리 경우의 수만 비교.
#             best = wins  # =는 대입. 최대 승리 수 갱신.
#             answer = [i + 1 for i in selected]  # 리스트 내포로 0 기반 번호를 1 기반으로 변환. combinations 순서가 오름차순을 보장.
#     return answer  # 가장 승률이 높은 주사위 번호 목록 반환.

# 풀이 요약
# A가 고를 절반의 주사위 조합을 모두 비교합니다. 합별 경우의 수를 캐시하고, B의 누적 빈도로 A보다 작은 합의 경우의 수를 빠르게 셉니다.
# 무승부는 이긴 경우에 넣지 않습니다. 각 선택의 전체 경우 수가 같으므로 승리 횟수가 가장 큰 조합이 답입니다. N≤10, 합 범위≤500을 이용합니다.
# 예: 첫 예제에서 1·4번 주사위는 616가지 승리로 최댓값이므로 [1,4]를 반환합니다.
