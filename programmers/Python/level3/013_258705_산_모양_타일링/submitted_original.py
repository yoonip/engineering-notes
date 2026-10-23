def solution(n, tops):
    modulus = 10007
    joined, free = 0, 1
    for top in tops:
        next_joined = (joined + free) % modulus
        next_free = ((1 + top) * joined + (2 + top) * free) % modulus
        joined, free = next_joined, next_free
    return (joined + free) % modulus

# 전체 코드 줄별 설명
# def solution(n, tops):  # def는 함수 정의. n은 사다리꼴 윗변 길이, tops는 위쪽 삼각형의 존재 여부 목록.
#     modulus = 10007  # =는 대입. 문제에서 요구한 나머지 기준 저장.
#     joined, free = 0, 1  # 두 값 언패킹. 오른쪽 끝 삼각형이 왼쪽과 마름모를 이룬 경우·단독인 경우. 시작 삼각형 하나는 단독 한 가지.
#     for top in tops:  # for~in으로 위쪽 삼각형의 유무 0 또는 1을 왼쪽부터 순회.
#         next_joined = (joined + free) % modulus  # %는 나머지. 새 오른쪽 삼각형을 왼쪽과 묶으면 이전 두 상태 모두 한 방법씩 확장.
#         next_free = ((1 + top) * joined + (2 + top) * free) % modulus  # *는 곱셈. 이전 끝이 묶였으면 1+top개, 단독이면 왼쪽과 묶는 방법까지 2+top개로 확장.
#         joined, free = next_joined, next_free  # 동시에 대입해 다음 구간의 두 DP 상태로 갱신.
#     return (joined + free) % modulus  # return은 결과 반환. 서로 겹치지 않는 끝 상태들의 경우의 수를 합산.

# 풀이 요약
# 오른쪽 끝의 삼각형이 이전 삼각형과 묶였는지로 상태를 두 개만 유지하는 DP입니다.
# 새 오른쪽을 마름모로 묶는 방법은 이전 전체 경우의 수입니다. 새 오른쪽이 단독이면 왼쪽 끝의 사용 여부와 top에 따라 1+top 또는 2+top가지로 확장합니다. 시간 O(N), 추가 공간 O(1).
# 예: tops=[0,1]이면 (joined,free)는 (0,1)→(1,2)→(3,8). 총 11가지입니다.
