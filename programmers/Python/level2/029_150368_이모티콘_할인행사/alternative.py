def solution(users,emoticons):
    spending=[0]*len(users)
    best=(0,0)
    def visit(index):
        nonlocal best
        if index==len(emoticons):
            joined=sum(paid>=user[1] for paid,user in zip(spending,users))
            revenue=sum(paid for paid,user in zip(spending,users) if paid<user[1])
            best=max(best,(joined,revenue))
            return
        for rate in (10,20,30,40):
            price=emoticons[index]*(100-rate)//100
            buyers=[i for i,user in enumerate(users) if rate>=user[0]]
            for i in buyers: spending[i]+=price
            visit(index+1)
            for i in buyers: spending[i]-=price
    visit(0)
    return list(best)
