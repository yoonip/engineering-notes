# sequence는 원래 정수 수열 목록.
def solution(sequence):
    # 빈 앞부분도 포함.
    prefix = lowest = highest = 0
    # for는 순회, enumerate는 (인덱스, 값) 제공.
    for index, value in enumerate(sequence):
        # +=는 더해 저장.
        prefix += value if index % 2 == 0 else -value
        # 지금까지의 가장 작은 누적합 갱신.
        lowest = min(lowest, prefix)
        # 가장 큰 누적합 갱신.
        highest = max(highest, prefix)
    # 반대 펄스를 고를 수 있어 차이의 부호는 언제든 양수로 바꿀 수 있음.
    return highest - lowest
