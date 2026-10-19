# target은 정확히 얻어야 할 점수.
def solution(target):
    # 싱글·더블·트리플·불 점수 수집.
    scores = set(range(1, 21)) | {2 * value for value in range(1, 21)} | {3 * value for value in range(1, 21)} | {50}
    # 같은 점수면 싱글·불이 가능한 방법이 항상 유리.
    options = [(score, int(score <= 20 or score == 50)) for score in sorted(scores)]
    # throws[s]는 s점을 만드는 최소 다트 수.
    throws = [target + 1] * (target + 1)
    # singles[s]는 최소 다트 수를 쓴 경우의 최대 싱글·불 횟수.
    singles = [0] * (target + 1)
    # 0점은 다트를 던지지 않는 한 방법으로 시작.
    throws[0] = 0
    # 작은 점수부터 DP를 계산.
    for total in range(1, target + 1):
        # for~in으로 마지막에 던질 점수와 싱글·불 여부를 언패킹.
        for score, bonus in options:
            # 남은 점수보다 큰 다트는 사용할 수 없음.
            if score > total:
                break
            # 이전 점수의 최소 다트 수에 이번 한 발 추가.
            count = throws[total - score] + 1
            # 이전 최선의 싱글·불 수에 이번 가산값 추가.
            good = singles[total - score] + bonus
            # 다트 수가 더 적거나 동률에서 싱글·불이 더 많을 때 갱신.
            if count < throws[total] or count == throws[total] and good > singles[total]:
                # 최소 다트 수 저장.
                throws[total] = count
                # 같은 최적해의 최대 싱글·불 수 저장.
                singles[total] = good
    # [] 리스트로 다트 수·싱글과 불 횟수를 순서대로 return.
    return [throws[target], singles[target]]
