def solution(str1, str2):
    return 1 if str2 in str1 else 2

# 전체 코드 줄별 설명
# def solution(str1, str2):  # def는 함수 정의. 원본 문자열과 찾을 부분 문자열 입력.
#     return 1 if str2 in str1 else 2  # in은 연속 부분 문자열 포함 검사. 조건 표현식으로 포함되면 1, 없으면 2 반환.

# 풀이 요약
# 문제에서 미포함 결과를 0이 아닌 2로 요구하는 점을 주의합니다.
# 