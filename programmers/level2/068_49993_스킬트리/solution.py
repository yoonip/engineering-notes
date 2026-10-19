def solution(skill, skill_trees):
    # 선행 조건이 있는 스킬들을 빠르게 찾도록 저장.
    required = set(skill)
    answer = 0
    for tree in skill_trees:
        # 생성식의 if·in으로 선행 대상만 남기고 join으로 문자열 연결.
        filtered = ''.join(character for character in tree if character in required)
        if skill.startswith(filtered):
            answer += 1
    return answer
