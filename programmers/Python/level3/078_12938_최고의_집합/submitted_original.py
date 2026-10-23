def solution(n, s):
    if s < n:
        return [-1]
    quotient, remainder = divmod(s, n)
    return [quotient] * (n - remainder) + [quotient + 1] * remainder

# 전체 코드 줄별 설명
# def solution(n, s):  # def는 함수 정의. 자연수 개수와 만들 합을 받음.
#     if s < n:  # 각 원소가 최소 1이어야 하므로 합이 개수보다 작으면 불가능.
#         return [-1]  # []는 리스트. 문제에서 지정한 불가능 표시 반환.
#     quotient, remainder = divmod(s, n)  # divmod는 몫·나머지 반환. 두 변수에 언패킹 대입해 고르게 나눌 기준값 계산.
#     return [quotient] * (n - remainder) + [quotient + 1] * remainder  # *는 리스트 반복, +는 리스트 연결. 작은 값부터 배치해 오름차순 결과 생성.

# 풀이 요약
# 두 수의 차이가 2 이상이면 큰 수에서 1을 빼 작은 수에 더할 때 합은 같고 곱은 증가한다. 따라서 최적 집합의 수들은 차이가 최대 1이다.
# 예: 9를 2개로 나누면 몫 4·나머지 1이라 [4,5]. 몫을 n-r개, 몫+1을 r개 쓰면 합이 정확히 s가 된다.
# 실제 큰 곱을 계산할 필요가 없다. 시간 O(N), 반환 배열을 포함한 공간 O(N).
# 