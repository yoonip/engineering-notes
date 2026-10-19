# 문제: 후보키
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42890
# 풀이: 열 수가 작은 조합부터 검사한다. 기존 후보키를 포함하는 조합은 건너뛰고 행 튜플 set으로 유일성을 확인한다.
# 복잡도: 열 C개·행 R개·최종 후보키 K개: 시간 상한 O(2^C C(R+K)), 추가 공간 O(C(R+K)).

from itertools import combinations

def solution(relation):
    rows, columns = len(relation), len(relation[0])
    keys = []
    for size in range(1, columns + 1):
        for selected in combinations(range(columns), size):
            selected_set = set(selected)
            if any(key <= selected_set for key in keys):
                continue
            values = {tuple(row[column] for column in selected) for row in relation}
            if len(values) == rows:
                keys.append(selected_set)
    return len(keys)
