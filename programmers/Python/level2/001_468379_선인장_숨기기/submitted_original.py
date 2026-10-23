from collections import deque


def window_minimum(values, size):
    q = deque()
    result = []

    for i, value in enumerate(values):
        while q and q[0] <= i - size:
            q.popleft()

        while q and values[q[-1]] >= value:
            q.pop()

        q.append(i)

        if i >= size - 1:
            result.append(values[q[0]])

    return result


def solution(m, n, h, w, drops):
    never = len(drops) + 1
    rain = [never] * (m * n)

    for time, (r, c) in enumerate(drops, start=1):
        rain[r * n + c] = time

    cols = n - w + 1

    row_min = []

    for r in range(m):
        row = rain[r * n:(r + 1) * n]
        row_min.extend(window_minimum(row, w))

    best_time = -1
    answer = [0, 0]

    for c in range(cols):
        column = row_min[c::cols]
        area_times = window_minimum(column, h)

        for r, time in enumerate(area_times):
            if time > best_time or (
                time == best_time and [r, c] < answer
            ):
                best_time = time
                answer = [r, c]

    return answer

# 전체 코드 줄별 설명
# from collections import deque  # from A import B는 A 모듈에서 B를 가져옴. deque는 양끝 삽입·삭제가 빠른 덱.
# 
# 
# def window_minimum(values, size):  # def는 함수 정의. values는 값 목록, size는 연속 구간의 길이.
#     q = deque()  # deque()는 빈 덱 생성. 최솟값 후보의 인덱스를 저장.
#     result = []  # []는 빈 리스트. 각 구간의 최솟값을 모음.
# 
#     for i, value in enumerate(values):  # for는 순회, enumerate는 (인덱스, 값) 제공. 두 변수로 나눠 받음.
#         while q and q[0] <= i - size:  # while은 반복, and는 두 조건 모두 참. [0]은 맨 앞, 범위 밖 후보인지 검사.
#             q.popleft()  # popleft()는 덱 맨 앞을 제거하고 반환.
# 
#         while q and values[q[-1]] >= value:  # [-1]은 맨 뒤. 새 값보다 크거나 같은 후보는 앞으로 쓸 일이 없음.
#             q.pop()  # pop()은 맨 뒤 후보 제거. 작은 값부터 남는 단조 덱 유지.
# 
#         q.append(i)  # append(i)는 현재 인덱스를 맨 뒤에 추가.
# 
#         if i >= size - 1:  # if는 조건문, >=는 이상. 구간 길이가 size가 됐는지 확인.
#             result.append(values[q[0]])  # 덱 첫 인덱스의 값이 구간 최솟값. 결과 리스트 끝에 추가.
# 
#     return result  # return은 함수 종료와 결과 반환.
# 
# 
# def solution(m, n, h, w, drops):  # 입력 m·n은 지도 크기, h·w는 구역 크기, drops는 빗방울 순서.
#     never = len(drops) + 1  # len은 길이. 실제 빗방울보다 큰 값으로 비가 안 오는 칸 표현.
#     rain = [never] * (m * n)  # [never] * 개수로 초기화. r*n+c에 저장할 1차원 지도.
# 
#     for time, (r, c) in enumerate(drops, start=1):  # enumerate(..., start=1)은 번호를 1부터 붙임. (r,c)는 좌표 언패킹.
#         rain[r * n + c] = time  # r*n+c로 2차원 좌표를 1차원 인덱스로 바꿔 도착 시각 저장.
# 
#     cols = n - w + 1  # 가로 w칸 구역을 시작할 수 있는 열의 수.
# 
#     row_min = []  # 각 행에서 구한 가로 구간 최솟값을 저장할 빈 리스트.
# 
#     for r in range(m):  # range(m)은 0부터 m-1까지 순회.
#         row = rain[r * n:(r + 1) * n]  # [시작:끝] 슬라이스는 끝을 제외. r번째 행의 n칸 추출.
#         row_min.extend(window_minimum(row, w))  # 함수 호출 ()로 가로 최솟값을 구함. extend는 여러 원소를 이어 붙임.
# 
#     best_time = -1  # 모든 시각보다 작은 값으로 최적값 초기화.
#     answer = [0, 0]  # [0,0]은 행·열 두 값을 담은 리스트.
# 
#     for c in range(cols):  # 가능한 시작 열 c를 순회.
#         column = row_min[c::cols]  # [c::cols]는 c부터 cols 간격으로 추출. 같은 열만 모음.
#         area_times = window_minimum(column, h)  # 세로 h칸 최솟값으로 각 직사각형의 첫 빗방울 시각 계산.
# 
#         for r, time in enumerate(area_times):  # 각 시작 행 r와 구역의 첫 빗방울 시각 time을 순회.
#             if time > best_time or (  # or는 둘 중 하나가 참. 더 늦게 젖거나 동률 우선순위가 좋으면 갱신.
#                 time == best_time and [r, c] < answer  # ==는 같음. 리스트 <는 앞 원소부터 비교하므로 위쪽·왼쪽 우선.
#             ):  # )는 앞의 여러 줄 조건을 닫음. : 다음 들여쓰기는 if 본문.
#                 best_time = time  # 현재 더 좋은 시각을 저장.
#                 answer = [r, c]  # 선택한 왼쪽 위 좌표를 새 리스트에 저장.
# 
#     return answer  # 정답 좌표를 채점기에 반환.

# 풀이 요약
# 각 칸의 빗방울 시각을 기록하고, 가로·세로 단조 덱으로 직사각형의 첫 비 시각을 구합니다.
# 첫 비가 가장 늦는 좌표를 선택하고, 동률이면 위쪽·왼쪽을 우선합니다. 시간·공간 O(m*n).
# 