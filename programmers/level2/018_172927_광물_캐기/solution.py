from functools import lru_cache

def solution(picks, minerals):
    fatigue = {'diamond': (1, 5, 25), 'iron': (1, 1, 5), 'stone': (1, 1, 1)}
    blocks = []
    for start in range(0, len(minerals), 5):
        chunk = minerals[start:start + 5]
        blocks.append(tuple(sum(fatigue[name][pick] for name in chunk) for pick in range(3)))
    @lru_cache(None)
    def dfs(index, remaining):
        if index == len(blocks) or sum(remaining) == 0:
            return 0
        best = float('inf')
        for pick, count in enumerate(remaining):
            if count > 0:
                next_remaining = list(remaining)
                next_remaining[pick] -= 1
                cost = blocks[index][pick] + dfs(index + 1, tuple(next_remaining))
                best = min(best, cost)
        return best
    return dfs(0, tuple(picks))

# 전체 코드 줄별 설명
# from functools import lru_cache  # from~import로 기능 가져오기. functools의 lru_cache는 같은 인수의 함수 결과를 재사용하는 캐시.
# 
# def solution(picks, minerals):  # def는 함수 정의. 곡괭이 수·광물 순서가 입력.
#     fatigue = {'diamond': (1, 5, 25), 'iron': (1, 1, 5), 'stone': (1, 1, 1)}  # {}는 딕셔너리, 문자열 키에 곡괭이별 피로도 튜플을 연결.
#     blocks = []  # []는 빈 리스트. 연속 다섯 광물의 곡괭이별 비용 저장.
#     for start in range(0, len(minerals), 5):  # range(시작,끝,간격)으로 0,5,10,... 순회. len은 길이.
#         chunk = minerals[start:start + 5]  # [시작:끝] 슬라이스는 끝 미포함 부분 리스트 복사.
#         blocks.append(tuple(sum(fatigue[name][pick] for name in chunk) for pick in range(3)))  # sum은 합계, tuple은 불변 묶음. 각 곡괭이의 묶음 비용을 만들어 append로 추가.
#     @lru_cache(None)  # @는 데코레이터 적용. None은 캐시 개수 제한 없이 동일 상태의 결과 재사용.
#     def dfs(index, remaining):  # 중첩 함수 정의. 다음 광물 묶음 번호와 남은 곡괭이 튜플을 상태로 사용.
#         if index == len(blocks) or sum(remaining) == 0:  # ==는 같음, or는 하나라도 참. 광물 또는 곡괭이가 끝나면 종료.
#             return 0  # 더 들 피로도 0 반환.
#         best = float('inf')  # float('inf')는 양의 무한대. 최솟값 비교용 초기값.
#         for pick, count in enumerate(remaining):  # enumerate는 인덱스·값 제공. 곡괭이 종류와 수를 순회.
#             if count > 0:  # if는 조건 분기, >는 큼. 남은 종류만 선택.
#                 next_remaining = list(remaining)  # list는 수정 가능한 리스트로 변환. 원래 상태를 보존하며 복사.
#                 next_remaining[pick] -= 1  # [pick] 원소 접근, -=는 빼서 저장. 선택한 곡괭이 하나 소비.
#                 cost = blocks[index][pick] + dfs(index + 1, tuple(next_remaining))  # 다음 묶음 재귀 호출. 캐시 키에는 불변 tuple 사용, 현재 비용을 더함.
#                 best = min(best, cost)  # min은 최솟값. 가능한 선택 중 가장 적은 비용 유지.
#         return best  # 현재 상태에서의 최소 추가 피로도 반환.
#     return dfs(0, tuple(picks))  # 0번 묶음부터 시작해 전체 최소 피로도 반환.

# 풀이 요약
# 광물을 순서대로 다섯 개씩 묶고, 각 묶음에 쓸 곡괭이를 모두 선택해 봅니다. 남은 수가 같은 상태는 캐시로 재사용합니다.
# 예: 첫 묶음은 다이아, 나머지는 철 곡괭이를 쓰면 12. 묶음 수 B, 초기 곡괭이 수 D,I,S일 때 시간·공간 O(B(D+1)(I+1)(S+1)).
