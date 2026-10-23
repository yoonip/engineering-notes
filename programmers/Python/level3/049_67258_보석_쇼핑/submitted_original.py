def solution(gems):
    kinds = len(set(gems))
    counts = {}
    left = 0
    best_left, best_right = 0, len(gems) - 1
    for right, gem in enumerate(gems):
        counts[gem] = counts.get(gem, 0) + 1
        while len(counts) == kinds:
            if right - left < best_right - best_left:
                best_left, best_right = left, right
            old = gems[left]
            counts[old] -= 1
            if counts[old] == 0:
                del counts[old]
            left += 1
    return [best_left + 1, best_right + 1]

# 전체 코드 줄별 설명
# def solution(gems):  # def는 함수 정의. gems는 진열 순서대로 저장된 보석 목록.
#     kinds = len(set(gems))  # set은 중복 없는 집합, len은 개수. 필요한 전체 보석 종류 수.
#     counts = {}  # {}는 딕셔너리. 현재 연속 구간 안에서 보석별 개수 저장.
#     left = 0  # 구간의 왼쪽 인덱스. 오른쪽과 함께 움직이는 투 포인터 방식.
#     best_left, best_right = 0, len(gems) - 1  # 언패킹 대입. 처음에는 전체 구간을 답으로 둠.
#     for right, gem in enumerate(gems):  # enumerate는 인덱스·값 쌍 제공. 오른쪽 끝을 한 칸씩 늘림.
#         counts[gem] = counts.get(gem, 0) + 1  # get은 키 조회, 없으면 0. 새로 포함한 보석 수 증가.
#         while len(counts) == kinds:  # while은 조건 반복, ==는 같음. 모든 종류가 들어 있는 동안 왼쪽을 줄임.
#             if right - left < best_right - best_left:  # 더 짧은 구간일 때만 갱신해 동점이면 이른 시작점 유지.
#                 best_left, best_right = left, right  # 최적 구간 갱신.
#             old = gems[left]  # []로 구간에서 빠질 보석 조회.
#             counts[old] -= 1  # -=는 빼서 저장. 왼쪽 보석 하나 제거.
#             if counts[old] == 0:  # 이 종류가 현재 구간에서 완전히 사라졌는지 확인.
#                 del counts[old]  # del은 딕셔너리의 키 삭제. len(counts)가 실제 포함 종류 수를 나타내게 함.
#             left += 1  # +=는 더해 저장. 왼쪽 끝을 한 칸 이동.
#     return [best_left + 1, best_right + 1]  # []는 리스트. 0부터 세는 인덱스를 1부터 세는 진열대 번호로 변환.

# 풀이 요약
# 오른쪽 끝을 늘려 모든 종류를 모으고, 조건을 만족하는 동안 왼쪽 끝을 줄여 최단 구간을 찾는다.
# 예제 1은 1~7번을 모은 뒤 중복된 앞 보석을 빼면 3~7번이 된다. 두 포인터는 뒤로 돌아가지 않는다.
# 시간 O(N), 공간 O(보석 종류 수). 동점에는 갱신하지 않아 시작 번호가 가장 작은 구간을 반환한다.
# 