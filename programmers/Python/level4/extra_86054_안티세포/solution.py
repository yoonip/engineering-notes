def solution(a, s):
    mod = 1_000_000_007  # 정답을 나눌 수. _는 숫자 자릿수 구분자.
    answer = []  # []는 빈 리스트. 각 배열의 정답 저장.
    offset = 0  # 다음 배열이 a에서 시작하는 위치.
    for length in s:
        b = a[offset:offset + length]  # [시작:끝]은 끝을 제외하는 슬라이스. 이번 배열을 분리.
        offset += length
        prefix = [0]  # 누적 합 리스트. prefix[i]는 처음 i개 원소의 합.
        positions = {0: 0}  # {}는 딕셔너리. 누적 합 값에 대응하는 경계 위치 저장.
        depth = [0] * length  # depth[i]는 i에서 끝나는 한 세포가 마지막 원소를 몇 번 두 배까지 키울 수 있는지 저장.
        dp = [1]  # dp[i]는 처음 i개 원소의 합성 기록 개수. 빈 배열의 기록은 한 가지.
        for right, value in enumerate(b):  # enumerate는 (인덱스, 값) 제공. 오른쪽 끝을 차례대로 확장.
            prefix.append(prefix[-1] + value)  # [-1]은 마지막 원소, append는 끝에 추가. 누적 합 갱신.
            positions[prefix[-1]] = right + 1  # 양수 배열이라 누적 합이 중복되지 않음. 합→경계 위치 등록.
            left, mass = right, value  # 현재 마지막 세포의 왼쪽 위치와 질량 초기화.
            ways = dp[right]  # 마지막 원소를 합치지 않은 경우는 앞부분의 모든 기록과 연결 가능.
            while left > 0:  # while은 조건이 참인 동안 반복. 왼쪽 세포가 있는 동안 합성 시도.
                previous = left - 1  # 합치려는 왼쪽 세포의 마지막 원소 인덱스.
                ratio, remainder = divmod(mass, b[previous])  # divmod는 몫·나머지 반환. 왼쪽 끝 세포가 같은 질량이 될 수 있는지 확인.
                if remainder or ratio == 0 or ratio & (ratio - 1):  # or는 하나라도 참. 양의 2의 거듭제곱 비율이 아니면 합성 불가능.
                    break  # break는 현재 while 반복 종료.
                required = ratio.bit_length() - 1  # bit_length는 이진수 자릿수. 2의 거듭제곱 비율에 필요한 합성 횟수 계산.
                if required > depth[previous]:  # 이미 계산한 왼쪽 세포가 그 횟수만큼 커질 수 없는 경우.
                    break  # 더 큰 질량도 만들 수 없으므로 확장 중단.
                left = positions[prefix[left] - mass]  # 같은 질량인 왼쪽 세포의 시작 경계를 누적 합으로 찾음.
                mass *= 2  # *=는 곱한 값 저장. 같은 질량의 두 세포를 합치면 질량 두 배.
                depth[right] += 1  # 이번 끝점에서 가능한 연속 합성 횟수 증가.
                ways += dp[left]  # 현재 마지막 세포 앞부분을 만드는 모든 기록을 더함.
            dp.append(ways % mod)  # 가능한 마지막 세포별 경우를 합산하고 나머지를 저장.
        answer.append(dp[-1])  # 이번 배열 전체를 처리한 기록 수를 결과에 추가.
    return answer  # 각 배열의 정답 목록 반환.
