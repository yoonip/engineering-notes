def solution(n, build_frame):
    structures = set()
    def valid(x, y, kind):
        if kind == 0:
            return y == 0 or (x, y - 1, 0) in structures or (x - 1, y, 1) in structures or (x, y, 1) in structures
        return (x, y - 1, 0) in structures or (x + 1, y - 1, 0) in structures or ((x - 1, y, 1) in structures and (x + 1, y, 1) in structures)
    for x, y, kind, action in build_frame:
        structure = (x, y, kind)
        if action == 1:
            if valid(x, y, kind):
                structures.add(structure)
        else:
            structures.remove(structure)
            if not all(valid(sx, sy, sk) for sx, sy, sk in structures):
                structures.add(structure)
    return [list(structure) for structure in sorted(structures)]

# 전체 코드 줄별 설명
# def solution(n, build_frame):  # def는 함수 정의. 벽 크기와 작업 목록을 받음. 범위를 벗어나는 작업은 입력되지 않음.
#     structures = set()  # set()은 빈 집합. (x,y,종류) 튜플로 설치된 구조물을 저장하고 포함 여부를 빠르게 검사.
#     def valid(x, y, kind):  # 현재 집합에서 구조물 하나의 지지 조건을 검사하는 내부 함수.
#         if kind == 0:  # ==는 같음. 종류 0은 기둥.
#             return y == 0 or (x, y - 1, 0) in structures or (x - 1, y, 1) in structures or (x, y, 1) in structures  # or는 하나라도 참. 바닥·아래 기둥·왼쪽 보의 끝·오른쪽 보의 시작 중 하나로 지지되어야 함.
#         return (x, y - 1, 0) in structures or (x + 1, y - 1, 0) in structures or ((x - 1, y, 1) in structures and (x + 1, y, 1) in structures)  # 종류 1은 보. 양 끝 중 하나 아래 기둥이 있거나 양옆 보가 모두 있어야 함. and는 모두 참.
#     for x, y, kind, action in build_frame:  # for로 각 명령의 네 값을 언패킹.
#         structure = (x, y, kind)  # ()는 튜플. 현재 구조물의 고유 정보.
#         if action == 1:  # 1은 설치 명령.
#             if valid(x, y, kind):  # 새 구조물의 지지 조건 검사. 설치는 기존 구조물의 지지를 약화시키지 않음.
#                 structures.add(structure)  # add는 집합 원소 추가.
#         else:  # 나머지 0은 삭제 명령.
#             structures.remove(structure)  # remove는 집합 원소 삭제. 먼저 지운 상태를 가정.
#             if not all(valid(sx, sy, sk) for sx, sy, sk in structures):  # all은 모든 조건 확인, not은 부정. 남은 구조물 중 하나라도 불안정하면 삭제 취소.
#                 structures.add(structure)  # 삭제한 구조물을 다시 넣어 원래 상태로 복구.
#     return [list(structure) for structure in sorted(structures)]  # sorted는 튜플을 x·y·종류 순으로 정렬. list로 각 튜플을 리스트로 변환.

# 풀이 요약
# 기둥·보의 지지 조건을 함수로 옮겨 시뮬레이션한다. 설치는 새 구조물만 검사하고, 삭제는 남은 구조물을 전부 확인해 실패하면 되돌린다.
# 예제 2에서 보를 지워 다른 보가 떠버리는 삭제는 취소된다. 집합에 없는 음수 좌표 구조물은 in 검사에서 자연스럽게 거짓이 된다.
# 명령 수 Q≤1000. 시간 O(Q² + Q log Q), 공간 O(Q).
# 