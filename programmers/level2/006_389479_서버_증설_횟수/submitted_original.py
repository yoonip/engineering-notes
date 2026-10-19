def solution(players, m, k):
    expires = [0] * (len(players) + k)
    active = 0
    answer = 0
    for hour, people in enumerate(players):
        active -= expires[hour]
        added = max(0, people // m - active)
        active += added
        answer += added
        expires[hour + k] += added
    return answer

# 전체 코드 줄별 설명 (아래는 모두 실행되지 않는 주석입니다.)
# def solution(players, m, k):  # def는 함수 정의. players·m·k는 함수 입력 매개변수.
#     expires = [0] * (len(players) + k)  # len은 원소 수. [0]*길이는 0으로 채운 리스트. k시간 뒤까지 만료 기록 공간 확보.
#     active = 0  # 현재 가동 중인 증설 서버 수 초기화. =는 대입.
#     answer = 0  # 총 증설 횟수 초기화.
#     for hour, people in enumerate(players):  # enumerate는 (인덱스,값)을 제공. hour·people로 시간과 인원을 언패킹.
#         active -= expires[hour]  # []는 인덱싱. -=는 빼서 저장. 이번 시간에 만료된 서버 제거.
#         added = max(0, people // m - active)  # //는 몫 내림, max는 큰 값 선택. 필요한 서버에서 현재 서버를 뺀 부족분 계산.
#         active += added  # +=는 더해서 저장. 새 서버를 가동 수에 반영.
#         answer += added  # 추가한 수만큼 정답 누적.
#         expires[hour + k] += added  # k시간 뒤의 만료 칸에 추가 서버 수 기록.
#     return answer  # return으로 전체 증설 횟수 반환.

# 풀이 요약
# 매 시간 만료 서버를 먼저 빼고, 필요한 서버 수 people//m에서 부족한 만큼만 증설합니다.
# 새 서버는 hour+k에 만료됩니다. 시간·공간 O(시간 수+k).
# 예: m=3, 현재 2대, 이용자 10명이면 10//3=3대가 필요하므로 1대를 추가합니다.
