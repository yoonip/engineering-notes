


def solution(d, budget):
    d.sort()
    total = 0
    answer = 0
    
    for cost in d:
        if total + cost>budget:
            break
        total +=cost
        answer += 1
        
    return answer