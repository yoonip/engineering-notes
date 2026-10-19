def solution(number):
    return sum(int(char) for char in number) % 9

# 전체 코드 줄별 설명
# def solution(number):  # def는 함수 정의. 아주 긴 숫자 문자열 입력.
#     return sum(int(char) for char in number) % 9  # int는 한 자리 숫자 변환, sum은 합계, %는 나머지. 자릿수 합을 9로 나눈 나머지 반환.

# 풀이 요약
# 전체 숫자를 정수로 바꾸지 않고 각 자리 합을 구해 긴 입력도 처리합니다.
# 