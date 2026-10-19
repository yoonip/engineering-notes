def solution(arrows):
    directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    current = (0, 0)
    vertices = {current}
    edges = set()
    rooms = 0
    for arrow in arrows:
        dx, dy = directions[arrow]
        for _ in range(2):
            following = (current[0] + dx, current[1] + dy)
            edge = (current, following) if current < following else (following, current)
            if edge not in edges:
                if following in vertices:
                    rooms += 1
                edges.add(edge)
                vertices.add(following)
            current = following
    return rooms

# 전체 코드 줄별 설명
# def solution(arrows):  # def는 함수 정의. arrows는 0~7 방향 번호를 담은 입력 리스트.
#     directions = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))  # ()는 변경 불가 튜플. 위부터 시계 방향으로 좌표 변화량 저장.
#     current = (0, 0)  # 현재 좌표를 두 정수의 튜플로 저장. 튜플은 집합의 원소로 사용 가능.
#     vertices = {current}  # {}에 원소를 쓰면 집합 set. 방문 좌표를 중복 없이 저장하고 빠르게 조회.
#     edges = set()  # set()은 빈 집합. 이미 그은 무방향 선분을 저장.
#     rooms = 0  # 새로 완성된 방의 개수 초기화.
#     for arrow in arrows:  # for는 반복문. 입력 방향을 차례대로 처리.
#         dx, dy = directions[arrow]  # []로 인덱스 접근. 튜플의 두 값을 dx, dy로 나누어 받음.
#         for _ in range(2):  # range(2)는 0,1. 한 이동을 두 단계로 나누어 대각선 교차점도 좌표로 처리. _는 사용하지 않는 변수.
#             following = (current[0] + dx, current[1] + dy)  # 현재 x·y에 방향 변화량을 더해 다음 좌표 계산.
#             edge = (current, following) if current < following else (following, current)  # 조건 표현식. 튜플은 앞 값부터 비교하여 두 끝점의 순서를 통일.
#             if edge not in edges:  # if는 조건문, not in은 집합에 없음. 처음 그리는 선분만 검사.
#                 if following in vertices:  # in은 포함 여부. 새 선분으로 이미 방문한 점에 닿으면 닫힌 방 하나 생성.
#                     rooms += 1  # +=는 기존 값에 더해 저장. 방 개수 1 증가.
#                 edges.add(edge)  # add는 집합에 원소 추가. 이 선분을 그렸다고 기록.
#                 vertices.add(following)  # 도착 좌표를 방문 집합에 기록. 이미 있으면 변화 없음.
#             current = following  # 다음 반복을 위해 현재 위치를 도착 좌표로 갱신.
#     return rooms  # return은 함수 결과 반환. 총 방 개수 출력.

# 풀이 요약
# 새로운 선분으로 기존 꼭짓점에 도착하면 방이 하나 늘어납니다. 이미 그은 선분을 되짚을 때는 늘어나지 않습니다.
# 한 이동을 두 단계로 쪼개 대각선끼리 중간에서 교차하는 점도 반드시 기록합니다. 예제 답은 3이며 시간·공간은 O(N)입니다.
# 