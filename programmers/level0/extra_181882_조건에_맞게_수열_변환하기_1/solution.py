def solution(arr):
    return [x // 2 if x >= 50 and x % 2 == 0 else x * 2 if x < 50 and x % 2 == 1 else x for x in arr]

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 정수 리스트 입력.
#     return [x // 2 if x >= 50 and x % 2 == 0 else x * 2 if x < 50 and x % 2 == 1 else x for x in arr]  # 리스트 내포와 조건 표현식. and는 모두 참, %는 나머지, //는 정수 나눗셈. 조건별로 절반·두 배·원래 값 선택.

# 풀이 요약
# 50 이상 짝수는 절반, 50 미만 홀수는 두 배, 나머지는 그대로 둡니다.
# 