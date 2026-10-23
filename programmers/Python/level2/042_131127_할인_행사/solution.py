from collections import Counter

def solution(want, number, discount):
    needed = dict(zip(want, number))
    answer = 0
    for start in range(len(discount) - 9):
        # 열흘 구간의 상품별 수량을 센다.
        current = Counter(discount[start:start + 10])
        # 원하는 종류와 수량이 모두 같아야 한다.
        if current == needed:
            answer += 1
    return answer
