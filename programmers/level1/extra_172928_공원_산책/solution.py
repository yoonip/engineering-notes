def solution(park, routes):
    height = len(park)
    width = len(park[0])
    row, col = 0, 0
    for r, line in enumerate(park):
        if "S" in line:
            row, col = r, line.index("S")
            break
    directions = {
        "N": (-1, 0),
        "S": (1, 0),
        "W": (0, -1),
        "E": (0, 1),
    }
    for route in routes:
        direction, distance = route.split()
        distance = int(distance)
        dr, dc = directions[direction]
        next_row, next_col = row, col
        valid = True
        for _ in range(distance):
            next_row += dr
            next_col += dc
            if not (0 <= next_row < height and 0 <= next_col < width):
                valid = False
                break
            if park[next_row][next_col] == "X":
                valid = False
                break
        if valid:
            row, col = next_row, next_col
    return [row, col]

# 전체 코드 줄별 설명
# def solution(park, routes):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 공원 지도와 이동 명령을 입력받음.
#     height = len(park)  # len은 길이. =는 값 저장. 지도 행 수.
#     width = len(park[0])  # len은 길이. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 지도 열 수.
#     row, col = 0, 0  # =는 값 저장. 시작 좌표를 담을 변수 초기화.
#     for r, line in enumerate(park):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 각 행 번호와 문자열을 순회.
#         if "S" in line:  # if는 조건이 참일 때 실행. in은 포함 여부. 해당 행에 시작 표시 S가 있는지 확인.
#             row, col = r, line.index("S")  # index는 값이 처음 나오는 위치. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. S의 행·열 좌표 저장.
#             break  # break는 가장 가까운 반복문 종료. 시작점을 찾았으므로 탐색 종료.
#     directions = {  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 방향 이름을 행·열 변화량에 연결할 딕셔너리.
#         "N": (-1, 0),  # ()로 묶은 여러 값은 변경 불가 튜플. 북쪽은 행 -1, 열 0.
#         "S": (1, 0),  # ()로 묶은 여러 값은 변경 불가 튜플. 남쪽은 행 +1, 열 0.
#         "W": (0, -1),  # ()로 묶은 여러 값은 변경 불가 튜플. 서쪽은 행 0, 열 -1.
#         "E": (0, 1),  # ()로 묶은 여러 값은 변경 불가 튜플. 동쪽은 행 0, 열 +1.
#     }  # 딕셔너리 정의의 닫는 중괄호. 방향 정의 마침.
#     for route in routes:  # for·in은 원소를 차례로 꺼내는 반복문. 이동 명령을 순서대로 처리.
#         direction, distance = route.split()  # split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 명령을 방향 문자열과 거리 문자열로 나눔.
#         distance = int(distance)  # int는 정수 변환. =는 값 저장. 거리를 계산 가능한 정수로 바꿈.
#         dr, dc = directions[direction]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 해당 방향의 행·열 변화량을 읽음.
#         next_row, next_col = row, col  # =는 값 저장. 명령을 시험할 임시 위치를 현재 위치로 시작.
#         valid = True  # =는 값 저장. True·False는 참·거짓. 이동 가능하다고 가정.
#         for _ in range(distance):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 명령 거리만큼 한 칸씩 시험 이동.
#             next_row += dr  # +=는 더하거나 연결한 값을 저장. 임시 행 좌표 이동.
#             next_col += dc  # +=는 더하거나 연결한 값을 저장. 임시 열 좌표 이동.
#             if not (0 <= next_row < height and 0 <= next_col < width):  # if는 조건이 참일 때 실행. not은 참·거짓 반전. and는 두 조건 모두 참. <=는 이하 비교. <는 작음 비교. 지도를 벗어났는지 확인.
#                 valid = False  # =는 값 저장. True·False는 참·거짓. 명령을 무효로 표시.
#                 break  # break는 가장 가까운 반복문 종료. 남은 시험 이동 중단.
#             if park[next_row][next_col] == "X":  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. 도중에 장애물 X를 만났는지 확인.
#                 valid = False  # =는 값 저장. True·False는 참·거짓. 이 명령을 무효로 표시.
#                 break  # break는 가장 가까운 반복문 종료. 남은 시험 이동 중단.
#         if valid:  # if는 조건이 참일 때 실행. 모든 중간 칸을 지나갈 수 있는지 확인.
#             row, col = next_row, next_col  # =는 값 저장. 성공한 명령에만 실제 위치를 갱신.
#     return [row, col]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 마지막 행·열 좌표를 리스트로 반환.

# 풀이 요약
# 시작점을 찾고 방향별 행·열 변화량을 저장한다. 명령은 임시 좌표에서 한 칸씩 시험한다. 중간에 경계나 장애물을 만나면 명령 전체를 무효로 하고, 전부 통과했을 때만 실제 좌표를 바꾼다. 도착점만 검사하면 중간 장애물을 놓친다.
# 지도 H×W, 명령 거리 합 D: 시간 O(HW+D), 보조 공간 O(1).
