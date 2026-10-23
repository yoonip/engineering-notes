def solution(ineq, eq, n, m):
    if n == m:
        return int(eq == '=')
    return int(n > m if ineq == '>' else n < m)

# 전체 코드 줄별 설명
# def solution(ineq, eq, n, m):  # def는 함수 정의. 부등호·등호 포함 여부·두 정수 입력.
#     if n == m:  # if는 조건, ==는 값 같음 비교.
#         return int(eq == '=')  # 같은 수라면 등호가 포함된 비교만 참. int로 1 또는 0 반환.
#     return int(n > m if ineq == '>' else n < m)  # 조건 표현식으로 부등호 방향 선택. >·<는 대소 비교, int는 참·거짓을 정수로 변환.

# 풀이 요약
# 같은 수일 때 등호 여부를 먼저 처리하고, 나머지는 부등호 방향만 비교합니다.
# 