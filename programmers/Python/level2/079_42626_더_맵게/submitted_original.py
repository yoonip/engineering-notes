from heapq import heapify, heappop, heappush

def solution(scoville, K):
    heapify(scoville)
    answer = 0
    while scoville[0] < K:
        if len(scoville) < 2:
            return -1
        first = heappop(scoville)
        second = heappop(scoville)
        heappush(scoville, first + second * 2)
        answer += 1
    return answer

# 전체 코드 줄별 설명
# from heapq import heapify, heappop, heappush  # heapq는 최소 힙 모듈. heapify는 힙 구성, heappop은 최솟값 제거, heappush는 새 값 추가.
# 
# def solution(scoville, K):  # def는 함수 정의. 음식 스코빌 목록·목표 지수 입력.
#     heapify(scoville)  # 리스트를 제자리 최소 힙으로 바꿈. 인덱스 0이 항상 최솟값.
#     answer = 0  # =는 대입. 섞은 횟수 초기화.
#     while scoville[0] < K:  # while은 반복, []는 접근, <는 작음. 최솟값이 목표 미만이면 섞어야 함.
#         if len(scoville) < 2:  # len은 원소 수. 음식이 하나면 더 섞을 수 없음.
#             return -1  # 목표 달성이 불가능하므로 -1 반환.
#         first = heappop(scoville)  # 가장 작은 음식 하나 꺼내기.
#         second = heappop(scoville)  # 남은 것 중 가장 작은 음식, 즉 원래 둘째 음식 꺼내기.
#         heappush(scoville, first + second * 2)  # *는 곱셈. 지정 공식으로 만든 음식을 힙에 추가.
#         answer += 1  # +=는 더해 저장. 섞은 횟수 증가.
#     return answer  # 최솟값이 K 이상이면 전체가 조건을 만족하므로 횟수 반환.

# 풀이 요약
# 최소 힙으로 매번 가장 작은 두 음식을 골라 섞습니다. 최솟값만 확인하면 모든 음식이 K 이상인지 알 수 있습니다.
# 예: 1+2×2=5, 이어서 3+5×2=13으로 두 번. 음식 N개일 때 시간 O(N log N), 힙 공간 O(N).
