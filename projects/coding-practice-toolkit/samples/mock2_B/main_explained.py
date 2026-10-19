# 정렬된 기록에서 값이 L 이상 R 이하인 원소 수를 구한다.
# 두 경계 위치를 이분탐색으로 찾으면 질문마다 배열 전체를 다시 읽지 않아도 된다.
# 왼쪽은 L 이상 첫 위치, 오른쪽은 R 초과 첫 위치다. 위치 차이가 중복을 포함한 개수다.
# 입력 제한과 실행 비용: 시간 O(N+Q log N), 배열 공간 O(N). Python 파싱·출력 포함 O(N+Q).

# a는 비내림차순 기록이다. lo와 hi는 경계를 찾는 반열린 구간 [lo,hi)를 표현한다.
# strict가 거짓이면 >= x, 참이면 > x인 첫 위치를 찾는다.
# hi=n도 유효한 반환값이다. 범위 밖 배열을 읽는 것이 아니라 모든 값 뒤의 삽입 위치를 뜻한다.

# sys.stdin.buffer는 입력을 바이트로 읽는다. read는 전체 입력을 메모리에 올린다는 점을 고려한다.
# 문자열이 필요하면 decode하고 숫자가 필요하면 int로 바꾼다. 정수는 큰 값도 자동 확장된다.

import sys
it=iter(map(int,sys.stdin.buffer.read().split()))
n,q=next(it),next(it)
a=[next(it) for _ in range(n)]
# bound는 조건을 처음 만족하는 위치를 반환한다.
# 조건을 만족한 중간값은 오른쪽 후보를 mid로 줄이고, 아니면 왼쪽을 mid+1로 옮긴다.
# 왼쪽 경계를 찾는 함수와 오른쪽 경계를 찾는 함수는 비교의 등호 유무만 다르다.
def bound(x,strict):
    lo,hi=0,n
    # lo<hi인 동안 아직 한 위치로 좁혀지지 않았다.
    # 중간값은 lo+(hi-lo)/2로 계산하며 구간이 매번 줄어 O(log N)에 끝난다.
    while lo<hi:
        mid=lo+(hi-lo)//2
        # 조건이 참이면 첫 만족 위치는 mid 또는 그 왼쪽에 있다.
        # 조건이 거짓이면 mid까지는 제외하므로 lo를 mid+1로 옮긴다.
        if (a[mid]>x if strict else a[mid]>=x): hi=mid
        else: lo=mid+1
    return lo # 찾는 값이 없으면 n, 처음부터 만족하면 0도 반환할 수 있다.
out=[]
# L과 R은 배열 인덱스가 아니라 값의 범위다.
# bound(R,참)-bound(L,거짓)이 구간 [L,R] 안의 원소 개수다.
# 같은 값도 차지하는 위치 수만큼 세며 음수 역시 같은 비교 규칙을 따른다.
for _ in range(q):
    l,r=next(it),next(it)
    out.append(str(bound(r,True)-bound(l,False))) # 오른쪽은 >R, 왼쪽은 >=L이므로 R과 같은 값도 포함한다.
print('\n'.join(out))

# 손으로 확인: L=2,R=4
# 손으로 확인: L이상 첫 위치=1
# 손으로 확인: R초과 첫 위치=4
# 손으로 확인: 개수4-1=3
# 완성 후 확인: L,R을 인덱스로 해석하지 않는다.
# 완성 후 확인: 오른쪽 경계는 strict > R.
# 완성 후 확인: 중복된 값도 원소별로 센다.
