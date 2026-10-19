def solution(players, callings):
    position = {}
    for i, name in enumerate(players):
        position[name] = i

    for name in callings:
        i = position[name]
        front = players[i - 1]

        players[i - 1], players[i] = players[i], players[i - 1]
        position[name] = i - 1
        position[front] = i

    return players