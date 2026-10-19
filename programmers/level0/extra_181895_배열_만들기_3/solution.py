def solution(arr, intervals):
    (a, b), (c, d) = intervals
    return arr[a:b + 1] + arr[c:d + 1]

# 전체 코드 줄별 설명
# def solution(arr, intervals):  # def는 함수 정의. 원본 리스트와 두 구간 입력.
#     (a, b), (c, d) = intervals  # 중첩 분해 대입. 두 구간의 양 끝 인덱스를 각각 받음.
#     return arr[a:b + 1] + arr[c:d + 1]  # 슬라이싱의 끝은 제외라 1을 더함. +는 두 부분 리스트 연결.

# 풀이 요약
# 두 닫힌 구간을 잘라낸 뒤 주어진 순서대로 붙입니다.
# 