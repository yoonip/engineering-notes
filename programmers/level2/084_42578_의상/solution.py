from collections import Counter

def solution(clothes):
    # 생성식 for로 이름·종류를 언패킹하고 종류만 Counter로 집계.
    counts = Counter(kind for name, kind in clothes)
    answer = 1
    for count in counts.values():
        # 해당 종류에서 하나 고르는 count가지+안 입는 1가지.
        answer *= count + 1
    return answer - 1
