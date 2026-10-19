def solution(my_string, n):
    return my_string[:n]

# 전체 코드 줄별 설명
# def solution(my_string, n):  # def는 함수 정의. 문자열과 가져올 글자 수 입력.
#     return my_string[:n]  # [:n]은 처음부터 인덱스 n 직전까지 잘라 앞 n글자 반환.

# 풀이 요약
# 슬라이싱의 끝 인덱스는 포함되지 않으므로 n을 그대로 사용합니다.
# 