def solution(mats, park):
    rows = len(park)
    cols = len(park[0])
    for size in sorted(mats, reverse=True):
        for row in range(rows - size + 1):
            for col in range(cols - size + 1):
                possible = True
                for r in range(row, row + size):
                    for c in range(col, col + size):
                        if park[r][c] != "-1":
                            possible = False
                            break
                    if not possible:
                        break
                if possible:
                    return size
    return -1

# 전체 코드 줄별 설명
# def solution(mats, park):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 돗자리 크기들과 공원 배치를 입력받음.
#     rows = len(park)  # len은 길이. =는 값 저장. 공원의 행 수.
#     cols = len(park[0])  # len은 길이. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 공원의 열 수.
#     for size in sorted(mats, reverse=True):  # for·in은 원소를 차례로 꺼내는 반복문. sorted는 정렬한 새 리스트. =는 이름 붙인 인수에 값 지정. True·False는 참·거짓. 큰 돗자리부터 차례로 시도.
#         for row in range(rows - size + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 현재 크기의 돗자리가 시작할 수 있는 행을 순회.
#             for col in range(cols - size + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 가능한 시작 열을 순회.
#                 possible = True  # =는 값 저장. True·False는 참·거짓. 현재 위치에 펼칠 수 있다고 가정.
#                 for r in range(row, row + size):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 돗자리가 차지할 행들을 확인.
#                     for c in range(col, col + size):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 돗자리가 차지할 열들을 확인.
#                         if park[r][c] != "-1":  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. !=는 다름 비교. 빈칸 표시 -1이 아닌 칸을 발견했는지 검사.
#                             possible = False  # =는 값 저장. True·False는 참·거짓. 현재 위치에는 펼칠 수 없다고 표시.
#                             break  # break는 가장 가까운 반복문 종료. 해당 행의 칸 검사를 중단.
#                     if not possible:  # if는 조건이 참일 때 실행. not은 참·거짓 반전. 이미 실패한 위치인지 확인.
#                         break  # break는 가장 가까운 반복문 종료. 나머지 행 검사도 중단.
#                 if possible:  # if는 조건이 참일 때 실행. 정사각형 안의 칸이 전부 비었는지 확인.
#                     return size  # return은 결과를 돌려주고 함수 종료. 큰 크기부터 봤으므로 첫 성공 크기가 최댓값.
#     return -1  # return은 결과를 돌려주고 함수 종료. 어떤 돗자리도 못 펴면 -1 반환.

# 풀이 요약
# 큰 돗자리부터 모든 시작 위치를 검사한다. 해당 정사각형의 모든 칸이 빈칸 표시 문자열 -1이어야 펼칠 수 있다. 한 칸이라도 차 있으면 그 위치의 검사를 중단한다. 큰 크기부터 보므로 처음 성공한 크기가 답이다.
# 돗자리 K개, 지도 R×C, 최대 변 S: 시간 상한 O(K log K+KRCS²), 공간 O(K).
