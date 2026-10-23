def solution(n):
    full = (1 << n) - 1
    def search(columns, left, right):
        if columns == full:
            return 1
        available = full & ~(columns | left | right)
        count = 0
        while available:
            position = available & -available
            available -= position
            count += search(columns | position, (left | position) << 1, (right | position) >> 1)
        return count
    return search(0, 0, 0)

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. n은 체스판 한 변과 배치할 퀸 수.
#     full = (1 << n) - 1  # <<는 왼쪽 비트 이동. 아래 n비트가 모두 1인 마스크로 유효 열 표시.
#     def search(columns, left, right):  # 중첩 재귀 함수. 사용한 열과 현재 행에서 대각선 공격을 받는 열들을 비트로 저장.
#         if columns == full:  # ==는 같음. 모든 열에 하나씩 배치되면 n개 퀸 배치 완료.
#             return 1  # 가능한 배치 한 가지 반환.
#         available = full & ~(columns | left | right)  # |는 비트 OR, ~는 반전, &는 AND. 현재 행에서 열·대각선 공격을 안 받는 열만 선택.
#         count = 0  # =는 대입. 현재 상태에서 가능한 완성 배치 수 초기화.
#         while available:  # while은 반복. 놓을 수 있는 열이 남아 있는 동안 검사.
#             position = available & -available  # 음수와 비트 AND를 취해 가장 오른쪽 1비트 하나 추출.
#             available -= position  # -=는 빼서 저장. 현재 선택 열을 후보에서 제거.
#             count += search(columns | position, (left | position) << 1, (right | position) >> 1)  # 선택 열을 OR로 추가. 다음 행의 대각선은 <<1·>>1로 한 열씩 옮겨 재귀 호출, +=로 경우의 수 누적.
#         return count  # 현재 상태에서 얻은 총 배치 수 반환.
#     return search(0, 0, 0)  # 아직 어떤 공격 열도 없는 첫 행에서 시작해 결과 반환.

# 풀이 요약
# 행마다 퀸을 하나 놓으며 사용한 열·두 대각선을 비트마스크로 관리합니다. 공격받지 않는 열을 모두 시도하는 백트래킹입니다.
# 예: n=4는 [1,3,0,2]·[2,0,3,1] 열 배치 두 가지. 탐색 시간 상한 O(n!), 재귀 공간 O(n).
