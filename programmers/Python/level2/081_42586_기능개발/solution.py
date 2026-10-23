def solution(progresses, speeds):
    answer = []
    # 현재 배포 묶음의 배포일 초기화.
    release_day = 0
    for progress, speed in zip(progresses, speeds):
        # 남은 작업량을 속도로 올림 나눠 완료까지의 일수 계산.
        days = (100 - progress + speed - 1) // speed
        if days > release_day:
            # 현재 기능 한 개 포함.
            answer.append(1)
            release_day = days
        else:
            # 앞 기능과 함께 배포.
            answer[-1] += 1
    return answer
