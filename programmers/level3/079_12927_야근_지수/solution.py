# 작업량을 정렬한 후 큰 작업들을 같은 높이까지 한 번에 줄입니다. 한 번에 한 시간을 줄이는 힙보다 n이 클 때
# 유리합니다. 남은 횟수는 몫·나머지로 분배합니다.
def solution(n,works):
    if sum(works)<=n:return 0
    levels=sorted(works,reverse=True)+[0]
    for i in range(len(works)):
        width=i+1;cost=(levels[i]-levels[i+1])*width
        if n>=cost:n-=cost;continue
        quotient,remainder=divmod(n,width);height=levels[i]-quotient
        return (width-remainder)*height*height+remainder*(height-1)**2+sum(x*x for x in levels[i+1:])
