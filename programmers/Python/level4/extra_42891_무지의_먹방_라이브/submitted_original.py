def solution(food_times, k):
    if sum(food_times) <= k:
        return -1
    foods = sorted((time, index + 1) for index, time in enumerate(food_times))
    n = len(foods)
    previous = 0
    for position, (time, number) in enumerate(foods):
        remaining = n - position
        cost = (time - previous) * remaining
        if cost > k:
            order = sorted(number for time, number in foods[position:])
            return order[k % remaining]
        k -= cost
        previous = time
    return -1

# 전체 코드 줄별 설명
# def solution(food_times, k):  # def는 함수 정의. 음식별 남은 시간과 방송 중단 시각을 입력받음.
#     if sum(food_times) <= k:  # sum은 합계. 중단 전에 음식을 모두 먹었는지 검사.
#         return -1  # return은 함수 종료. 남은 음식이 없다는 표시 반환.
#     foods = sorted((time, index + 1) for index, time in enumerate(food_times))  # enumerate는 인덱스·값 제공. (시간, 1부터 시작하는 번호) 튜플을 시간순 정렬.
#     n = len(foods)  # len은 길이. 전체 음식 개수.
#     previous = 0  # 모든 남은 음식에서 공통으로 먹은 층의 높이 초기화.
#     for position, (time, number) in enumerate(foods):  # 중첩 언패킹으로 정렬 위치와 음식 정보를 나눠 받음.
#         remaining = n - position  # 아직 제거하지 않은 음식 개수.
#         cost = (time - previous) * remaining  # 다음 음식이 소진될 때까지 모든 음식에서 같은 층을 먹는 총시간.
#         if cost > k:  # if는 조건문. 남은 시간으로 이 층 전체를 먹을 수 없으면 실행.
#             order = sorted(number for time, number in foods[position:])  # [position:]은 남은 구간 슬라이스. 음식 번호순으로 다시 정렬.
#             return order[k % remaining]  # %는 나머지. 남은 음식 사이의 완전한 회전을 생략하고 다음 음식 번호 반환.
#         k -= cost  # -=는 뺀 값 저장. 완전히 먹을 수 있는 층의 시간을 한 번에 차감.
#         previous = time  # 모두 먹은 층의 높이를 이번 음식 시간까지 올림.
#     return -1  # 전체를 소진한 경우의 기본 반환값.

# 풀이 요약
# 매초 하나씩 먹는 대신, 남은 음식 모두에서 다음 음식이 소진될 때까지 같은 층을 한꺼번에 제거합니다.
# 한 층 전체를 제거할 시간이 부족해지면 남은 음식을 원래 번호순으로 정렬하고 k의 나머지 위치를 고릅니다. 예: [3,1,2], k=5의 답은 1.
# 음식 수 N에 대해 시간 O(N*log N), 공간 O(N).
# 