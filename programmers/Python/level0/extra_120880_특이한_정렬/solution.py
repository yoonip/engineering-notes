def solution(numlist, n):
    return sorted(numlist, key=lambda x: (abs(x - n), -x))

# 전체 코드 줄별 설명
# def solution(numlist, n):  # def는 함수 정의. 후보 정수 리스트와 기준값 입력.
#     return sorted(numlist, key=lambda x: (abs(x - n), -x))  # sorted는 정렬, lambda는 익명 기준 함수, abs는 절댓값. 거리 우선, 동률이면 -x를 사용해 큰 수 우선.

# 풀이 요약
# 정렬 기준을 (거리,음수 값)으로 지정해 동률일 때 큰 수를 앞에 둡니다.
# 