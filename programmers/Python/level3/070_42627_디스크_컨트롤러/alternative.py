# 매번 도착한 미처리 작업 중 (소요시간, 요청시각, 번호)가 가장 작은 것을 고릅니다. 현재 지문의 우선순위를 그대로
# 따르며 힙 없이 구현합니다.
def solution(jobs):
    pending=set(range(len(jobs)));now=total=0
    while pending:
        ready=[i for i in pending if jobs[i][0]<=now]
        if not ready:now=min(jobs[i][0] for i in pending);continue
        i=min(ready,key=lambda i:(jobs[i][1],jobs[i][0],i));pending.remove(i)
        now+=jobs[i][1];total+=now-jobs[i][0]
    return total//len(jobs)
