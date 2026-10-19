def solution(dist_limit, split_limit):
    def binary_cost(count, depth):
        total = 0
        for _ in range(depth):
            # 이 깊이에 필요한 분배 노드 수를 더한다.
            total += count
            # 한 층 위에서 필요한 부모 수를 올림 나눗셈으로 구한다.
            count = (count + 1) // 2
        return total

    answer = 1
    width = 1
    depth = 0
    while width <= split_limit:
        answer = max(answer, min(width, dist_limit + 1))
        power = 1
        while width * power * 3 <= split_limit:
            power *= 3
        if depth == 0:
            answer = max(answer, 1 + 2 * min(dist_limit, (power - 1) // 2))
        elif power > 1:
            low, high = 1, width // 2
            while low < high:
                mid = (low + high) // 2
                needed = binary_cost(mid, depth) + mid * (power - 1)
                if needed >= dist_limit:
                    high = mid
                else:
                    low = mid + 1
            # 예산과 용량이 만나는 경계 양쪽을 확인한다.
            for count in (low - 1, low):
                if count == 0:
                    continue
                used = binary_cost(count, depth)
                if used <= dist_limit:
                    ternary = min(dist_limit - used, count * (power - 1))
                    answer = max(answer, 1 + used + 2 * ternary)
        width *= 2
        depth += 1
    return answer
