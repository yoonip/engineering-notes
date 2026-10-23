def solution(n, m, timetable):
    delta = [0] * 1322
    for start, end in timetable:
        delta[start] += 1
        delta[end + 1] -= 1
    current = peak = 0
    for change in delta:
        current += change
        peak = max(peak, current)
    if peak <= 1:
        return 0
    for distance in range(2 * n - 2, 0, -1):
        for offset in range(n):
            placed = []
            for position in range(offset, n * n):
                row, col = divmod(position, n)
                if all(abs(row - r) + abs(col - c) >= distance for r, c in placed):
                    placed.append((row, col))
                    if len(placed) == peak:
                        return distance
    return 1

# 전체 코드 줄별 설명
# def solution(n, m, timetable):  # def는 함수 정의. 락커 한 변·손님 수·예약 목록 입력.
#     delta = [0] * 1322  # []는 리스트, *는 반복. 분별 입퇴실 인원 변화량 저장.
#     for start, end in timetable:  # for로 입실·퇴실 시각 언패킹.
#         delta[start] += 1  # +=는 더해 저장. 입실 시각부터 한 명 사용.
#         delta[end + 1] -= 1  # 퇴실 시각도 이용하므로 그 다음 분부터 감소.
#     current = peak = 0  # 연쇄 대입. 현재·최대 동시 이용 인원 초기화.
#     for change in delta:  # 시간순 변화량 누적.
#         current += change  # 현재 동시 이용 인원 갱신.
#         peak = max(peak, current)  # max는 최댓값. 필요한 최대 락커 수.
#     if peak <= 1:  # 동시에 두 명 이상인 적이 없으면 거리 0.
#         return 0  # return은 결과 반환.
#     for distance in range(2 * n - 2, 0, -1):  # range의 세 번째 값 -1은 감소. 가장 큰 거리부터 검사.
#         for offset in range(n):  # 첫 행의 첫 배치 열을 모두 바꿔 검사. 모서리만 고집하지 않음.
#             placed = []  # 선택한 락커 좌표 목록.
#             for position in range(offset, n * n):  # 첫 위치 뒤부터 행 우선 순서로 칸을 확인.
#                 row, col = divmod(position, n)  # divmod는 몫·나머지. 1차원 번호를 행·열로 변환.
#                 if all(abs(row - r) + abs(col - c) >= distance for r, c in placed):  # all은 모든 조건, abs는 절댓값. 기존 배치와 맨해튼 거리를 검사.
#                     placed.append((row, col))  # append는 추가, ()는 튜플. 조건을 만족하는 칸 배치.
#                     if len(placed) == peak:  # len은 개수. 최대 동시 인원만큼 배치했는지 확인.
#                         return distance  # 큰 거리부터 검사했으므로 첫 성공 거리 반환.
#     return 1  # 모든 락커를 써도 최소 거리 1은 보장.

# 풀이 요약
# 예약 구간의 양 끝을 포함해 최대 동시 인원 K를 센다. K개의 충분히 떨어진 락커를 준비하면 예약은 빈 락커로 배정할 수 있다.
# 거리를 큰 값부터 내리며 첫 행의 시작 열을 바꾼 행 우선 배치를 검사한다. 첫 모서리만 쓰면 n=4,K=3의 거리 4 배치를 놓칠 수 있다.
# 거리 후보 O(N), 시작 열 O(N), 칸 O(N²), 거리 비교 O(N²)로 상한 O(N⁶). N≤10이며 인원을 채우면 즉시 종료한다.
# 