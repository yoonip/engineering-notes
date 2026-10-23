# e는 구간의 공통 오른쪽 끝, starts는 여러 왼쪽 끝 목록.
def solution(e, starts):
    # 각 정수의 약수 개수를 1로 시작.
    divisors = [1] * (e + 1)
    # 2부터 e까지 소수 후보 순회.
    for prime in range(2, e + 1):
        # 이미 작은 소수의 배수로 처리됐다면 합성수.
        if divisors[prime] != 1:
            # continue는 다음 후보로 이동.
            continue
        # 현재 소수 거듭제곱과 지수.
        power, exponent = prime, 1
        # prime, prime², prime³...을 순회.
        while power <= e:
            # 해당 거듭제곱의 모든 배수를 순회.
            for multiple in range(power, e + 1, power):
                # 소수 지수가 증가하면 약수 선택 수가 exponent에서 exponent+1로 증가.
                divisors[multiple] = divisors[multiple] // exponent * (exponent + 1)
            # 다음 거듭제곱으로 이동.
            power *= prime
            exponent += 1
    # 원래 순서대로 답을 보관할 리스트.
    answer = [0] * len(starts)
    # 오른쪽부터 스캔할 위치와 현재 최적 정수 초기화.
    cursor = winner = e
    # 현재 구간에서 가장 많은 약수 개수.
    best_count = divisors[e]
    # 큰 시작점부터 처리.
    for index, start in sorted(enumerate(starts), key=lambda item: item[1], reverse=True):
        # 이전에 처리하지 않은 왼쪽 부분만 추가로 스캔.
        while cursor >= start:
            # 개수가 같아도 더 작은 정수인 현재 cursor로 바꿔 동률 우선순위 처리.
            if divisors[cursor] >= best_count:
                # 최적 정수 갱신.
                winner = cursor
                # 최고 등장 횟수 갱신.
                best_count = divisors[cursor]
            # 다음으로 작은 정수 확인.
            cursor -= 1
        # [인덱스]에 저장해 정렬 전 질의 순서 복원.
        answer[index] = winner
    # 각 구간의 답 목록 반환.
    return answer
