# array는 같은 종류 숫자를 메모리 효율적으로 저장하는 표준 라이브러리 배열.
from array import array

# n은 행 수, k는 선택 행, cmd는 명령어 목록.
def solution(n, k, cmd):
    # 각 행의 바로 위 행을 저장.
    previous = array('i', range(-1, n - 1))
    # -1과 n은 양 끝에 행이 없다는 표시.
    following = array('i', range(1, n + 1))
    # 처음에는 모든 행이 남아 있음.
    alive = ['O'] * n
    # 리스트의 append/pop으로 구현.
    deleted = []
    # for는 모든 명령을 차례로 반복.
    for command in cmd:
        # [0]은 문자열의 첫 글자 조회.
        action = command[0]
        # 이동 명령 구분.
        if action == 'U' or action == 'D':
            # 위로 가면 previous, 아래로 가면 following 선택.
            links = previous if action == 'U' else following
            # 정해진 칸 수 반복.
            for _ in range(int(command[2:])):
                # 삭제된 행은 연결에서 빠져 있어 자동으로 건너뜀.
                k = links[k]
        # elif는 앞 조건이 거짓일 때 검사하는 추가 조건.
        elif action == 'C':
            # 튜플 언패킹으로 삭제 행의 위·아래를 저장.
            left, right = previous[k], following[k]
            # 복구에 필요한 행과 양쪽 이웃을 스택 끝에 추가.
            deleted.append((k, left, right))
            # 삭제 여부 표시.
            alive[k] = 'X'
            # 위 행이 있으면 연결 복원.
            if left != -1:
                # 위 행이 삭제 행을 건너뛰어 아래 행을 가리키게 함.
                following[left] = right
            # 아래 행이 있으면 연결 복원.
            if right != n:
                # 아래 행도 위 행과 직접 연결.
                previous[right] = left
            # 아래 행을 선택하되 마지막 행 삭제라면 위 행 선택.
            k = right if right != n else left
        else:
            # 가장 최근 삭제를 복구.
            row, left, right = deleted.pop()
            # 현재 선택 k는 유지.
            alive[row] = 'O'
            # 위 행이 있으면 연결 복원.
            if left != -1:
                # 위 행의 다음 행을 복구한 행으로 바꿈.
                following[left] = row
            # 아래 행이 있으면 연결 복원.
            if right != n:
                # 아래 행의 이전 행을 복구한 행으로 바꿈.
                previous[right] = row
    # join은 문자열 리스트를 구분자 없이 이어 붙임.
    return ''.join(alive)
