def solution(k, ranges):
    prefix = [0.0]
    while k > 1:
        next_value = k // 2 if k % 2 == 0 else 3 * k + 1
        # 폭이 1인 사다리꼴의 넓이를 누적한다.
        prefix.append(prefix[-1] + (k + next_value) / 2)
        k = next_value
    n = len(prefix) - 1
    answer = []
    for start, offset in ranges:
        # 음수 끝점은 전체 단계 수를 기준으로 해석한다.
        end = n + offset
        answer.append(prefix[end] - prefix[start] if start <= end else -1.0)
    return answer
