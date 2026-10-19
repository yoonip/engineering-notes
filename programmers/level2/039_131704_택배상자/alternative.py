def solution(order):
    incoming=1
    waiting=[]
    loaded=0
    for target in order:
        while incoming<=target:
            waiting.append(incoming)
            incoming+=1
        if not waiting or waiting[-1]!=target: break
        waiting.pop()
        loaded+=1
    return loaded
