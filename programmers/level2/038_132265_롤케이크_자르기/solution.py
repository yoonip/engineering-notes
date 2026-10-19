from collections import Counter

def solution(topping):
    right = Counter(topping)
    left = set()
    answer = 0
    for value in topping:
        left.add(value)
        right[value] -= 1
        # 오른쪽에서 사라진 종류의 키도 지워 종류 수를 맞춘다.
        if right[value] == 0:
            del right[value]
        # 개수가 아니라 서로 다른 토핑 종류 수를 비교한다.
        if len(left) == len(right):
            answer += 1
    return answer
