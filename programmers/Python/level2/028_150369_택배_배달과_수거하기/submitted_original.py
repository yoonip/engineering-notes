def solution(cap, n, deliveries, pickups):
    delivery = pickup = answer = 0
    for index in range(n - 1, -1, -1):
        delivery += deliveries[index]
        pickup += pickups[index]
        trips = max(0, (delivery + cap - 1) // cap, (pickup + cap - 1) // cap)
        answer += trips * (index + 1) * 2
        delivery -= trips * cap
        pickup -= trips * cap
    return answer

# 전체 코드 줄별 설명
# def solution(cap, n, deliveries, pickups):  # def는 함수 정의. ()는 적재량·집 수·배달량·수거량 입력.
#     delivery = pickup = answer = 0  # 연쇄 대입. 처리할 물량과 총 거리 초기화. 음수 물량은 이전 운행의 남는 용량.
#     for index in range(n - 1, -1, -1):  # range(시작,끝,간격)으로 마지막 집부터 0번까지 역순 순회.
#         delivery += deliveries[index]  # []는 원소 접근, +=는 더해 저장. 이 집의 배달 물량 반영.
#         pickup += pickups[index]  # 이 집의 수거 물량도 반영.
#         trips = max(0, (delivery + cap - 1) // cap, (pickup + cap - 1) // cap)  # //는 정수 몫. 올림 나눗셈으로 필요한 추가 왕복 수를 구해 max로 큰 쪽 선택.
#         answer += trips * (index + 1) * 2  # *는 곱셈. 해당 집까지의 왕복 거리를 추가 운행 수만큼 누적.
#         delivery -= trips * cap  # -=는 빼서 저장. 추가 왕복의 배달 용량을 반영하고 남는 용량을 음수로 유지.
#         pickup -= trips * cap  # 수거 용량도 반영. 더 가까운 집을 처리할 때 남는 용량 활용.
#     return answer  # return으로 최소 총 왕복 거리 반환.

# 풀이 요약
# 먼 집부터 필요한 왕복을 확정합니다. 한 왕복에서 배달·수거를 각각 cap개까지 처리하고 남는 용량은 가까운 집에 씁니다.
# 예: 첫 예제는 5번·3번 집까지 왕복해 10+6=16. 시간 O(N), 추가 공간 O(1).
