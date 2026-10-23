# 00:00부터 마지막 버스 시각까지 콘을 실제 대기열에 넣어 탑승 여부를 확인합니다. 같은 시각 크루가 먼저 타므로 콘은
# 동점에서 뒤에 둡니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(n,t,m,timetable):
    crews=[int(s[:2])*60+int(s[3:]) for s in timetable]
    def boards(arrival):
        people=sorted([(x,0) for x in crews]+[(arrival,1)])
        index=0
        for bus in range(n):
            departure=540+bus*t;seats=0
            while index<len(people) and people[index][0]<=departure and seats<m:
                if people[index][1]:return True
                index+=1;seats+=1
        return False
    best=max(minute for minute in range(540+(n-1)*t+1) if boards(minute))
    return f'{best//60:02d}:{best%60:02d}'
