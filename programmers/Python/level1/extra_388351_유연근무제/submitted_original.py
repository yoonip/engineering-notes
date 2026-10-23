def solution(schedules, timelogs, startday):
    answer = 0

    for i in range(len(schedules)):
        scheduled = schedules[i]
        limit = (scheduled // 100) * 60 + scheduled % 100 + 10
        eligible = True

        for day in range(7):
            weekday = (startday + day - 1) % 7 + 1

            if weekday >= 6:
                continue

            arrival = timelogs[i][day]
            arrival_minutes = (arrival // 100) * 60 + arrival % 100

            if arrival_minutes > limit:
                eligible = False
                break

        if eligible:
            answer += 1

    return answer