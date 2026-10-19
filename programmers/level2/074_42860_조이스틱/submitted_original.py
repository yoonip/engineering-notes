def solution(name):
    vertical = sum(min(ord(ch) - ord('A'), ord('Z') - ord(ch) + 1) for ch in name)
    n = len(name)
    horizontal = n - 1
    for index in range(n):
        next_index = index + 1
        while next_index < n and name[next_index] == 'A':
            next_index += 1
        tail = n - next_index
        horizontal = min(horizontal, 2 * index + tail, index + 2 * tail)
    return vertical + horizontal

# 전체 코드 줄별 설명
# def solution(name):  # def는 함수 정의. name은 만들 이름 문자열 입력.
#     vertical = sum(min(ord(ch) - ord('A'), ord('Z') - ord(ch) + 1) for ch in name)  # ord는 문자 코드, min은 최솟값, sum은 합. 각 문자를 위·아래 중 짧게 변경하는 비용.
#     n = len(name)  # len은 문자열 길이. =는 대입.
#     horizontal = n - 1  # 한 방향으로 끝까지 이동하는 기본 가로 비용.
#     for index in range(n):  # range(n)은 0~n-1. 방향을 되돌릴 지점 순회.
#         next_index = index + 1  # 현재 위치 뒤의 A 구간 시작점.
#         while next_index < n and name[next_index] == 'A':  # while은 반복, and는 둘 다 참, []는 문자 접근. 바꾸지 않아도 되는 연속 A 구간 탐색.
#             next_index += 1  # +=는 더해 저장. A 구간의 끝까지 이동.
#         tail = n - next_index  # A 구간 뒤쪽을 왼쪽으로 돌아 방문할 거리.
#         horizontal = min(horizontal, 2 * index + tail, index + 2 * tail)  # *는 곱셈. 오른쪽 먼저 갔다 복귀하거나 왼쪽 먼저 갔다 복귀하는 두 경로 비교.
#     return vertical + horizontal  # 세로·가로 최소 비용을 더해 return으로 반환.

# 풀이 요약
# 문자 변경 비용은 각 자리에서 독립입니다. 가로 이동은 연속 A 구간을 건너뛰며 한쪽으로 갔다 돌아오는 두 방향을 모두 비교합니다.
# 예: JAN은 J=9,N=13에 왼쪽 이동 1을 더해 23. 길이 N일 때 시간 O(N²), 추가 공간 O(1).
