# 모든 광고 시작 초마다 각 시청 구간과 겹치는 길이를 직접 더합니다. 시작 포함·끝 제외 구간과 가장 이른 동점 선택을
# 독립적으로 확인합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(play_time,adv_time,logs):
    def sec(text):
        h,m,s=map(int,text.split(':'));return h*3600+m*60+s
    play,adv=sec(play_time),sec(adv_time)
    ranges=[tuple(map(sec,line.split('-'))) for line in logs]
    best=0;maximum=-1
    for start in range(play-adv+1):
        total=sum(max(0,min(end,start+adv)-max(begin,start)) for begin,end in ranges)
        if total>maximum:best,maximum=start,total
    h,rest=divmod(best,3600);m,s=divmod(rest,60)
    return f'{h:02d}:{m:02d}:{s:02d}'
