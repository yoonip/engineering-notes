def solution(order):
    return sum(5000 if 'cafelatte' in item else 4500 for item in order)

# 전체 코드 줄별 설명
# def solution(order):  # def는 함수 정의. 주문 문자열 리스트 입력.
#     return sum(5000 if 'cafelatte' in item else 4500 for item in order)  # in은 문자열 포함 검사. 조건 표현식으로 라테는 5000, 나머지는 4500을 골라 sum으로 합산.

# 풀이 요약
# 온도에 따라 가격이 바뀌지 않으며 아무거나 주문은 아메리카노 가격입니다.
# 