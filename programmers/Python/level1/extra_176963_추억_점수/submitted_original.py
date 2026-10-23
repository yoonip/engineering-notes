
def solution(name, yearning, photo):
    scores = dict(zip(name, yearning))
    
    answer = []
    
    for people in photo:
        total = 0
        
        for person in people:
            total += scores.get(person, 0)
            
        answer.append(total)
        
    return answer
