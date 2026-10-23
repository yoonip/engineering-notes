def solution(num, total):
    start = (total - num * (num - 1) // 2) // num
    return list(range(start, start + num))

# 전체 코드 줄별 설명
# def solution(num, total):  # def는 함수 정의. 연속된 정수 개수와 합계 입력.
#     start = (total - num * (num - 1) // 2) // num  # //는 정수 나눗셈. 합계=시작값*num+0부터 num-1까지의 합을 이용해 시작값 계산.
#     return list(range(start, start + num))  # range는 끝 제외 연속 정수 생성, list는 리스트 변환. num개 정수 반환.

# 풀이 요약
# 연속된 수를 시작값+x로 표현하고 0부터 num-1까지의 합을 빼 시작값을 역산합니다.
# 