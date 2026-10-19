def solution(cards):
    visited = set()
    groups = [0, 0]
    for start in range(len(cards)):
        node, size = start, 0
        while node not in visited:
            visited.add(node)
            size += 1
            node = cards[node] - 1
        groups.append(size)
    groups.sort(reverse=True)
    return groups[0] * groups[1]

# 전체 코드 줄별 설명
# def solution(cards):  # def는 함수 정의, cards는 상자 속 카드 번호 목록.
#     visited = set()  # set()은 중복 없는 집합. 연 상자 인덱스 저장.
#     groups = [0, 0]  # []는 리스트. 실제 그룹이 하나여도 두 최댓값을 고르도록 0 두 개 준비.
#     for start in range(len(cards)):  # len은 길이, range는 0부터 길이-1까지. 모든 시작점 순회.
#         node, size = start, 0  # 쉼표로 현재 상자와 그룹 크기를 각각 대입.
#         while node not in visited:  # while은 반복, not in은 집합에 없음. 이미 연 상자를 만날 때까지 진행.
#             visited.add(node)  # add로 현재 상자를 방문 표시.
#             size += 1  # +=는 더해 저장. 그룹 크기 증가.
#             node = cards[node] - 1  # [인덱스]로 카드 읽기. 1부터인 번호를 0부터인 인덱스로 변환.
#         groups.append(size)  # append로 이 시작점에서 새로 연 그룹 크기 저장.
#     groups.sort(reverse=True)  # sort는 제자리 정렬. reverse=True로 큰 그룹부터 배치.
#     return groups[0] * groups[1]  # *는 곱셈, return은 반환. 가장 큰 두 그룹의 곱 계산.

# 풀이 요약
# 카드가 중복 없는 순열이므로 연결을 따라가면 서로 겹치지 않는 사이클 그룹이 됩니다. 가장 큰 두 그룹을 선택합니다.
# 예: 그룹 크기 4,3,1이면 4×3=12. 시간 O(N log N), 공간 O(N).
