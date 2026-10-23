# 각 구간이 원래 단어·규칙 1·규칙 2·두 규칙 결합인지 직접 검사하고 유효한 구간을 이어 붙입니다. 모든 소문자의 출현이
# 한 규칙에 온전히 들어가야 하며 재사용과 교차를 막습니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from functools import lru_cache

def solution(sentence):
    n=len(sentence)
    if not n or any(not ('a'<=ch<='z' or 'A'<=ch<='Z') for ch in sentence):return 'invalid'
    positions={ch:[i for i,c in enumerate(sentence) if c==ch] for ch in set(sentence) if ch.islower()}
    def rule1(left,right):
        word=sentence[left:right]
        if word and all(ch.isupper() for ch in word):return word
        if len(word)<3 or len(word)%2==0:return None
        marker=word[1]
        if not marker.islower():return None
        if positions[marker]!=list(range(left+1,right,2)):return None
        if any(not word[i].isupper() for i in range(0,len(word),2)):return None
        if any(word[i]!=marker for i in range(1,len(word),2)):return None
        return word[::2]
    def read(left,right):
        word=sentence[left:right]
        if word[0].isupper():return rule1(left,right)
        marker=word[0]
        if len(word)<3 or word[-1]!=marker or positions[marker]!=[left,right-1]:return None
        return rule1(left+1,right-1)
    @lru_cache(None)
    def parse(start):
        if start==n:return ()
        for end in range(start+1,n+1):
            word=read(start,end)
            if word:
                rest=parse(end)
                if rest is not None:return (word,)+rest
        return None
    result=parse(0)
    return ' '.join(result) if result is not None else 'invalid'
