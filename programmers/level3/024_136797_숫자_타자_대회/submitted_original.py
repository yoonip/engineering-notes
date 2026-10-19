def solution(numbers):
    coordinates = [(3, 1)] + [divmod(number - 1, 3) for number in range(1, 10)]
    weights = [[0] * 10 for _ in range(10)]
    for first, (r1, c1) in enumerate(coordinates):
        for second, (r2, c2) in enumerate(coordinates):
            dr, dc = abs(r1 - r2), abs(c1 - c2)
            weights[first][second] = 3 * min(dr, dc) + 2 * abs(dr - dc) if first != second else 1
    dp = {(4, 6): 0}
    infinity = 10 ** 9
    for letter in numbers:
        target = int(letter)
        next_dp = {}
        for (left, right), cost in dp.items():
            if target != right:
                state = (target, right)
                next_dp[state] = min(next_dp.get(state, infinity), cost + weights[left][target])
            if target != left:
                state = (left, target)
                next_dp[state] = min(next_dp.get(state, infinity), cost + weights[right][target])
        dp = next_dp
    return min(dp.values())

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. numbers는 입력할 숫자 문자열.
#     coordinates = [(3, 1)] + [divmod(number - 1, 3) for number in range(1, 10)]  # [] 리스트와 + 결합. divmod는 (몫,나머지). 0은 (3,1), 1~9는 3열 자판 좌표.
#     weights = [[0] * 10 for _ in range(10)]  # 리스트 내포로 숫자 간 이동 비용 표 생성. _는 사용하지 않는 반복 변수.
#     for first, (r1, c1) in enumerate(coordinates):  # enumerate는 번호·좌표를 함께 제공, () 언패킹으로 행·열 분리.
#         for second, (r2, c2) in enumerate(coordinates):  # 도착 숫자 번호와 좌표 순회.
#             dr, dc = abs(r1 - r2), abs(c1 - c2)  # abs는 절댓값. 두 좌표의 행·열 차이.
#             weights[first][second] = 3 * min(dr, dc) + 2 * abs(dr - dc) if first != second else 1  # min은 작은 값. 가능한 만큼 대각선 3, 나머지 직선 2. 같은 키는 제자리 누르기 1.
#     dp = {(4, 6): 0}  # {} 딕셔너리. (왼손 위치,오른손 위치) 튜플을 키로 최소 비용 저장. 처음은 4·6, 비용 0.
#     infinity = 10 ** 9  # **는 거듭제곱. 아직 없는 다음 상태의 큰 기본 비용.
#     for letter in numbers:  # for~in으로 입력할 문자를 차례로 순회.
#         target = int(letter)  # int는 숫자 문자를 정수로 변환.
#         next_dp = {}  # 다음 문자를 누른 뒤의 위치별 최소 비용을 담을 빈 딕셔너리.
#         for (left, right), cost in dp.items():  # items는 (키,값) 제공. 튜플 키의 두 손 위치와 누적 비용 언패킹.
#             if target != right:  # if는 조건문, !=는 다름. 오른손이 이미 누를 숫자 위에 있으면 왼손으로 이동 금지.
#                 state = (target, right)  # 왼손만 이동한 다음 위치 튜플.
#                 next_dp[state] = min(next_dp.get(state, infinity), cost + weights[left][target])  # get은 없는 키에 기본값 반환. 같은 상태에 도달하는 비용 중 최소값 저장.
#             if target != left:  # 왼손이 목표 위에 있지 않을 때만 오른손으로 누를 수 있음.
#                 state = (left, target)  # 오른손만 이동한 위치.
#                 next_dp[state] = min(next_dp.get(state, infinity), cost + weights[right][target])  # 오른손 이동·누르기 비용을 더해 다음 상태 최소값 갱신.
#         dp = next_dp  # 다음 문자를 처리할 DP 표로 교체.
#     return min(dp.values())  # values는 딕셔너리 값들, min은 최소값. 마지막 손 위치에 상관없이 최소 비용 반환.

# 풀이 요약
# 두 손가락의 위치가 같을 수 없다는 조건을 지키며, 다음 숫자를 왼손·오른손으로 누르는 두 선택을 DP로 비교합니다.
# 이동 비용은 가능한 대각선을 3씩, 나머지 직선을 2씩 더하며 같은 키는 1입니다. 각 글자 직후에는 한 손이 그 글자 위에 있어 가능한 상태 수가 제한됩니다. 전체 시간 O(100L), 상태 공간 O(100) 이내입니다.
# 예: 이미 오른손이 6에 있을 때 6을 누르면 반드시 오른손으로 비용 1을 지불합니다. 다른 손을 6으로 옮기는 선택은 금지합니다.
# 