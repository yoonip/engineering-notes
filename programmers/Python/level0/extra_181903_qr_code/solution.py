def solution(q, r, code):
    return code[r::q]

# 전체 코드 줄별 설명
# def solution(q, r, code):  # def는 함수 정의. 나눌 수·나머지·문자열 입력.
#     return code[r::q]  # [시작::간격] 슬라이싱. r부터 q칸 간격인 인덱스는 q로 나눈 나머지가 모두 r.

# 풀이 요약
# 조건을 만족하는 인덱스 r, r+q, r+2q 위치를 슬라이싱으로 한 번에 가져옵니다.
# 