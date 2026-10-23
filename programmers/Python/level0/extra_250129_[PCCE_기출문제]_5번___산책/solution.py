def solution(route):
    east = 0
    north = 0
    for i in route:
        if i == "N":
            north += 1
        elif i == "S":
            north -= 1
        elif i == "E":
            east += 1
        elif i == "W":
            east -= 1
    return [east, north]

# 전체 코드 줄별 설명
# def solution(route):  # def는 함수 정의. route는 방향 문자열.
#     east = 0  # 동쪽 방향 이동량 초기화.
#     north = 0  # 북쪽 방향 이동량 초기화.
#     for i in route:  # for는 문자열에서 문자를 하나씩 순회.
#         if i == "N":  # if는 조건, ==는 같음 비교. 북쪽 이동인지 확인.
#             north += 1  # +=는 더해 저장. 북쪽 좌표 증가.
#         elif i == "S":  # elif는 다음 조건. 남쪽 이동 검사.
#             north -= 1  # -=는 빼서 저장. 북쪽 좌표 감소.
#         elif i == "E":  # 동쪽 이동 검사.
#             east += 1  # 동쪽 좌표 증가.
#         elif i == "W":  # 서쪽 이동 검사.
#             east -= 1  # 동쪽 좌표 감소.
#     return [east, north]  # []는 리스트, return은 결과 반환. 동쪽·북쪽 좌표 순서로 반환.

# 풀이 요약
# 동서 이동은 east, 남북 이동은 north에 각각 누적합니다. 반대 방향은 음수로 더합니다.
# 