def solution(wallpaper):
    lux = len(wallpaper)
    luy = len(wallpaper[0])
    rdx = 0
    rdy = 0
    for r, row in enumerate(wallpaper):
        for c, cell in enumerate(row):
            if cell == "#":
                lux = min(lux, r)
                luy = min(luy, c)
                rdx = max(rdx, r + 1)
                rdy = max(rdy, c + 1)
    return [lux, luy, rdx, rdy]

# 전체 코드 줄별 설명
# def solution(wallpaper):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. wallpaper: 각 행을 문자열로 저장한 리스트
#     lux = len(wallpaper)  # len은 길이. =는 값 저장. 시작 행: 전체 행 수로 초기화한 뒤 더 작은 파일 행을 찾음
#     luy = len(wallpaper[0])  # len은 길이. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 시작 열: 첫 행의 길이, 즉 전체 열 수로 초기화
#     rdx = 0  # =는 값 저장. 끝 행: 파일을 찾을 때마다 필요한 아래쪽 경계로 갱신
#     rdy = 0  # =는 값 저장. 끝 열: 파일을 찾을 때마다 필요한 오른쪽 경계로 갱신
#     for r, row in enumerate(wallpaper):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 행 번호 r과 해당 행의 문자열을 함께 꺼냄
#         for c, cell in enumerate(row):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 그 행에서 열 번호 c와 문자 하나를 함께 꺼냄
#             if cell == "#":  # if는 조건이 참일 때 실행. ==는 같음 비교. 파일이 있는 칸만 처리. 빈칸 "."은 건너뜀
#                 lux = min(lux, r)  # min은 최솟값. =는 값 저장. 기존 시작 행과 현재 행 중 작은 값 → 가장 위쪽
#                 luy = min(luy, c)  # min은 최솟값. =는 값 저장. 기존 시작 열과 현재 열 중 작은 값 → 가장 왼쪽
#                 rdx = max(rdx, r + 1)  # max는 최댓값. =는 값 저장. 현재 파일 칸의 아래쪽 경계까지 포함
#                 rdy = max(rdy, c + 1)  # max는 최댓값. =는 값 저장. 현재 파일 칸의 오른쪽 경계까지 포함
#     return [lux, luy, rdx, rdy]  # return은 결과를 돌려주고 함수 종료. []는 리스트. [시작 행, 시작 열, 끝 행, 끝 열]을 반환

# 풀이 요약
# 파일이 있는 모든 칸의 최소 행·열과 최대 행·열을 구한다. 드래그 사각형의 오른쪽·아래 끝은 칸 경계이므로 최대 좌표에 1을 더한다. 각 방향의 극단을 포함해야 모든 파일을 덮으며, 그보다 줄이면 적어도 한 파일을 놓친다.
# 지도 H×W: 시간 O(HW), 보조 공간 O(1).
