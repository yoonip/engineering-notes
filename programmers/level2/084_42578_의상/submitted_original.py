from collections import Counter

def solution(clothes):
    counts = Counter(kind for name, kind in clothes)
    answer = 1
    for count in counts.values():
        answer *= count + 1
    return answer - 1

# 전체 코드 줄별 설명
# from collections import Counter  # collections의 Counter를 import. 의상 종류별 개수를 세는 자료구조.
# 
# def solution(clothes):  # def는 함수 정의, clothes는 이름·종류 목록 입력.
#     counts = Counter(kind for name, kind in clothes)  # 생성식 for로 이름·종류를 언패킹하고 종류만 Counter로 집계.
#     answer = 1  # =는 대입. 선택 경우의 수를 곱할 초기값 1.
#     for count in counts.values():  # values()는 종류별 의상 수 제공. for로 순회.
#         answer *= count + 1  # *=는 곱해 저장. 해당 종류에서 하나 고르는 count가지+안 입는 1가지.
#     return answer - 1  # 모든 종류에서 안 입는 한 경우를 빼 return으로 반환.

# 풀이 요약
# 종류별로 한 벌 선택 또는 미착용이 가능하므로 (개수+1)을 모두 곱하고 아무것도 안 입는 경우 하나를 뺍니다.
# 예: 모자 2개·안경 1개는 (2+1)(1+1)-1=5. 의상 N개·종류 U개일 때 시간 O(N), 공간 O(U).
