from itertools import combinations

def solution(line):
    points = set()
    for first, second in combinations(line, 2):
        a, b, e = first
        c, d, f = second
        denominator = a * d - b * c
        if denominator == 0:
            continue
        nx, ny = b * f - e * d, e * c - a * f
        if nx % denominator == 0 and ny % denominator == 0:
            points.add((nx // denominator, ny // denominator))
    min_x = min(x for x, y in points)
    max_x = max(x for x, y in points)
    min_y = min(y for x, y in points)
    max_y = max(y for x, y in points)
    board = [['.'] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for x, y in points:
        board[max_y - y][x - min_x] = '*'
    return [''.join(row) for row in board]

# 전체 코드 줄별 설명
# from itertools import combinations  # itertools의 combinations를 import. 중복 없이 두 직선을 고르는 조합 생성 함수.
# 
# def solution(line):  # def는 함수 정의. line은 직선 계수 목록.
#     points = set()  # set은 중복 없는 집합. 정수 좌표 교점 저장.
#     for first, second in combinations(line, 2):  # 모든 두 직선 조합을 for로 순회해 두 목록 언패킹.
#         a, b, e = first  # 첫 직선 ax+by+e=0의 계수 언패킹.
#         c, d, f = second  # 둘째 직선 cx+dy+f=0의 계수 언패킹.
#         denominator = a * d - b * c  # *는 곱셈. 두 식을 소거할 때의 공통 분모 계산.
#         if denominator == 0:  # ==는 같음. 평행한 직선은 유일한 교점이 없음.
#             continue  # continue로 다음 직선 쌍 처리.
#         nx, ny = b * f - e * d, e * c - a * f  # 소거 공식의 x·y 분자를 각각 계산.
#         if nx % denominator == 0 and ny % denominator == 0:  # %는 나머지, and는 둘 다 참. 두 좌표 모두 정수인지 검사.
#             points.add((nx // denominator, ny // denominator))  # //는 정수 몫, ()는 좌표 튜플, add는 집합에 추가.
#     min_x = min(x for x, y in points)  # min은 최솟값. 생성식으로 가장 왼쪽 x 계산.
#     max_x = max(x for x, y in points)  # max는 최댓값. 가장 오른쪽 x 계산.
#     min_y = min(y for x, y in points)  # 가장 아래 y 계산.
#     max_y = max(y for x, y in points)  # 가장 위 y 계산.
#     board = [['.'] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]  # 리스트 내포로 독립된 행 생성. _는 안 쓰는 변수, 점으로 최소 사각형 초기화.
#     for x, y in points:  # 정수 교점의 두 좌표를 언패킹하며 순회.
#         board[max_y - y][x - min_x] = '*'  # [][]는 행·열 접근. y가 클수록 위쪽 행, x는 왼쪽 경계 기준으로 변환.
#     return [''.join(row) for row in board]  # join은 문자들을 연결. 리스트 내포로 각 행을 문자열로 바꿔 반환.

# 풀이 요약
# 두 직선의 교점을 정수 나눗셈으로 판정해 모으고, 모든 점의 최소 사각형에 별을 찍습니다. 화면의 행 방향은 y축과 반대입니다.
# 예: y=1의 교점 x=-1,1이면 '*.*'. 직선 N개·출력 넓이 A일 때 시간 O(N²+A), 공간 O(교점 수+A).
