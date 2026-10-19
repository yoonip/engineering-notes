from itertools import combinations

def solution(relation):
    # 행 수·열 수 각각 대입.
    rows, columns = len(relation), len(relation[0])
    keys = []
    for size in range(1, columns + 1):
        # 열 번호에서 size개를 선택한 튜플 순회.
        for selected in combinations(range(columns), size):
            selected_set = set(selected)
            # 기존 후보키를 포함하면 최소성 위반.
            if any(key <= selected_set for key in keys):
                continue
            values = {tuple(row[column] for column in selected) for row in relation}
            # 모든 행의 묶음이 서로 다르면 유일성 만족.
            if len(values) == rows:
                keys.append(selected_set)
    return len(keys)
