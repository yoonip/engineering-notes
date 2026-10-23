def solution(points, routes):
    robots = []
    for route in routes:
        r, c = points[route[0] - 1]
        robots.append((r, c, 1, route))
    answer = 0
    while robots:
        counts = {}
        next_robots = []
        for r, c, index, route in robots:
            position = (r, c)
            counts[position] = counts.get(position, 0) + 1
            if index == len(route):
                continue
            target_r, target_c = points[route[index] - 1]
            if r != target_r:
                r += 1 if r < target_r else -1
            elif c != target_c:
                c += 1 if c < target_c else -1
            if r == target_r and c == target_c:
                index += 1
            next_robots.append((r, c, index, route))
        for count in counts.values():
            if count >= 2:
                answer += 1
        robots = next_robots
    return answer

# 전체 코드 줄별 설명 (아래는 모두 실행되지 않는 주석입니다.)
# def solution(points, routes):  # def는 함수 정의. points·routes는 입력, : 아래 들여쓰기는 함수 본문.
#     robots = []  # []는 빈 리스트. 현재 초에 센터 안에 있는 로봇 상태 저장.
#     for route in routes:  # for~in으로 로봇별 경로를 순회.
#         r, c = points[route[0] - 1]  # []는 인덱싱, -1은 번호를 0부터인 인덱스로 변환. 쉼표 언패킹으로 시작 좌표 받음.
#         robots.append((r, c, 1, route))  # append는 리스트 끝에 추가. () 튜플에 행·열·다음 목표 인덱스·경로를 묶어 저장.
#     answer = 0  # 위험 횟수 초기화. =는 대입.
#     while robots:  # while은 조건 반복. 빈 리스트는 거짓이므로 로봇이 남은 동안 실행.
#         counts = {}  # {}는 빈 딕셔너리. 이번 초의 좌표별 로봇 수 저장.
#         next_robots = []  # 다음 초의 상태를 담을 새 리스트 생성.
#         for r, c, index, route in robots:  # 로봇 상태 튜플의 네 값을 변수 네 개로 언패킹하며 순회.
#             position = (r, c)  # (r,c)는 좌표 튜플. 원소가 정수인 튜플은 딕셔너리 키로 사용 가능.
#             counts[position] = counts.get(position, 0) + 1  # get(키,기본값)은 키가 없으면 0을 반환. [키]에 해당 좌표의 수를 1 늘려 저장.
#             if index == len(route):  # len은 원소 수, ==는 같음. 다음 목표가 없으면 최종 도착한 로봇.
#                 continue  # continue로 이번 로봇 처리를 마침. 현재 도착 위치는 셌고 다음 초 목록에서는 제외.
#             target_r, target_c = points[route[index] - 1]  # 경로의 다음 번호를 좌표로 변환. 두 []는 각각 경로와 포인트 목록 접근.
#             if r != target_r:  # !=는 다름. 목표와 행이 다르면 행부터 이동.
#                 r += 1 if r < target_r else -1  # a if 조건 else b는 조건 표현식. 목표 방향에 따라 +1 또는 -1, +=는 더해서 저장.
#             elif c != target_c:  # elif는 앞 조건이 거짓일 때 검사. 행이 같을 때만 열 이동.
#                 c += 1 if c < target_c else -1  # 목표 열 방향으로 한 칸 이동. 한 초에 행·열 중 하나만 바뀜.
#             if r == target_r and c == target_c:  # and는 두 조건 모두 참. 이동 후 목표에 도착했는지 검사.
#                 index += 1  # 다음에 방문할 경로 인덱스를 1 늘림.
#             next_robots.append((r, c, index, route))  # 이동 후 상태를 다음 초 목록에 추가. 최종 도착 순간도 다음 반복에서 한 번 셈.
#         for count in counts.values():  # values()는 딕셔너리 값들을 제공. 좌표별 로봇 수만 순회.
#             if count >= 2:  # >=는 이상. 같은 초·좌표에 두 대 이상이면 위험.
#                 answer += 1  # += 1로 위험 좌표를 한 번만 셈. 로봇 쌍 수를 세지 않음.
#         robots = next_robots  # 다음 초 목록으로 교체. 현재 리스트를 순회 중에 삭제하지 않음.
#     return answer  # return으로 모든 초의 위험 횟수 반환.

# 풀이 요약
# 매 초 로봇의 현재 좌표를 세고, 행 우선으로 한 칸 움직여 다음 초 상태를 만듭니다.
# 0초와 마지막 도착 순간을 포함하며, 센터를 떠난 로봇은 다음 초부터 제외합니다. 시간 O(로봇 수*최대 이동 시간), 공간 O(로봇 수).
# 예: 같은 초 (4,4)에 네 대가 모여도 위험 상황은 1번입니다. 서로 다른 두 좌표에서 모이면 2번입니다.
