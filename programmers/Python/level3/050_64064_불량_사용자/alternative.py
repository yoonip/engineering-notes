# 패턴 개수만큼 사용자를 순서 있게 뽑아 하나씩 매칭합니다. 최종 사용자 집합으로 중복을 제거합니다. 비트마스크 DP보다
# 중복 탐색이 많지만 직접적입니다.
from itertools import permutations

def solution(user_id,banned_id):
    result=set()
    for assignment in permutations(user_id,len(banned_id)):
        if all(len(user)==len(pattern) and all(p=='*' or p==u for p,u in zip(pattern,user))
               for user,pattern in zip(assignment,banned_id)):
            result.add(frozenset(assignment))
    return len(result)
