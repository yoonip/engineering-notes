# 문제: 유사 칸토어 비트열
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/148652
# 풀이: 완전한 부분 블록의 1 개수는 거듭제곱으로 센다. 남은 블록만 재귀로 계산해 전체 비트열을 만들지 않는다.
# 복잡도: 단계 N: 재귀 호출 O(N), 재귀 공간 O(N). 거듭제곱 등 큰 정수 연산 비용은 별도다.

def solution(n, l, r):
    def prefix(level, length):
        if level == 0:
            return length
        block = 5 ** (level - 1)
        groups, rest = divmod(length, block)
        full = groups - int(groups > 2)
        total = full * 4 ** (level - 1)
        if groups == 2:
            return total
        return total + prefix(level - 1, rest)
    return prefix(n, r) - prefix(n, l - 1)
