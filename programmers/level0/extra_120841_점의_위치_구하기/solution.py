def solution(dot):
    x, y = dot
    if y > 0:
        return 1 if x > 0 else 2
    return 4 if x > 0 else 3

# 전체 코드 줄별 설명
# def solution(dot):  # def는 함수 정의. 점의 x·y 좌표 리스트 입력.
#     x, y = dot  # 두 좌표를 각각 변수에 나누어 대입.
#     if y > 0:  # if는 조건, >는 초과 비교. 위쪽 반평면인지 확인.
#         return 1 if x > 0 else 2  # 조건 표현식. 위쪽에서 x 양수는 1사분면, 음수는 2사분면.
#     return 4 if x > 0 else 3  # 아래쪽에서 x 양수는 4사분면, 음수는 3사분면.

# 풀이 요약
# y의 부호로 위·아래를 나눈 뒤 x의 부호로 좌·우를 구분합니다.
# 