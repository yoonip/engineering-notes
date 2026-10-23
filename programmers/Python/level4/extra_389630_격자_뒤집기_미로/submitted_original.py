def solution(visible, hidden, k):
    n, m = len(visible), len(visible[0])
    must_skip = n % 2 == 0 and m % 2 == 0
    answer = -10**9
    for mask in range(1 << n):
        flips = [(mask >> r) & 1 for r in range(n)]
        total = -k * mask.bit_count()
        best_loss = -10**9
        for c in range(m):
            front = back = 0
            low_front = low_back = 101
            for r in range(n):
                a, b = visible[r][c], hidden[r][c]
                if flips[r]:
                    a, b = b, a
                front += a
                back += b
                if must_skip and (r + c) % 2:
                    low_front = min(low_front, a)
                    low_back = min(low_back, b)
            normal = max(front, back - k)
            total += normal
            if must_skip:
                reduced = max(front - low_front, back - low_back - k)
                best_loss = max(best_loss, reduced - normal)
        if must_skip:
            total += best_loss
        answer = max(answer, total)
    return answer

# 전체 코드 줄별 설명
# def solution(visible, hidden, k):  # def는 함수를 정의. 두 면의 격자와 뒤집기 비용 k를 입력받음.
#     n, m = len(visible), len(visible[0])  # len은 길이. n은 행 수, m은 열 수이며 쉼표로 두 변수에 대입.
#     must_skip = n % 2 == 0 and m % 2 == 0  # %는 나머지, and는 두 조건 모두 참. 양쪽 길이가 짝수면 한 칸을 제외해야 함.
#     answer = -10**9  # **는 거듭제곱. 어떤 가능한 점수보다 작은 값으로 최댓값 초기화.
#     for mask in range(1 << n):  # <<는 비트 왼쪽 이동. 2의 n제곱개 행 뒤집기 조합을 순회.
#         flips = [(mask >> r) & 1 for r in range(n)]  # 리스트 내포. >>와 &로 각 행을 뒤집는지 0 또는 1로 추출.
#         total = -k * mask.bit_count()  # bit_count()는 1인 비트 수. 뒤집은 행 개수만큼 비용 차감.
#         best_loss = -10**9  # 제외할 칸으로 인한 최선의 점수 변화량을 저장.
#         for c in range(m):  # for로 열을 하나씩 순회. range(m)은 0부터 m-1까지.
#             front = back = 0  # 연쇄 대입으로 열을 그대로 두거나 뒤집을 때의 합을 0으로 초기화.
#             low_front = low_back = 101  # 각 칸은 최대 100. 제외 가능한 칸의 최솟값 초기화.
#             for r in range(n):  # 이번 열의 모든 행을 순회.
#                 a, b = visible[r][c], hidden[r][c]  # [][]는 2차원 리스트의 행·열 접근. 양면 값을 가져옴.
#                 if flips[r]:  # if는 조건문. 이 행을 뒤집는 경우 실행.
#                     a, b = b, a  # 동시 대입으로 두 값을 교환하여 행 뒤집기 반영.
#                 front += a  # +=는 더한 값을 다시 저장. 열을 유지할 때의 합.
#                 back += b  # 열까지 뒤집으면 반대 면이 보이므로 b를 합산.
#                 if must_skip and (r + c) % 2:  # 행·열이 모두 짝수면 체스판의 홀수 색 칸 하나를 제외할 수 있음.
#                     low_front = min(low_front, a)  # min은 작은 값 반환. 열 유지 시 제외할 최소 칸 값 갱신.
#                     low_back = min(low_back, b)  # 열 뒤집기 시 제외할 최소 칸 값 갱신.
#             normal = max(front, back - k)  # max는 큰 값 반환. 이 열의 뒤집기 비용까지 반영한 최선의 합.
#             total += normal  # 각 열의 독립적인 최선 점수를 전체 점수에 추가.
#             if must_skip:  # 짝수×짝수 격자에만 한 칸 제외 조건 적용.
#                 reduced = max(front - low_front, back - low_back - k)  # 제외할 칸을 뺀 뒤 두 열 방향 중 최선 선택.
#                 best_loss = max(best_loss, reduced - normal)  # 한 열에서만 칸을 제외하므로 가장 손해가 작은 변화량 저장.
#         if must_skip:  # 한 칸을 반드시 제외해야 하면 실행.
#             total += best_loss  # 모든 열 중 가장 유리한 한 칸 제외 결과를 반영.
#         answer = max(answer, total)  # 모든 행 뒤집기 조합 중 최대 점수 유지.
#     return answer  # return은 최종 점수를 반환하고 함수를 끝냄.

# 풀이 요약
# 양쪽 길이가 짝수면 홀수 색 칸 하나만 빼고, 그 외에는 모든 칸을 방문하는 경로가 있습니다. 양수 점수라 더 뺄 필요가 없습니다.
# 행 뒤집기 2^n가지를 고정하면 각 열은 독립적으로 선택됩니다. 짝수×짝수에서는 한 칸 제외 손실도 함께 비교합니다.
# 예: [[1,2],[3,4]], 숨은 면 [[5,6],[7,8]], k=0이면 5+7+8=20. 시간 O(2^n*n*m), 추가 공간 O(n).
# 