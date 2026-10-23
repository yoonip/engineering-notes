# 110을 꺼내 다른 모든 위치에 넣은 문자열을 BFS로 모읍니다. 가능한 문자열 중 사전순 최솟값이 답입니다. 스택의 교환
# 논리를 짧은 문자열에서 직접 확인합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from collections import deque

def solution(s):
    answers=[]
    for word in s:
        seen={word};queue=deque([word])
        while queue:
            value=queue.popleft()
            for i in range(len(value)-2):
                if value[i:i+3]!='110':continue
                rest=value[:i]+value[i+3:]
                for j in range(len(rest)+1):
                    nxt=rest[:j]+'110'+rest[j:]
                    if nxt not in seen:seen.add(nxt);queue.append(nxt)
        answers.append(min(seen))
    return answers
