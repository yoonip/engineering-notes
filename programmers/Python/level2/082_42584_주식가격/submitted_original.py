def solution(prices):
    n = len(prices)
    answer = [n - index - 1 for index in range(n)]
    stack = []
    for index, price in enumerate(prices):
        while stack and prices[stack[-1]] > price:
            previous = stack.pop()
            answer[previous] = index - previous
        stack.append(index)
    return answer

# 전체 코드 줄별 설명
# def solution(prices):  # def는 함수 정의. prices는 초 단위 가격 목록 입력.
#     n = len(prices)  # len은 원소 수. =는 대입.
#     answer = [n - index - 1 for index in range(n)]  # 리스트 내포·range로 끝까지 떨어지지 않는 기본 유지 기간 생성.
#     stack = []  # []는 빈 스택. 아직 가격 하락 시점을 못 찾은 인덱스 저장.
#     for index, price in enumerate(prices):  # enumerate는 (인덱스,값) 제공. 현재 시점·가격 언패킹.
#         while stack and prices[stack[-1]] > price:  # while은 반복, and는 둘 다 참. [-1]은 스택 위. 이전 가격보다 낮아진 시점 검사.
#             previous = stack.pop()  # pop으로 하락 시점이 확정된 인덱스를 꺼내 삭제.
#             answer[previous] = index - previous  # [] 원소에 대입. 하락한 현재 시점까지의 시간 차 저장.
#         stack.append(index)  # append로 현재 시점을 대기 스택에 추가.
#     return answer  # return으로 가격별 유지 기간 목록 반환.

# 풀이 요약
# 가격 하락을 기다리는 시점들을 스택에 모으고, 더 낮은 가격이 오면 해당 시점들의 기간을 확정합니다. 끝까지 남으면 마지막 초까지의 기간입니다.
# 예: [1,2,3,2,3]의 3은 1초 뒤 하락해 [4,3,1,1,0]. 시간·공간 O(N).
