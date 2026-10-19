# 문제: 스킬트리
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/49993
# 풀이: 선행 조건이 없는 스킬을 set 조회로 걸러낸다. 남은 순서가 필수 스킬의 접두부인지 확인한다.
# 복잡도: 전체 문자열 길이 합 L·선행 스킬 길이 S: 평균 시간 O(L+S), 추가 공간 O(S+가장 긴 스킬트리 길이).

def solution(skill, skill_trees):
    required = set(skill)
    answer = 0
    for tree in skill_trees:
        filtered = ''.join(character for character in tree if character in required)
        if skill.startswith(filtered):
            answer += 1
    return answer
