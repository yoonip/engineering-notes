# 삽입 위치를 이분탐색하고 최솟값·최댓값을 배열 양끝에서 삭제합니다. 오래된 힙 항목 처리가 없어서 단순하지만 삽입·앞
# 삭제가 선형 시간입니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from bisect import insort

def solution(operations):
    values=[]
    for operation in operations:
        command,text=operation.split();value=int(text)
        if command=='I':insort(values,value)
        elif values:values.pop(-1 if value==1 else 0)
    return [values[-1],values[0]] if values else [0,0]
