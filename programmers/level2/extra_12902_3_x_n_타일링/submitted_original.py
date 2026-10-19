def solution(n):
    if n % 2:
        return 0
    previous, current = 1, 3
    for _ in range(4, n + 1, 2):
        previous, current = current, (4 * current - previous) % 1000000007
    return current

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 세로 3인 바닥의 가로 길이 입력.
#     if n % 2:  # %는 나머지. 홀수 너비면 전체 칸 수 3n이 홀수라 두 칸 타일로 채울 수 없음.
#         return 0  # 불가능한 경우의 수는 0.
#     previous, current = 1, 3  # 언패킹 대입. 너비 0은 빈 배치 한 가지, 너비 2는 세 가지.
#     for _ in range(4, n + 1, 2):  # range의 간격 2로 짝수 너비만 계산. _는 사용하지 않는 반복 변수.
#         previous, current = current, (4 * current - previous) % 1000000007  # 오른쪽 값을 먼저 계산해 동시 갱신. 점화식 f(n)=4f(n-2)-f(n-4), %는 나머지.
#     return current  # 목표 너비의 방법 수 반환.

# 풀이 요약
# 기본 너비 2 조각은 세 모양이고, 더 길게 이어지는 특수 모양은 각 짝수 너비마다 두 가지다. 따라서 f(n)=3f(n-2)+2(f(n-4)+...+f(0)).
# 이전 점화식을 빼면 f(n)=4f(n-2)-f(n-4)로 줄어든다. f(0)=1,f(2)=3이므로 f(4)=12-1=11.
# 두 이전 값만 유지하는 DP다. 시간 O(N), 공간 O(1). Python의 양수 기준 나머지는 뺄셈 후에도 0 이상으로 정규화된다.
# 