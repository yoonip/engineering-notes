def solution(n):
    previous, current = 1, 1
    for _ in range(2, n + 1):
        previous, current = current, (previous + current) % 1234567
    return current

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 도달할 칸 수 입력.
#     previous, current = 1, 1  # 언패킹 대입. 0칸은 아무것도 안 하는 한 가지, 1칸은 한 번 뛰는 한 가지.
#     for _ in range(2, n + 1):  # range는 끝 제외. 2칸부터 n칸까지 동적 계획법(DP) 계산. _는 값이 필요 없는 반복 변수.
#         previous, current = current, (previous + current) % 1234567  # 오른쪽 먼저 계산해 동시 대입. 마지막 1칸·2칸 점프의 경우 수 합산. %는 나머지.
#     return current  # n칸에 도달하는 방법 수 반환.

# 풀이 요약
# 마지막에 1칸 뛰면 n-1칸까지의 모든 방법, 2칸 뛰면 n-2칸까지의 모든 방법이 있다. 두 경우는 겹치지 않아 더한다.
# 예: f(2)=2,f(3)=3,f(4)=5. 이전 두 값만 보관하므로 시간 O(N), 공간 O(1).
# 