def solution(sizes):
    max_width = 0
    max_height = 0
    for width, height in sizes:
        long_side = max(width, height)
        short_side = min(width, height)
        max_width = max(max_width, long_side)
        max_height = max(max_height, short_side)
    return max_width * max_height

def solution(sizes):
    max_width = 0
    max_height = 0
    for width, height in sizes:
        long_side = max(width, height)
        short_side = min(width, height)
        if long_side > max_width:
            max_width = long_side
        if short_side > max_height:
            max_height = short_side
    return max_width * max_height

# 전체 코드 줄별 설명
# def solution(sizes):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. sizes: 각 명함의 [가로, 세로]가 들어 있는 리스트
#     max_width = 0  # =는 값 저장. 모든 명함을 넣는 데 필요한 가로 길이. 처음에는 0으로 시작
#     max_height = 0  # =는 값 저장. 모든 명함을 넣는 데 필요한 세로 길이. 처음에는 0으로 시작
#     for width, height in sizes:  # for·in은 원소를 차례로 꺼내는 반복문. 명함을 하나씩 꺼내 가로와 세로를 각각 변수에 저장
#         long_side = max(width, height)  # max는 최댓값. =는 값 저장. 두 길이 중 큰 값 → 이 명함의 가로로 사용할 길이
#         short_side = min(width, height)  # min은 최솟값. =는 값 저장. 두 길이 중 작은 값 → 이 명함의 세로로 사용할 길이
#         max_width = max(max_width, long_side)  # max는 최댓값. =는 값 저장. 지금까지 확인한 긴 변 중 가장 큰 값을 유지
#         max_height = max(max_height, short_side)  # max는 최댓값. =는 값 저장. 지금까지 확인한 짧은 변 중 가장 큰 값을 유지
#     return max_width * max_height  # return은 결과를 돌려주고 함수 종료. 필요한 가로 길이 × 세로 길이로 최소 넓이를 반환
# 
# def solution(sizes):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. sizes: 각 명함의 [가로, 세로]가 들어 있는 리스트
#     max_width = 0  # =는 값 저장. 모든 명함을 넣는 데 필요한 가로 길이. 처음에는 0으로 시작
#     max_height = 0  # =는 값 저장. 모든 명함을 넣는 데 필요한 세로 길이. 처음에는 0으로 시작
#     for width, height in sizes:  # for·in은 원소를 차례로 꺼내는 반복문. 명함을 하나씩 꺼내 가로와 세로를 각각 변수에 저장
#         long_side = max(width, height)  # max는 최댓값. =는 값 저장. 두 길이 중 큰 값 → 이 명함의 가로로 사용할 길이
#         short_side = min(width, height)  # min은 최솟값. =는 값 저장. 두 길이 중 작은 값 → 이 명함의 세로로 사용할 길이
#         if long_side > max_width:  # if는 조건이 참일 때 실행. >는 큼 비교. 긴 변의 최대 길이를 새로 갱신해야 하는지 비교.
#             max_width = long_side  # =는 값 저장. 새로운 최대 긴 변 길이 저장.
#         if short_side > max_height:  # if는 조건이 참일 때 실행. >는 큼 비교. 짧은 변의 최대 길이를 갱신해야 하는지 비교.
#             max_height = short_side  # =는 값 저장. 새로운 최대 짧은 변 길이 저장.
#     return max_width * max_height  # return은 결과를 돌려주고 함수 종료. 필요한 가로 길이 × 세로 길이로 최소 넓이를 반환

# 풀이 요약
# 명함의 긴 변을 가로, 짧은 변을 세로로 통일한다. 가장 긴 긴 변과 가장 긴 짧은 변을 각각 수용하는 지갑이면 전부 들어간다. 두 최대 길이보다 작게 줄일 수는 없으므로 그 곱이 최소 넓이다.
# 명함 N개: 시간 O(N), 보조 공간 O(1).
