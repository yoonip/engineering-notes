def solution(dirs):
    moves = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}
    x = y = 0
    edges = set()
    for command in dirs:
        dx, dy = moves[command]
        nx, ny = x + dx, y + dy
        if -5 <= nx <= 5 and -5 <= ny <= 5:
            edge = tuple(sorted(((x, y), (nx, ny))))
            edges.add(edge)
            x, y = nx, ny
    return len(edges)

# 전체 코드 줄별 설명
# def solution(dirs):  # def는 함수 정의. dirs는 이동 명령 문자열 입력.
#     moves = {'U': (0, 1), 'D': (0, -1), 'R': (1, 0), 'L': (-1, 0)}  # {} 딕셔너리에 명령별 이동량 () 튜플 저장.
#     x = y = 0  # 연쇄 대입으로 시작 좌표를 원점으로 초기화.
#     edges = set()  # set은 중복 없는 집합. 지나간 무방향 길 저장.
#     for command in dirs:  # for~in으로 명령 순회.
#         dx, dy = moves[command]  # [키]의 이동량을 두 변수로 언패킹.
#         nx, ny = x + dx, y + dy  # +로 다음 좌표 계산.
#         if -5 <= nx <= 5 and -5 <= ny <= 5:  # 연쇄 비교로 경계 검사. and는 두 조건 모두 참.
#             edge = tuple(sorted(((x, y), (nx, ny))))  # sorted로 양끝 좌표 순서 통일, tuple로 불변 키 생성. 반대 방향 이동도 같은 길로 표현.
#             edges.add(edge)  # add로 길 추가. 이미 지나간 길은 중복되지 않음.
#             x, y = nx, ny  # 유효한 이동에서만 현재 좌표 갱신.
#     return len(edges)  # len은 원소 수. return으로 서로 다른 길 개수 반환.

# 풀이 요약
# 이동한 칸이 아닌 두 좌표 사이의 길을 집합에 저장합니다. 양끝을 정렬해 왕복도 같은 길로 셉니다.
# 예: 'ULURRDLLU'의 9번 이동 중 새 길은 7개. 명령 N개에 시간 O(N), 길 집합은 고정 격자 안에서 최대 220개.
