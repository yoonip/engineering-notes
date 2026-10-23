from collections import Counter

def solution(numbers, target):
    ways = Counter({0: 1})
    for number in numbers:
        next_ways = Counter()
        for total, count in ways.items():
            next_ways[total + number] += count
            next_ways[total - number] += count
        ways = next_ways
    return ways[target]

# 전체 코드 줄별 설명
# from collections import Counter  # collections의 Counter를 import. 합별로 그 합을 만드는 방법 수를 저장하는 딕셔너리형 자료구조.
# 
# def solution(numbers, target):  # def는 함수 정의. 숫자 목록·목표 합 입력.
#     ways = Counter({0: 1})  # {}는 딕셔너리. 숫자를 사용하기 전 합 0을 만드는 방법은 1개.
#     for number in numbers:  # for~in으로 숫자를 주어진 순서대로 처리.
#         next_ways = Counter()  # 다음 숫자까지 사용한 방법 수를 담을 빈 Counter.
#         for total, count in ways.items():  # items는 (합,방법 수) 제공. 두 변수로 언패킹.
#             next_ways[total + number] += count  # [키] 접근, +=는 더해 저장. 이번 숫자를 더하는 모든 방법 누적.
#             next_ways[total - number] += count  # 이번 숫자를 빼는 모든 방법 누적. 같은 합은 횟수를 합침.
#         ways = next_ways  # =로 다음 단계의 방법 수 표로 교체.
#     return ways[target]  # Counter의 없는 키는 0. return으로 목표 합을 만드는 방법 수 반환.

# 풀이 요약
# 각 숫자마다 가능한 합에 +와 -를 적용하고, 같은 합에 도달한 방법 수를 더합니다.
# 예: 1 다섯 개로 3을 만들려면 한 개만 음수여야 하므로 5가지. 숫자 N개·절댓값 합 S일 때 시간 O(NS), 공간 O(S).
