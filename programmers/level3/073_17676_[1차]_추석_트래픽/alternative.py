# 요청 [s,e]가 겹칠 1초 창의 시작점은 [s−999,e]입니다. 이 시작점 구간들의 최대 겹침을 차분 이벤트로
# 계산합니다. 끝점 전수 비교보다 빠릅니다.
from collections import defaultdict
from decimal import Decimal

def solution(lines):
    events=defaultdict(int)
    for line in lines:
        date,clock,duration=line.split();h,m,s=clock.split(':')
        end=(int(h)*3600+int(m)*60)*1000+int(Decimal(s)*1000)
        start=end-int(Decimal(duration[:-1])*1000)+1
        events[start-999]+=1;events[end+1]-=1
    current=answer=0
    for instant in sorted(events):
        current+=events[instant];answer=max(answer,current)
    return answer
