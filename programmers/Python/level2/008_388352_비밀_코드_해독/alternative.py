def solution(n, q, ans):
    attempts = [set(row) for row in q]
    answer = 0
    def visit(start, chosen):
        nonlocal answer
        need = 5-len(chosen)
        for attempt, target in zip(attempts, ans):
            matched = len(chosen & attempt)
            possible = sum(v >= start for v in attempt)
            if matched > target or matched + min(need, possible) < target:
                return
        if need == 0:
            answer += 1
            return
        for value in range(start, n-need+2):
            visit(value+1, chosen | {value})
    visit(1, set())
    return answer
