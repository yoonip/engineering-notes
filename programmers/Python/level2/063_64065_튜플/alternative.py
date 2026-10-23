def solution(s):
    groups=[set(map(int,chunk.split(','))) for chunk in s[2:-2].split('},{')]
    groups.sort(key=len)
    seen=set()
    answer=[]
    for group in groups:
        fresh=group-seen
        answer.append(fresh.pop())
        seen=group
    return answer
