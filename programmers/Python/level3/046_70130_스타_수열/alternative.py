# 스타 수열에 공통으로 들어갈 값을 하나 고르고 왼쪽부터 겹치지 않는 쌍을 만듭니다. 기본 풀이처럼 모든 값을 동시에
# 갱신하지 않아 최악 O(N²)입니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(a):
    answer=0
    for common in set(a):
        index=pairs=0
        while index+1<len(a):
            if a[index]!=a[index+1] and common in (a[index],a[index+1]):
                pairs+=1;index+=2
            else:index+=1
        answer=max(answer,2*pairs)
    return answer
