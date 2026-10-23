def solution(n, stations, w):
    coverage = 2 * w + 1
    next_start = 1
    answer = 0
    for station in stations:
        gap = station - w - next_start
        if gap > 0:
            answer += (gap + coverage - 1) // coverage
        next_start = max(next_start, station + w + 1)
    if next_start <= n:
        gap = n - next_start + 1
        answer += (gap + coverage - 1) // coverage
    return answer

# 전체 코드 줄별 설명
# def solution(n, stations, w):  # def는 함수 정의. 아파트 수·정렬된 기존 기지국·전파 반경을 받음.
#     coverage = 2 * w + 1  # 한 기지국이 덮는 연속 아파트 수. 양쪽 w개와 본인 한 개.
#     next_start = 1  # 아직 기존 전파로 덮이지 않은 구간의 시작 아파트 번호.
#     answer = 0  # 추가로 설치할 기지국 수.
#     for station in stations:  # for로 기존 기지국을 왼쪽부터 순회.
#         gap = station - w - next_start  # 기존 전파 시작점 직전까지의 빈 구간 길이.
#         if gap > 0:  # >는 초과. 빈 구간이 있을 때만 설치 수 추가.
#             answer += (gap + coverage - 1) // coverage  # +=는 더해 저장, //는 정수 나눗셈. 양수 나눗셈을 올림해 필요한 최소 개수 계산.
#         next_start = max(next_start, station + w + 1)  # max는 큰 값. 현재 전파가 끝난 다음 아파트로 이동하며 겹치는 구간도 처리.
#     if next_start <= n:  # 마지막 기존 전파 뒤에 아파트가 남았는지 확인.
#         gap = n - next_start + 1  # 양 끝을 포함한 남은 구간 길이.
#         answer += (gap + coverage - 1) // coverage  # 마지막 구간도 같은 올림 나눗셈으로 채움.
#     return answer  # 전체 빈 구간에 필요한 추가 기지국 수 반환.

# 풀이 요약
# 기존 전파 구간 사이의 빈 구간을 각각 길이 2W+1짜리 전파로 채운다. 길이 L 구간에는 ceil(L/(2W+1))개가 최소로 필요하다.
# 예: N=11, 기지국 4·11, W=1이면 빈 구간 길이가 2·4라서 1+2=3개. 새 기지국은 왼쪽 미포함 지점을 덮으며 최대한 오른쪽에 놓으면 된다.
# 기존 기지국 S개일 때 시간 O(S), 공간 O(1). N이 2억이어도 N개 배열이나 반복이 필요 없다.
# 