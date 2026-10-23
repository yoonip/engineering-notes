def solution(angle):
    if angle < 90:
        return 1
    if angle == 90:
        return 2
    if angle < 180:
        return 3
    return 4

# 전체 코드 줄별 설명
# def solution(angle):  # def는 함수 정의. 1~180도의 각도 입력.
#     if angle < 90:  # if는 조건, <는 미만 비교. 예각 검사.
#         return 1  # 예각 번호 반환.
#     if angle == 90:  # ==는 같음 비교. 직각 검사.
#         return 2  # 직각 번호 반환.
#     if angle < 180:  # 앞 경우를 제외했으므로 90 초과 180 미만의 둔각 검사.
#         return 3  # 둔각 번호 반환.
#     return 4  # 남은 180도는 평각.

# 풀이 요약
# 90도와 180도의 경계값을 별도로 구분합니다.
# 