from collections import Counter

def solution(want, number, discount):
    needed = dict(zip(want, number))
    answer = 0
    for start in range(len(discount) - 9):
        current = Counter(discount[start:start + 10])
        if current == needed:
            answer += 1
    return answer

# 전체 코드 줄별 설명
# from collections import Counter  # collections의 Counter를 import. 상품별 등장 횟수를 세는 딕셔너리형 자료구조.
# 
# def solution(want, number, discount):  # def는 함수 정의. 원하는 상품·수량·날짜별 할인 상품이 입력.
#     needed = dict(zip(want, number))  # zip은 같은 위치의 원소끼리 묶음, dict는 (키,값) 쌍을 딕셔너리로 변환.
#     answer = 0  # =는 대입. 가입 가능한 시작 날짜 수 초기화.
#     for start in range(len(discount) - 9):  # len은 길이, range는 끝 미포함. 온전한 10일 구간의 시작점만 순회.
#         current = Counter(discount[start:start + 10])  # [시작:끝]은 끝 미포함 슬라이스. 해당 열흘의 상품 개수 집계.
#         if current == needed:  # if는 조건 분기, ==는 키·값의 일치 검사. 상품 순서와 무관하게 수량 비교.
#             answer += 1  # +=는 더해 저장. 가능한 날짜 하나 누적.
#     return answer  # return으로 가입 가능한 총 날짜 수 반환.

# 풀이 요약
# 연속한 열흘마다 할인 상품 개수를 세어 원하는 상품별 수량과 비교합니다. 필요한 수량 합이 10이라 정확히 일치해야 합니다.
# 예: 첫 예제는 3·4·5일 시작이 가능해 3. 할인 날짜 D개일 때 시간 O(10D), 구간 집계 공간 O(10).
