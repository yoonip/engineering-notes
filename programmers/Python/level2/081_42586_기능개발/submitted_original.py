def solution(progresses, speeds):
    answer = []
    release_day = 0
    for progress, speed in zip(progresses, speeds):
        days = (100 - progress + speed - 1) // speed
        if days > release_day:
            answer.append(1)
            release_day = days
        else:
            answer[-1] += 1
    return answer

# 전체 코드 줄별 설명
# def solution(progresses, speeds):  # def는 함수 정의. 진도·개발 속도 목록 입력.
#     answer = []  # []는 빈 리스트. 배포 묶음별 기능 수 저장.
#     release_day = 0  # =는 대입. 현재 배포 묶음의 배포일 초기화.
#     for progress, speed in zip(progresses, speeds):  # zip은 같은 위치끼리 묶음. for로 진도·속도를 언패킹.
#         days = (100 - progress + speed - 1) // speed  # //는 정수 몫. 남은 작업량을 속도로 올림 나눠 완료까지의 일수 계산.
#         if days > release_day:  # >는 큼. 앞 묶음 배포일까지 완료되지 않으면 새 배포 필요.
#             answer.append(1)  # append로 새 배포 묶음 생성. 현재 기능 한 개 포함.
#             release_day = days  # 새 묶음의 배포일 갱신.
#         else:  # else는 앞 기능 배포일 전에 이미 완료된 경우.
#             answer[-1] += 1  # [-1]은 마지막 묶음, +=는 더해 저장. 앞 기능과 함께 배포.
#     return answer  # return으로 배포별 기능 수 목록 반환.

# 풀이 요약
# 각 기능의 완료 일수를 올림 계산하고, 앞 기능의 배포일 이하인 기능들은 같은 묶음으로 합칩니다.
# 예: 완료일 [7,3,9]는 [2,1]로 배포. 작업 N개일 때 시간·결과 공간 O(N).
