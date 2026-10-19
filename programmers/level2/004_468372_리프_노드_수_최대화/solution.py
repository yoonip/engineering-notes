# 문제: 리프 노드 수 최대화
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/468372
# 풀이: 이진 분기 깊이와 가능한 삼진 분기 수를 비교한다. 비용이 단조인 구간은 이분 탐색으로 좁힌다.
# 복잡도: 분기 한도 S·L=log₂S: 시간 상한 O(L³), 추가 공간 O(1). 큰 정수 연산 비용은 별도다.

def solution(dist_limit, split_limit):
    def binary_cost(count, depth):
        total = 0
        for _ in range(depth):
            total += count
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
