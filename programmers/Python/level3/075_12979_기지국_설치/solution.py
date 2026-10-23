# 아파트 수·정렬된 기존 기지국·전파 반경을 받음.
def solution(n, stations, w):
    # 양쪽 w개와 본인 한 개.
    coverage = 2 * w + 1
    # 아직 기존 전파로 덮이지 않은 구간의 시작 아파트 번호.
    next_start = 1
    # 추가로 설치할 기지국 수.
    answer = 0
    # for로 기존 기지국을 왼쪽부터 순회.
    for station in stations:
        # 기존 전파 시작점 직전까지의 빈 구간 길이.
        gap = station - w - next_start
        # 빈 구간이 있을 때만 설치 수 추가.
        if gap > 0:
            # 마지막 구간도 같은 올림 나눗셈으로 채움.
            answer += (gap + coverage - 1) // coverage
        # 현재 전파가 끝난 다음 아파트로 이동하며 겹치는 구간도 처리.
        next_start = max(next_start, station + w + 1)
    # 마지막 기존 전파 뒤에 아파트가 남았는지 확인.
    if next_start <= n:
        # 양 끝을 포함한 남은 구간 길이.
        gap = n - next_start + 1
        # 마지막 구간도 같은 올림 나눗셈으로 채움.
        answer += (gap + coverage - 1) // coverage
    # 전체 빈 구간에 필요한 추가 기지국 수 반환.
    return answer
