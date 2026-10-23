def solution(plans):
    tasks = []
    for name,start,duration in plans:
        h,m=map(int,start.split(':'))
        tasks.append((h*60+m,name,int(duration)))
    tasks.sort()
    now=tasks[0][0]
    index=0
    stack=[]
    answer=[]
    while index<len(tasks) or stack:
        while index<len(tasks) and tasks[index][0]==now:
            _,name,work=tasks[index]
            stack.append([name,work])
            index+=1
        if stack:
            stack[-1][1]-=1
            if stack[-1][1]==0:
                answer.append(stack.pop()[0])
        now+=1
    return answer
