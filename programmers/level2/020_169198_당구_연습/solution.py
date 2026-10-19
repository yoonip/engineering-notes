def solution(m, n, startX, startY, balls):
    answer = []
    for x, y in balls:
        distances = []
        if not (startY == y and x < startX):
            distances.append((startX + x) ** 2 + (startY - y) ** 2)
        if not (startY == y and x > startX):
            distances.append((2 * m - startX - x) ** 2 + (startY - y) ** 2)
        if not (startX == x and y < startY):
            distances.append((startX - x) ** 2 + (startY + y) ** 2)
        if not (startX == x and y > startY):
            distances.append((startX - x) ** 2 + (2 * n - startY - y) ** 2)
        answer.append(min(distances))
    return answer

# 전체 코드 줄별 설명
# def solution(m, n, startX, startY, balls):  # def는 함수 정의. () 안은 당구대 크기·시작 좌표·목표 공 목록 입력.
#     answer = []  # []는 빈 리스트. 각 목표까지의 최소 거리 제곱 저장.
#     for x, y in balls:  # for~in으로 목표 좌표를 두 변수에 언패킹하며 순회.
#         distances = []  # 네 벽을 거치는 유효한 거리 제곱 후보를 담을 리스트.
#         if not (startY == y and x < startX):  # not은 참·거짓 반전, and는 둘 다 참. 왼쪽 벽 전에 목표를 먼저 맞히는 경우 제외.
#             distances.append((startX + x) ** 2 + (startY - y) ** 2)  # append는 리스트 끝에 추가, **2는 제곱. 왼쪽 벽 대칭점까지 거리 제곱.
#         if not (startY == y and x > startX):  # 같은 높이에서 오른쪽 목표를 먼저 맞히는 경우 제외. ()는 조건을 묶음.
#             distances.append((2 * m - startX - x) ** 2 + (startY - y) ** 2)  # *는 곱셈. 오른쪽 벽에 비친 목표까지의 거리 제곱 추가.
#         if not (startX == x and y < startY):  # ==는 같음, <는 작음. 아래쪽 벽에 닿기 전 목표를 맞히는 경우 제외.
#             distances.append((startX - x) ** 2 + (startY + y) ** 2)  # 아래쪽 벽을 기준으로 반사한 목표까지 거리 제곱 추가.
#         if not (startX == x and y > startY):  # if는 조건 분기. 위쪽 벽 전에 목표를 맞히는 경우 제외.
#             distances.append((startX - x) ** 2 + (2 * n - startY - y) ** 2)  # 위쪽 벽을 기준으로 반사한 목표까지 거리 제곱 추가.
#         answer.append(min(distances))  # min은 최솟값. 유효한 네 방향 중 최소값을 정답 목록에 추가.
#     return answer  # return으로 목표 공 순서의 결과 리스트 반환.

# 풀이 요약
# 목표 공을 네 벽에 대칭시켜 반사 경로를 직선으로 바꿉니다. 벽 전에 목표 공을 먼저 맞히는 방향은 제외합니다.
# 예: (3,7)에서 (7,7)은 아래·위 벽 후보 중 위 벽을 거치면 거리 제곱 52. 공 B개일 때 시간·결과 공간 O(B).
