def solution(s):
    answer=0
    for offset in range(len(s)):
        current=s[offset:]+s[:offset]
        while current:
            following=current.replace('()','').replace('[]','').replace('{}','')
            if following==current: break
            current=following
        answer+=not current
    return answer
