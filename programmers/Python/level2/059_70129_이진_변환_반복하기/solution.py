def solution(s):
    conversions = removed = 0
    while s != '1':
        # 0을 지우고 남는 것은 1의 개수뿐이다.
        ones = s.count('1')
        # 이번 변환에서 제거한 0 수를 누적한다.
        removed += len(s) - ones
        s = bin(ones)[2:]
        conversions += 1
    return [conversions, removed]
