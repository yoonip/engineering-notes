from collections import deque  # from A import B는 모듈 A에서 B 가져오기. deque는 양끝 삽입·삭제가 빠른 덱 자료구조.

def solution(rc, operations):
    left = deque(row[0] for row in rc)  # 제너레이터 표현식으로 각 행의 첫 값을 읽어 왼쪽 열 덱 생성.
    right = deque(row[-1] for row in rc)  # [-1]은 마지막 원소. 오른쪽 열을 위에서 아래 순서로 저장.
    middle = deque(deque(row[1:-1]) for row in rc)  # [1:-1]은 양끝을 제외한 슬라이스. 행별 가운데 부분도 덱으로 저장.
    for operation in operations:
        if operation == 'ShiftRow':
            left.rotate(1)  # rotate(1)은 마지막 원소를 맨 앞으로 옮김. 왼쪽 열을 한 칸 아래로 순환.
            right.rotate(1)  # 오른쪽 열도 한 칸 아래로 순환.
            middle.rotate(1)  # 행별 가운데 덱의 순서도 한 칸 아래로 순환.
        else:  # else는 앞 조건이 거짓일 때. 남은 연산은 Rotate.
            middle[0].appendleft(left.popleft())  # popleft는 왼쪽 끝 제거·반환, appendleft는 왼쪽 끝 추가. 좌상단 값을 첫 행 가운데로 이동.
            right.appendleft(middle[0].pop())  # pop은 오른쪽 끝 제거·반환. 첫 행 오른쪽 값을 오른쪽 열 맨 위로 이동.
            middle[-1].append(right.pop())  # 오른쪽 열 맨 아래 값을 마지막 행 가운데 맨 뒤로 이동.
            left.append(middle[-1].popleft())  # 마지막 행 왼쪽 값을 왼쪽 열 맨 아래로 이동해 회전 완성.
    return [[a] + list(row) + [b] for a, row, b in zip(left, middle, right)]  # zip은 같은 위치 원소를 묶음. list로 가운데 덱을 변환하고 양쪽 열을 붙여 행렬 복원.
