from collections import Counter

def solution(k,tangerine):
    bucket=[0]*(len(tangerine)+1)
    for count in Counter(tangerine).values(): bucket[count]+=1
    used=0
    for frequency in range(len(tangerine),0,-1):
        take=min(bucket[frequency],(k+frequency-1)//frequency)
        used+=take
        k-=take*frequency
        if k<=0: return used
