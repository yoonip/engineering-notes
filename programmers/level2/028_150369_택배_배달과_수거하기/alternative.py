def solution(cap,n,deliveries,pickups):
    delivery,pickup=list(deliveries),list(pickups)
    di=pi=n-1
    answer=0
    while True:
        while di>=0 and delivery[di]==0: di-=1
        while pi>=0 and pickup[pi]==0: pi-=1
        if di<0 and pi<0: return answer
        answer+=2*(max(di,pi)+1)
        for values,index in ((delivery,di),(pickup,pi)):
            room=cap
            while index>=0 and room:
                used=min(values[index],room)
                values[index]-=used
                room-=used
                if values[index]==0: index-=1
