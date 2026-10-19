def solution(begin, end):
    answer = [0] * (end - begin + 1)
    for block in range(1, min(10000000, end // 2) + 1):
        first = max(2 * block, ((begin + block - 1) // block) * block)
        for position in range(first, end + 1, block):
            answer[position - begin] = block
    return answer
