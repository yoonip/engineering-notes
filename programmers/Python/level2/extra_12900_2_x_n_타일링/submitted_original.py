def solution(n):
    previous, current = 1, 1
    for _ in range(2, n + 1):
        previous, current = current, (previous + current) % 1000000007
    return current

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 세로 2인 바닥의 가로 길이 입력.
#     previous, current = 1, 1  # 언패킹 대입. 너비 0은 빈 배치 한 가지, 너비 1은 세로 타일 한 가지.
#     for _ in range(2, n + 1):  # range는 끝 제외. 너비 2부터 n까지 순서대로 DP 계산.
#         previous, current = current, (previous + current) % 1000000007  # 동시 대입으로 이전 두 값을 갱신. %는 나머지. 세로 타일 한 장·가로 타일 두 장으로 끝나는 경우의 합.
#     return current  # 목표 너비를 채우는 방법 수 반환.

# 풀이 요약
# 오른쪽 끝이 세로 한 장이면 왼쪽 너비 n-1, 가로 두 장이면 왼쪽 너비 n-2가 남는다. 따라서 f(n)=f(n-1)+f(n-2).
# 예: f(1)=1,f(2)=2,f(3)=3,f(4)=5. 시간 O(N), 공간 O(1). 멀리 뛰기와 점화식은 같지만 나머지 기준은 1000000007이다.
# 