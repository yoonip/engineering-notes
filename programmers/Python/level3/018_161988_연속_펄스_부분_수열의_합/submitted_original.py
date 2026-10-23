def solution(sequence):
    prefix = lowest = highest = 0
    for index, value in enumerate(sequence):
        prefix += value if index % 2 == 0 else -value
        lowest = min(lowest, prefix)
        highest = max(highest, prefix)
    return highest - lowest

# 전체 코드 줄별 설명
# def solution(sequence):  # def는 함수 정의. sequence는 원래 정수 수열 목록.
#     prefix = lowest = highest = 0  # 연쇄 대입. 현재 누적합과 누적합의 최솟값·최댓값을 모두 0으로 초기화. 빈 앞부분도 포함.
#     for index, value in enumerate(sequence):  # for는 순회, enumerate는 (인덱스, 값) 제공.
#         prefix += value if index % 2 == 0 else -value  # %는 나머지, ==는 같음. 짝수 위치에는 +1, 홀수 위치에는 -1을 곱해 누적. +=는 더해 저장.
#         lowest = min(lowest, prefix)  # min은 작은 값. 지금까지의 가장 작은 누적합 갱신.
#         highest = max(highest, prefix)  # max는 큰 값. 가장 큰 누적합 갱신.
#     return highest - lowest  # return으로 누적합 최대 차이 반환. 반대 펄스를 고를 수 있어 차이의 부호는 언제든 양수로 바꿀 수 있음.

# 풀이 요약
# 전체 수열에 +1,-1을 번갈아 곱한 뒤 누적합을 구합니다. 어떤 구간의 합은 두 누적합의 차이입니다.
# 반대 부호의 펄스도 허용되므로 구간 합 절댓값의 최댓값을 찾으면 됩니다. 이는 전체 누적합의 최댓값-최솟값입니다. 시간 O(N), 추가 공간 O(1).
# 예: [2,3,-6,1,3,-1,2,4]를 변환한 누적합은 0,2,-1,-7,-8,-5,-4,-2,-6. 최대 2와 최소 -8의 차이는 10입니다.
