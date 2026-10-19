def solution(m, n, board):
    grid = [list(row) for row in board]
    positions = {}
    for r in range(m):
        for c in range(n):
            ch = grid[r][c]
            if 'A' <= ch <= 'Z':
                positions.setdefault(ch, []).append((r, c))
    def clear(r1, c1, r2, c2, ch):
        return all(grid[r][c] in ('.', ch) for r in range(min(r1, r2), max(r1, r2) + 1) for c in range(min(c1, c2), max(c1, c2) + 1))
    answer = ''
    while positions:
        for ch in sorted(positions):
            (r1, c1), (r2, c2) = positions[ch]
            path_a = clear(r1, c1, r1, c2, ch) and clear(r1, c2, r2, c2, ch)
            path_b = clear(r1, c1, r2, c1, ch) and clear(r2, c1, r2, c2, ch)
            if path_a or path_b:
                grid[r1][c1] = grid[r2][c2] = '.'
                answer += ch
                del positions[ch]
                break
        else:
            return 'IMPOSSIBLE'
    return answer

# 전체 코드 줄별 설명
# def solution(m, n, board):  # def는 함수 정의. 행 수·열 수·보드 문자열 목록 입력.
#     grid = [list(row) for row in board]  # list는 문자열을 글자 리스트로 바꿈. 타일을 지울 수 있게 복사.
#     positions = {}  # {}는 딕셔너리. 글자별 두 좌표 저장.
#     for r in range(m):  # range는 정수 범위. 모든 행 순회.
#         for c in range(n):  # 모든 열 순회.
#             ch = grid[r][c]  # []로 글자 조회.
#             if 'A' <= ch <= 'Z':  # 대문자 타일인지 범위 비교.
#                 positions.setdefault(ch, []).append((r, c))  # setdefault는 기본 목록 생성, append는 추가, ()는 좌표 튜플.
#     def clear(r1, c1, r2, c2, ch):  # 축에 나란한 선분이 비어 있는지 검사하는 함수.
#         return all(grid[r][c] in ('.', ch) for r in range(min(r1, r2), max(r1, r2) + 1) for c in range(min(c1, c2), max(c1, c2) + 1))  # all은 전부 참, in은 포함. 선분 위는 빈칸이나 제거할 두 타일만 허용.
#     answer = ''  # 빈 문자열. 제거 순서 누적.
#     while positions:  # 남은 타일 종류가 있는 동안 반복.
#         for ch in sorted(positions):  # sorted는 키를 알파벳순으로 정렬. 가능한 가장 작은 글자부터 검사.
#             (r1, c1), (r2, c2) = positions[ch]  # 중첩 언패킹으로 두 타일 좌표 분리.
#             path_a = clear(r1, c1, r1, c2, ch) and clear(r1, c2, r2, c2, ch)  # and는 모두 참. 가로 이동 뒤 세로 이동하는 L자 검사.
#             path_b = clear(r1, c1, r2, c1, ch) and clear(r2, c1, r2, c2, ch)  # 세로 이동 뒤 가로 이동하는 L자 검사.
#             if path_a or path_b:  # or는 둘 중 하나라도 참. 경로 하나라도 가능하면 제거.
#                 grid[r1][c1] = grid[r2][c2] = '.'  # 연쇄 대입. 두 타일 칸을 빈칸으로 변경.
#                 answer += ch  # +=는 더해 저장. 제거 순서 뒤에 글자 추가.
#                 del positions[ch]  # del은 딕셔너리 키 삭제. 해당 쌍 제거 완료.
#                 break  # 다음 제거도 A부터 검사하도록 for 종료.
#         else:  # for가 break 없이 끝났을 때 실행되는 else. 제거 가능한 쌍이 없음.
#             return 'IMPOSSIBLE'  # 더 진행할 수 없으므로 실패 반환.
#     return answer  # 모든 쌍을 제거한 사전순 최소 순서 반환.

# 풀이 요약
# 한 번만 꺾는 경로는 두 L자 모양 중 하나다. 두 선분을 확인하고 제거 가능한 타일 중 알파벳이 가장 빠른 것을 매번 제거한다.
# 타일 제거는 다른 경로를 막지 않고 더 열어주므로 현재 제거 가능한 작은 글자를 먼저 골라도 완성 가능성을 잃지 않는다.
# 예: DBA/C*A/CDB는 처음 A·C가 가능하지만 A를 먼저 골라 ABCD가 된다. 타일 종류 T≤26, 시간 O(MN+T²(M+N)), 공간 O(MN).
# 