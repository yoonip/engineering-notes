def solution(h1, m1, s1, h2, m2, s2):
    start = h1 * 3600 + m1 * 60 + s1
    end = h2 * 3600 + m2 * 60 + s2
    def count(t):
        # 상대 각도의 정수 회전 수를 세고 삼중 겹침을 한 번 뺀다.
        return t * 719 // 43200 + t * 59 // 3600 - t // 43200 + 1
    # 누적 횟수 차이에서 빠진 시작 순간을 다시 포함한다.
    at_start = start * 719 % 43200 == 0 or start * 59 % 3600 == 0
    return count(end) - count(start) + int(at_start)
