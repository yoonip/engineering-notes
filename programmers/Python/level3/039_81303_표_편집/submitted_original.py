from array import array

def solution(n, k, cmd):
    previous = array('i', range(-1, n - 1))
    following = array('i', range(1, n + 1))
    alive = ['O'] * n
    deleted = []
    for command in cmd:
        action = command[0]
        if action == 'U' or action == 'D':
            links = previous if action == 'U' else following
            for _ in range(int(command[2:])):
                k = links[k]
        elif action == 'C':
            left, right = previous[k], following[k]
            deleted.append((k, left, right))
            alive[k] = 'X'
            if left != -1:
                following[left] = right
            if right != n:
                previous[right] = left
            k = right if right != n else left
        else:
            row, left, right = deleted.pop()
            alive[row] = 'O'
            if left != -1:
                following[left] = row
            if right != n:
                previous[right] = row
    return ''.join(alive)

# 전체 코드 줄별 설명
# from array import array  # import는 도구 가져오기. array는 같은 종류 숫자를 메모리 효율적으로 저장하는 표준 라이브러리 배열.
# 
# def solution(n, k, cmd):  # def는 함수 정의. n은 행 수, k는 선택 행, cmd는 명령어 목록.
#     previous = array('i', range(-1, n - 1))  # 'i'는 부호 있는 정수 타입. range(시작,끝)는 끝 제외. 각 행의 바로 위 행을 저장.
#     following = array('i', range(1, n + 1))  # 각 행의 바로 아래 행. -1과 n은 양 끝에 행이 없다는 표시.
#     alive = ['O'] * n  # []는 리스트, * n은 n번 반복. 처음에는 모든 행이 남아 있음.
#     deleted = []  # 최근 삭제부터 복구할 스택. 리스트의 append/pop으로 구현.
#     for command in cmd:  # for는 모든 명령을 차례로 반복.
#         action = command[0]  # [0]은 문자열의 첫 글자 조회.
#         if action == 'U' or action == 'D':  # ==는 같음, or는 둘 중 하나만 참이어도 참. 이동 명령 구분.
#             links = previous if action == 'U' else following  # 조건부 표현식. 위로 가면 previous, 아래로 가면 following 선택.
#             for _ in range(int(command[2:])):  # [2:]는 세 번째 문자부터 자르기. int는 정수 변환. 정해진 칸 수 반복.
#                 k = links[k]  # []로 이웃 행 번호 조회. 삭제된 행은 연결에서 빠져 있어 자동으로 건너뜀.
#         elif action == 'C':  # elif는 앞 조건이 거짓일 때 검사하는 추가 조건.
#             left, right = previous[k], following[k]  # 튜플 언패킹으로 삭제 행의 위·아래를 저장.
#             deleted.append((k, left, right))  # ()는 튜플. 복구에 필요한 행과 양쪽 이웃을 스택 끝에 추가.
#             alive[k] = 'X'  # 삭제 여부 표시.
#             if left != -1:  # !=는 다름. 위 행이 있을 때만 연결 수정.
#                 following[left] = right  # 위 행이 삭제 행을 건너뛰어 아래 행을 가리키게 함.
#             if right != n:  # 아래 행이 있는지 검사.
#                 previous[right] = left  # 아래 행도 위 행과 직접 연결.
#             k = right if right != n else left  # 아래 행을 선택하되 마지막 행 삭제라면 위 행 선택.
#         else:  # 나머지 명령은 복구 Z.
#             row, left, right = deleted.pop()  # pop은 스택의 마지막 원소를 꺼내 삭제. 가장 최근 삭제를 복구.
#             alive[row] = 'O'  # 복구 행을 남아 있는 상태로 표시. 현재 선택 k는 유지.
#             if left != -1:  # 위 행이 있으면 연결 복원.
#                 following[left] = row  # 위 행의 다음 행을 복구한 행으로 바꿈.
#             if right != n:  # 아래 행이 있으면 연결 복원.
#                 previous[right] = row  # 아래 행의 이전 행을 복구한 행으로 바꿈.
#     return ''.join(alive)  # join은 문자열 리스트를 구분자 없이 이어 붙임.

# 풀이 요약
# 배열 두 개로 양방향 연결 리스트를 만든다. 삭제·복구는 양옆 연결만 바꾸고, 복구 정보는 후입선출 스택에 보관한다.
# 예: 3↔4↔5에서 4를 삭제하면 3↔5. 복구할 때 저장한 (4,3,5)로 3↔4↔5를 되살린다.
# 시간 O(N + 명령 수 + 총 이동 칸 수), 공간 O(N + 삭제 수). 총 이동은 최대 100만이라 한 칸씩 이동해도 된다.
# 