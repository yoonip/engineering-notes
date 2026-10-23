def solution(strs, t):
    pieces = set(strs)
    lengths = sorted({len(piece) for piece in pieces})
    n = len(t)
    dp = [n + 1] * (n + 1)
    dp[0] = 0
    for end in range(1, n + 1):
        for size in lengths:
            if size > end:
                break
            start = end - size
            if t[start:end] in pieces:
                dp[end] = min(dp[end], dp[start] + 1)
    return dp[n] if dp[n] <= n else -1

# 전체 코드 줄별 설명
# def solution(strs, t):  # def는 함수 정의. 사용 가능한 조각 목록과 목표 문자열을 입력받음.
#     pieces = set(strs)  # set은 중복 없는 집합. 문자열 조각 포함 여부를 빠르게 검사.
#     lengths = sorted({len(piece) for piece in pieces})  # {} 집합 내포로 조각 길이를 중복 없이 모으고 sorted로 오름차순 정렬.
#     n = len(t)  # len은 문자열 길이. 목표 문자열 전체 길이.
#     dp = [n + 1] * (n + 1)  # dp[i]는 앞 i글자를 만드는 최소 조각 수. n+1은 불가능 표시.
#     dp[0] = 0  # 빈 문자열은 조각 0개로 만들 수 있음.
#     for end in range(1, n + 1):  # range는 끝을 제외하므로 앞 1글자부터 n글자까지 순회.
#         for size in lengths:  # 마지막에 붙일 조각의 가능한 길이 순회.
#             if size > end:  # if는 조건문. 현재 접두사보다 긴 조각은 사용할 수 없음.
#                 break  # 길이가 정렬되어 있으므로 이후 길이도 모두 건너뛰며 내부 반복 종료.
#             start = end - size  # 마지막 조각의 시작 인덱스 계산.
#             if t[start:end] in pieces:  # [시작:끝]은 끝을 제외한 슬라이스, in은 집합 포함 검사. 끝 조각이 실제로 있는지 확인.
#                 dp[end] = min(dp[end], dp[start] + 1)  # min은 작은 값 반환. 앞부분의 최소 조각 수에 이번 조각 하나를 더해 갱신.
#     return dp[n] if dp[n] <= n else -1  # 조건 표현식. 전체를 만들었으면 최소 개수, 불가능하면 -1 반환.

# 풀이 요약
# 목표의 앞 i글자를 만드는 최솟값을 저장하고, 마지막 조각의 길이 1~5를 검사하여 앞부분 DP와 연결합니다. 조각은 반복 사용 가능합니다.
# 예: banana는 ba+na+na로 3개, apple은 ap+ple로 2개입니다.
# 조각 최대 길이가 5로 고정되어 목표 길이 N에 대해 시간 O(N), 공간 O(N+조각 수).
# 