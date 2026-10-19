def solution(numbers, num1, num2):
    return numbers[num1:num2 + 1]

# 전체 코드 줄별 설명
# def solution(numbers, num1, num2):  # def는 함수 정의. 정수 리스트와 자를 양 끝 인덱스 입력.
#     return numbers[num1:num2 + 1]  # [시작:끝] 슬라이싱의 끝은 제외. num2를 포함하도록 1을 더함.

# 풀이 요약
# 인덱스 num1부터 num2까지 양 끝을 포함해 잘라냅니다.
# 