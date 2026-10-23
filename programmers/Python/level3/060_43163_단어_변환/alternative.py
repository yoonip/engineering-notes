# 한 글자를 별표로 바꾼 형태끼리 버킷을 만듭니다. 같은 버킷의 단어는 한 글자 변환으로 이어집니다. 단어 쌍을 매번
# 비교하는 대신 버킷을 재사용합니다.
from collections import defaultdict,deque

def solution(begin,target,words):
    if target not in words:return 0
    buckets=defaultdict(list)
    for word in words:
        for i in range(len(word)):buckets[word[:i]+'*'+word[i+1:]].append(word)
    queue=deque([(begin,0)]);seen={begin}
    while queue:
        word,d=queue.popleft()
        if word==target:return d
        for i in range(len(word)):
            pattern=word[:i]+'*'+word[i+1:]
            for nxt in buckets.pop(pattern,[]):
                if nxt not in seen:seen.add(nxt);queue.append((nxt,d+1))
    return 0
