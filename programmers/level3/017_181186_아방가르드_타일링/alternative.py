# 처음 세로로 끊을 수 있는 블록의 폭을 모두 합산합니다. 폭 1·2·3의 개수는 1·2·5, 그 뒤는 폭이 3의 배수이면
# 4, 아니면 2입니다. 압축 점화식을 쓰지 않아 작은 폭 검증에 적합합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(n):
    mod = 1000000007
    dp = [1]+[0]*n
    for width in range(1,n+1):
        for block in range(1,width+1):
            ways = (1,2,5)[block-1] if block<=3 else (4 if block%3==0 else 2)
            dp[width] += dp[width-block]*ways
        dp[width] %= mod
    return dp[n]
