def solution(info,query):
    applicants=[record.split() for record in info]
    answer=[]
    for text in query:
        parts=text.replace(' and ',' ').split()
        total=0
        for row in applicants:
            if all(wanted=='-' or wanted==actual for wanted,actual in zip(parts[:4],row[:4])) and int(row[4])>=int(parts[4]): total+=1
        answer.append(total)
    return answer
