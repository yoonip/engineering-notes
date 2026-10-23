# 범위를 벗어나는 작업은 입력되지 않음.
def solution(n, build_frame):
    # (x,y,종류) 튜플로 설치된 구조물을 저장하고 포함 여부를 빠르게 검사.
    structures = set()
    # 현재 집합에서 구조물 하나의 지지 조건을 검사하는 내부 함수.
    def valid(x, y, kind):
        # 종류 0은 기둥.
        if kind == 0:
            # 바닥·아래 기둥·왼쪽 보의 끝·오른쪽 보의 시작 중 하나로 지지되어야 함.
            return y == 0 or (x, y - 1, 0) in structures or (x - 1, y, 1) in structures or (x, y, 1) in structures
        # and는 모두 참.
        return (x, y - 1, 0) in structures or (x + 1, y - 1, 0) in structures or ((x - 1, y, 1) in structures and (x + 1, y, 1) in structures)
    # for로 각 명령의 네 값을 언패킹.
    for x, y, kind, action in build_frame:
        # 현재 구조물의 고유 정보.
        structure = (x, y, kind)
        # 1은 설치 명령.
        if action == 1:
            # 설치는 기존 구조물의 지지를 약화시키지 않음.
            if valid(x, y, kind):
                # 삭제한 구조물을 다시 넣어 원래 상태로 복구.
                structures.add(structure)
        else:
            # 먼저 지운 상태를 가정.
            structures.remove(structure)
            # 남은 구조물 중 하나라도 불안정하면 삭제 취소.
            if not all(valid(sx, sy, sk) for sx, sy, sk in structures):
                # 삭제한 구조물을 다시 넣어 원래 상태로 복구.
                structures.add(structure)
    # list로 각 튜플을 리스트로 변환.
    return [list(structure) for structure in sorted(structures)]
