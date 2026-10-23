def solution(friends, gifts):
    n = len(friends)
    index = {}

    for i, name in enumerate(friends):
        index[name] = i

    given = [[0] * n for _ in range(n)]
    score = [0] * n
    received = [0] * n

    for gift in gifts:
        giver, receiver = gift.split()
        a = index[giver]
        b = index[receiver]

        given[a][b] += 1
        score[a] += 1
        score[b] -= 1

    for i in range(n):
        for j in range(i + 1, n):
            if given[i][j] > given[j][i]:
                received[i] += 1
            elif given[i][j] < given[j][i]:
                received[j] += 1
            elif score[i] > score[j]:
                received[i] += 1
            elif score[i] < score[j]:
                received[j] += 1

    return max(received)