def solution(array):
    return sum(str(value).count('7') for value in array)

# 전체 코드 줄별 설명
# def solution(array):  # def는 함수 정의. 정수 리스트 입력.
#     return sum(str(value).count('7') for value in array)  # str은 정수의 문자열 변환, count는 문자 출현 횟수, sum은 모든 수에서 센 횟수 합산.

# 풀이 요약
# 각 정수를 문자열로 바꿔 숫자 문자 7의 출현 횟수를 셉니다.
# 