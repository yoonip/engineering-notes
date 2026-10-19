def solution(money):
    return [money // 5500, money % 5500]

# 전체 코드 줄별 설명
# def solution(money):  # def는 함수 정의. 가진 돈 입력.
#     return [money // 5500, money % 5500]  # //는 정수 나눗셈의 몫, %는 나머지. 살 수 있는 잔 수와 남은 돈을 리스트로 반환.

# 풀이 요약
# 가격 5500원으로 나눈 몫과 나머지를 사용합니다.
# 