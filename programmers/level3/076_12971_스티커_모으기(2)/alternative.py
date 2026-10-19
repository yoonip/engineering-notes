# 선택할 스티커 집합을 모두 만들고 인접 선택을 배제합니다. 첫 칸·마지막 칸의 연결까지 직접 검사하므로 원형 DP의 분리를
# 확인합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(sticker):
    n=len(sticker)
    if n==1:return sticker[0]
    best=0
    for mask in range(1<<n):
        if any(mask>>i&1 and mask>>((i+1)%n)&1 for i in range(n)):continue
        best=max(best,sum(sticker[i] for i in range(n) if mask>>i&1))
    return best
