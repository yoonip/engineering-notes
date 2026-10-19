# 문자 사이에 구분자를 넣어 홀수·짝수 중심을 하나로 만듭니다. 가장 오른쪽 팰린드롬의 대칭 정보를 재사용해 이미 확인한
# 글자를 다시 비교하지 않습니다.
def solution(s):
    text='^#'+'#'.join(s)+'#$'
    radius=[0]*len(text);center=right=0;answer=0
    for i in range(1,len(text)-1):
        if i<right:radius[i]=min(right-i,radius[2*center-i])
        while text[i+radius[i]+1]==text[i-radius[i]-1]:radius[i]+=1
        if i+radius[i]>right:center,right=i,i+radius[i]
        answer=max(answer,radius[i])
    return answer
