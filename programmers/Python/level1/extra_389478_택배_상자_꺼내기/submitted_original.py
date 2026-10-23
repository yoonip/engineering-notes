
def solution(n, w, num):
    row = (num - 1) // w
    col = (num - 1) % w

    if row % 2 == 1:
        col = w - 1 - col

    answer = 0

    for r in range(row, (n + w - 1) // w):
        if r % 2 == 0:
            box = r * w + col + 1
        else:
            box = (r + 1) * w - col

        if box <= n:
            answer += 1

    return answer
