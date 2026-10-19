from collections import defaultdict

def solution(fees,records):
    logs=defaultdict(list)
    for record in records:
        time,car,_=record.split()
        h,m=map(int,time.split(':'))
        logs[car].append(h*60+m)
    answer=[]
    base,price,unit,extra=fees
    for car in sorted(logs):
        times=logs[car]
        if len(times)%2: times.append(1439)
        total=sum(times[i+1]-times[i] for i in range(0,len(times),2))
        answer.append(price+(max(0,total-base)+unit-1)//unit*extra)
    return answer
