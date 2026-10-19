def solution(skill, skill_trees):
    order = {ch: i for i, ch in enumerate(skill)}
    answer = 0
    for tree in skill_trees:
        needed = 0
        for ch in tree:
            if ch in order:
                if order[ch] != needed:
                    break
                needed += 1
        else:
            answer += 1
    return answer
