from math import factorial

def solution(n, k):
    # 아직 배치하지 않은 번호를 오름차순으로 보관.
    available = list(range(1, n + 1))
    answer = []
    k -= 1
    block = factorial(n)
    # 남은 사람 수를 n부터 1까지 줄임.
    for remaining in range(n, 0, -1):
        block //= remaining
        # 몫은 선택할 번호 위치, 나머지는 그 묶음 안 순번.
        index, k = divmod(k, block)
        answer.append(available.pop(index))
    return answer
