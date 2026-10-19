def solution(n):
    answer = []
    def move(count, start, goal, spare):
        if count == 0:
            return
        move(count - 1, start, spare, goal)
        answer.append([start, goal])
        move(count - 1, spare, goal, start)
    move(n, 1, 3, 2)
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 옮길 원판 수 입력.
#     answer = []  # []는 리스트. [출발 기둥,도착 기둥] 이동 순서 저장.
#     def move(count, start, goal, spare):  # 내부 재귀 함수. 재귀는 함수가 자기 자신을 호출해 작은 문제를 푸는 방식.
#         if count == 0:  # ==는 같음. 옮길 원판이 없으면 재귀 종료.
#             return  # 반환값 없이 현재 함수 호출만 끝냄.
#         move(count - 1, start, spare, goal)  # 위의 작은 원판들을 보조 기둥으로 옮겨 가장 큰 원판을 노출.
#         answer.append([start, goal])  # append는 끝에 추가. 가장 큰 원판 하나를 목적지로 이동.
#         move(count - 1, spare, goal, start)  # 보조 기둥의 작은 원판들을 목적지의 큰 원판 위로 옮김.
#     move(n, 1, 3, 2)  # 원판 n개를 1번에서 3번으로 옮기고 2번을 보조로 사용.
#     return answer  # 최소 이동 순서 반환.

# 풀이 요약
# n개 이동은 위 n-1개를 보조로 이동→가장 큰 원판 하나 이동→n-1개를 목적지로 이동이다.
# 예: n=2는 1→2,1→3,2→3. 이동 수는 T(n)=2T(n-1)+1=2^n-1로 최소다. 시간·결과 공간 O(2^N), 재귀 깊이 O(N).
# 