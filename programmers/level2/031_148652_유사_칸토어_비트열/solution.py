def solution(n, l, r):
    def prefix(level, length):
        if level == 0:
            return length
        block = 5 ** (level - 1)
        groups, rest = divmod(length, block)
        # 가운데 세 번째 묶음은 모두 0이라 완전 묶음 수에서 뺀다.
        full = groups - int(groups > 2)
        total = full * 4 ** (level - 1)
        # 남은 위치가 가운데 묶음이면 1이 추가되지 않는다.
        if groups == 2:
            return total
        return total + prefix(level - 1, rest)
    return prefix(n, r) - prefix(n, l - 1)
