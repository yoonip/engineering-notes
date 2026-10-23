def solution(str1, str2):
    return int(str1 in str2)

# 전체 코드 줄별 설명
# def solution(str1, str2):  # def는 함수 정의. 찾을 문자열과 원본 문자열 입력.
#     return int(str1 in str2)  # in은 왼쪽 문자열이 오른쪽에 포함되는지 검사. int는 결과를 1·0으로 변환.

# 풀이 요약
# 포함 관계의 방향을 주의해 str1이 str2 안에 있는지 확인합니다.
# 