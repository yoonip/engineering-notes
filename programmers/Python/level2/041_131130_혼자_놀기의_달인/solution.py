def solution(cards):
    visited = set()
    groups = [0, 0]
    for start in range(len(cards)):
        node, size = start, 0
        # 순열의 포인터를 따라가면 한 순환 그룹이 만들어진다.
        while node not in visited:
            visited.add(node)
            size += 1
            node = cards[node] - 1
        groups.append(size)
    groups.sort(reverse=True)
    # 서로 다른 두 순환 중 가장 큰 둘이 곱을 최대화한다.
    return groups[0] * groups[1]
