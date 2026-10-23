# permutations는 원소를 순서 있게 배치한 모든 순열을 생성.
from itertools import permutations

# 외벽 둘레·정렬된 취약점·친구별 이동 거리 입력.
def solution(n, weak, dist):
    # len은 취약점 개수.
    length = len(weak)
    # 취약점을 한 바퀴 뒤에도 복사해 원을 직선처럼 펼침.
    extended = weak + [point + n for point in weak]
    # 같은 인원이라면 이동 거리가 긴 친구부터 후보로 사용.
    friends = sorted(dist, reverse=True)
    # 적은 인원부터 가능 여부 확인.
    for count in range(1, len(friends) + 1):
        # 강한 친구 count명의 모든 투입 순서 비교.
        for order in set(permutations(friends[:count])):
            # 원을 펼칠 시작 취약점을 전부 시도.
            for start in range(length):
                # 아직 점검하지 못한 첫 취약점의 인덱스.
                next_point = start
                # 정한 순서대로 친구를 투입.
                for reach in order:
                    # 가장 앞의 미점검 취약점에서 출발했을 때 도달 가능한 끝.
                    end = extended[next_point] + reach
                    # 도달 범위 안 취약점은 모두 처리.
                    while next_point < start + length and extended[next_point] <= end:
                        # 다음 미점검 취약점으로 이동.
                        next_point += 1
                    # 한 바퀴의 모든 취약점을 처리했는지 확인.
                    if next_point == start + length:
                        # 적은 인원부터 검사했으므로 처음 성공한 인원 수가 최소.
                        return count
    # 모든 친구를 사용해도 실패하면 -1 반환.
    return -1
