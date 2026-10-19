from itertools import combinations

def solution(places):
    def valid(room):
        people = [(r, c) for r in range(5) for c in range(5) if room[r][c] == 'P']
        for (r1, c1), (r2, c2) in combinations(people, 2):
            distance = abs(r1 - r2) + abs(c1 - c2)
            if distance == 1:
                return 0
            if distance == 2:
                if r1 == r2:
                    if room[r1][(c1 + c2) // 2] != 'X':
                        return 0
                elif c1 == c2:
                    if room[(r1 + r2) // 2][c1] != 'X':
                        return 0
                elif room[r1][c2] != 'X' or room[r2][c1] != 'X':
                    return 0
        return 1
    return [valid(room) for room in places]

# 전체 코드 줄별 설명
# from itertools import combinations  # itertools의 combinations를 import. 중복 없는 두 사람 조합을 생성하는 함수.
# 
# def solution(places):  # def는 함수 정의, places는 대기실 다섯 개 입력.
#     def valid(room):  # 중첩 함수. 한 대기실의 거리두기 준수 여부 계산.
#         people = [(r, c) for r in range(5) for c in range(5) if room[r][c] == 'P']  # 리스트 내포의 중첩 for·if로 P 좌표 튜플만 수집. [][]는 칸 접근.
#         for (r1, c1), (r2, c2) in combinations(people, 2):  # 두 사람의 좌표를 각각 언패킹하며 순회.
#             distance = abs(r1 - r2) + abs(c1 - c2)  # abs는 절댓값. 행 차이+열 차이로 맨해튼 거리 계산.
#             if distance == 1:  # ==는 같음. 바로 옆 사람 사이에는 파티션을 둘 수 없음.
#                 return 0  # 위반인 대기실은 즉시 0 반환.
#             if distance == 2:  # 거리가 2인 사람 쌍만 추가 검사.
#                 if r1 == r2:  # 같은 행인지 검사.
#                     if room[r1][(c1 + c2) // 2] != 'X':  # //는 정수 몫, !=는 다름. 가운데 칸이 파티션인지 검사.
#                         return 0  # 가로 사이가 열려 있으면 위반.
#                 elif c1 == c2:  # elif는 앞 조건이 거짓일 때 검사. 같은 열인지 확인.
#                     if room[(r1 + r2) // 2][c1] != 'X':  # 세로 가운데 칸 검사.
#                         return 0  # 세로 사이가 열려 있으면 위반.
#                 elif room[r1][c2] != 'X' or room[r2][c1] != 'X':  # or는 하나라도 참. 대각선 두 경유 칸이 모두 막혀야 허용.
#                     return 0  # 대각선 사이의 경로가 하나라도 열려 있으면 위반.
#         return 1  # 모든 사람 쌍을 통과하면 준수.
#     return [valid(room) for room in places]  # 리스트 내포로 각 방을 검사해 순서대로 결과 반환.

# 풀이 요약
# 모든 사람 쌍 중 거리 1은 위반, 거리 2는 사이의 경로가 파티션으로 막혔는지 검사합니다.
# 예: 예제의 둘째 방만 위반해 [1,0,1,1,1]. 한 방의 사람 수 P일 때 시간 O(P²), 공간 O(P); 방 크기는 5×5 고정.
