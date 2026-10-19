def solution(arr):
    numbers = list(map(int, arr[::2]))
    operators = arr[1::2]
    n = len(numbers)
    maximum = [[-10**9] * n for _ in range(n)]
    minimum = [[10**9] * n for _ in range(n)]
    for index, number in enumerate(numbers):
        maximum[index][index] = minimum[index][index] = number
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            for split in range(left, right):
                if operators[split] == '+':
                    high = maximum[left][split] + maximum[split + 1][right]
                    low = minimum[left][split] + minimum[split + 1][right]
                else:
                    high = maximum[left][split] - minimum[split + 1][right]
                    low = minimum[left][split] - maximum[split + 1][right]
                maximum[left][right] = max(maximum[left][right], high)
                minimum[left][right] = min(minimum[left][right], low)
    return maximum[0][n - 1]

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 숫자와 +·-가 번갈아 들어있는 문자열 리스트를 입력받음.
#     numbers = list(map(int, arr[::2]))  # [::2]는 두 칸 간격 슬라이스. map(int,...)는 숫자 문자열을 정수로 변환, list는 리스트 생성.
#     operators = arr[1::2]  # 1번 위치부터 두 칸 간격으로 연산자만 추출.
#     n = len(numbers)  # len은 길이. 숫자 개수를 구함.
#     maximum = [[-10**9] * n for _ in range(n)]  # 리스트 내포로 구간별 최댓값 표 생성. **는 거듭제곱이며 작은 값으로 초기화.
#     minimum = [[10**9] * n for _ in range(n)]  # 구간별 최솟값 표는 가능한 값보다 큰 수로 초기화.
#     for index, number in enumerate(numbers):  # enumerate는 (인덱스, 값)을 제공.
#         maximum[index][index] = minimum[index][index] = number  # 숫자 하나인 구간의 최대·최소는 그 숫자 자체.
#     for length in range(2, n + 1):  # 짧은 구간부터 길이 2~n을 순회하여 작은 구간을 먼저 계산.
#         for left in range(n - length + 1):  # 해당 길이 구간의 가능한 시작 인덱스 순회.
#             right = left + length - 1  # 구간의 마지막 숫자 인덱스 계산.
#             for split in range(left, right):  # 마지막으로 수행할 연산의 위치를 모두 검사.
#                 if operators[split] == '+':  # if는 조건문, ==는 같음 비교. 양쪽 구간을 더하는 경우.
#                     high = maximum[left][split] + maximum[split + 1][right]  # 합의 최댓값은 왼쪽 최대+오른쪽 최대.
#                     low = minimum[left][split] + minimum[split + 1][right]  # 합의 최솟값은 왼쪽 최소+오른쪽 최소.
#                 else:  # else는 뺄셈인 경우.
#                     high = maximum[left][split] - minimum[split + 1][right]  # 차의 최댓값은 왼쪽 최대-오른쪽 최소.
#                     low = minimum[left][split] - maximum[split + 1][right]  # 차의 최솟값은 왼쪽 최소-오른쪽 최대.
#                 maximum[left][right] = max(maximum[left][right], high)  # max는 큰 값 반환. 모든 분할 중 구간 최댓값 갱신.
#                 minimum[left][right] = min(minimum[left][right], low)  # min은 작은 값 반환. 모든 분할 중 구간 최솟값 갱신.
#     return maximum[0][n - 1]  # return으로 전체 숫자 구간의 최댓값 반환.

# 풀이 요약
# 숫자 순서를 유지한 모든 괄호 배치는 마지막 연산을 기준으로 왼쪽·오른쪽 연속 구간으로 나뉩니다. 모든 분할 위치를 비교합니다.
# 뺄셈 오른쪽에 오는 구간은 작을수록 좋으므로 최대와 최소를 함께 저장해야 합니다. 예: 1-(3+(5-8))=1.
# 숫자 개수 N에 대해 시간 O(N^3), 공간 O(N^2).
# 