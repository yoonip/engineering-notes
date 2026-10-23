# numbers는 입력할 숫자 문자열.
def solution(numbers):
    # 0은 (3,1), 1~9는 3열 자판 좌표.
    coordinates = [(3, 1)] + [divmod(number - 1, 3) for number in range(1, 10)]
    # _는 사용하지 않는 반복 변수.
    weights = [[0] * 10 for _ in range(10)]
    # enumerate는 번호·좌표를 함께 제공, () 언패킹으로 행·열 분리.
    for first, (r1, c1) in enumerate(coordinates):
        # 도착 숫자 번호와 좌표 순회.
        for second, (r2, c2) in enumerate(coordinates):
            # 두 좌표의 행·열 차이.
            dr, dc = abs(r1 - r2), abs(c1 - c2)
            # 같은 키는 제자리 누르기 1.
            weights[first][second] = 3 * min(dr, dc) + 2 * abs(dr - dc) if first != second else 1
    # 처음은 4·6, 비용 0.
    dp = {(4, 6): 0}
    # 아직 없는 다음 상태의 큰 기본 비용.
    infinity = 10 ** 9
    # for~in으로 입력할 문자를 차례로 순회.
    for letter in numbers:
        # int는 숫자 문자를 정수로 변환.
        target = int(letter)
        # 다음 문자를 누른 뒤의 위치별 최소 비용을 담을 빈 딕셔너리.
        next_dp = {}
        # 튜플 키의 두 손 위치와 누적 비용 언패킹.
        for (left, right), cost in dp.items():
            # 오른손이 이미 누를 숫자 위에 있으면 왼손으로 이동 금지.
            if target != right:
                # 왼손만 이동한 다음 위치 튜플.
                state = (target, right)
                # 같은 상태에 도달하는 비용 중 최소값 저장.
                next_dp[state] = min(next_dp.get(state, infinity), cost + weights[left][target])
            # 왼손이 목표 위에 있지 않을 때만 오른손으로 누를 수 있음.
            if target != left:
                # 오른손만 이동한 위치.
                state = (left, target)
                # 오른손 이동·누르기 비용을 더해 다음 상태 최소값 갱신.
                next_dp[state] = min(next_dp.get(state, infinity), cost + weights[right][target])
        # 다음 문자를 처리할 DP 표로 교체.
        dp = next_dp
    # 마지막 손 위치에 상관없이 최소 비용 반환.
    return min(dp.values())
