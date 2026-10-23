def solution(n):
    pegs = [0] * (n + 1)
    answer = []
    for step in range(1, 1 << n):
        disk = (step & -step).bit_length()
        direction = -1 if (n + disk) % 2 == 0 else 1
        start = pegs[disk]
        pegs[disk] = (start + direction) % 3
        answer.append([start + 1, pegs[disk] + 1])
    return answer
