from itertools import permutations

def solution(n, weak, dist):
    length = len(weak)
    extended = weak + [point + n for point in weak]
    friends = sorted(dist, reverse=True)
    for count in range(1, len(friends) + 1):
        for order in set(permutations(friends[:count])):
            for start in range(length):
                next_point = start
                for reach in order:
                    end = extended[next_point] + reach
                    while next_point < start + length and extended[next_point] <= end:
                        next_point += 1
                    if next_point == start + length:
                        return count
    return -1

# 전체 코드 줄별 설명
# from itertools import permutations  # import는 도구 가져오기. permutations는 원소를 순서 있게 배치한 모든 순열을 생성.
# 
# def solution(n, weak, dist):  # def는 함수 정의. 외벽 둘레·정렬된 취약점·친구별 이동 거리 입력.
#     length = len(weak)  # len은 취약점 개수.
#     extended = weak + [point + n for point in weak]  # 리스트 컴프리헨션. 취약점을 한 바퀴 뒤에도 복사해 원을 직선처럼 펼침.
#     friends = sorted(dist, reverse=True)  # sorted는 정렬, reverse=True는 내림차순. 같은 인원이라면 이동 거리가 긴 친구부터 후보로 사용.
#     for count in range(1, len(friends) + 1):  # range의 끝은 제외. 적은 인원부터 가능 여부 확인.
#         for order in set(permutations(friends[:count])):  # [:count]는 앞 count명. set은 중복 제거. 강한 친구 count명의 모든 투입 순서 비교.
#             for start in range(length):  # 원을 펼칠 시작 취약점을 전부 시도.
#                 next_point = start  # 아직 점검하지 못한 첫 취약점의 인덱스.
#                 for reach in order:  # 정한 순서대로 친구를 투입.
#                     end = extended[next_point] + reach  # 가장 앞의 미점검 취약점에서 출발했을 때 도달 가능한 끝.
#                     while next_point < start + length and extended[next_point] <= end:  # while은 조건 반복, and는 모두 참. 도달 범위 안 취약점은 모두 처리.
#                         next_point += 1  # +=는 더해 저장. 다음 미점검 취약점으로 이동.
#                     if next_point == start + length:  # ==는 같음. 한 바퀴의 모든 취약점을 처리했는지 확인.
#                         return count  # 적은 인원부터 검사했으므로 처음 성공한 인원 수가 최소.
#     return -1  # 모든 친구를 사용해도 실패하면 -1 반환.

# 풀이 요약
# 원을 두 배로 펼쳐 시작 취약점·친구 순서를 모두 시도한다. 각 친구는 첫 미점검 취약점부터 최대한 멀리 점검한다.
# 반시계로 덮는 구간도 반대 끝에서 시계로 덮을 수 있으므로 시계 방향만 검사해도 된다. 같은 인원에서는 긴 거리 친구를 쓰는 것이 불리하지 않다.
# 예제 1은 10→1과 5→6을 두 명이 담당한다. 취약점 W≤15, 친구 F≤8일 때 시간 O(F!·W²), 공간 O(F!·F+W).
# 