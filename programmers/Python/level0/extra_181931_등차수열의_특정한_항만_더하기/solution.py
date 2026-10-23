def solution(a, d, included):
    return sum(a + i * d for i, keep in enumerate(included) if keep)

# 전체 코드 줄별 설명
# def solution(a, d, included):  # def는 함수 정의. 첫 항·공차·포함 여부 리스트 입력.
#     return sum(a + i * d for i, keep in enumerate(included) if keep)  # enumerate는 인덱스와 값 제공. if로 참인 항만 골라 a+i*d를 sum으로 합산.

# 풀이 요약
# 0부터 시작하는 인덱스 i의 항은 a+i*d입니다. 포함 여부가 참인 항만 더합니다.
# 