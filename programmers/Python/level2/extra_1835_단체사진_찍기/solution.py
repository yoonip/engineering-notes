from itertools import permutations

def solution(n, data):
    # 두 친구·연산자·간격으로 조건 분리.
    conditions = [(text[0], text[2], text[3], int(text[4])) for text in data]
    answer = 0
    for order in permutations('ACFJMNRT'):
        # 친구별 위치를 빠르게 조회할 표 생성.
        positions = {friend: i for i, friend in enumerate(order)}
        for first, second, operator, wanted in conditions:
            # 둘 사이의 다른 사람 수 계산.
            gap = abs(positions[first] - positions[second]) - 1
            if operator == '=' and gap != wanted:
                break
            # 미만 조건을 만족하지 못하면 제외.
            if operator == '<' and gap >= wanted:
                break
            if operator == '>' and gap <= wanted:
                break
        else:
            answer += 1
    return answer
