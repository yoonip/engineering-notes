# 장르별 전체 합과 곡 목록을 만든 후 nsmallest로 두 곡만 고릅니다. 장르 안 모든 곡을 정렬하는 대신 필요한 상위
# 항목만 추출합니다.
from collections import defaultdict
from heapq import nsmallest

def solution(genres,plays):
    totals=defaultdict(int);songs=defaultdict(list)
    for i,(genre,count) in enumerate(zip(genres,plays)):
        totals[genre]+=count;songs[genre].append((-count,i))
    answer=[]
    for genre in sorted(totals,key=totals.get,reverse=True):
        answer.extend(i for count,i in nsmallest(2,songs[genre]))
    return answer
