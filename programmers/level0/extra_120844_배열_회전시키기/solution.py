def solution(numbers, direction):
    if direction == 'right':
        return numbers[-1:] + numbers[:-1]
    return numbers[1:] + numbers[:1]

# 전체 코드 줄별 설명
# def solution(numbers, direction):  # def는 함수 정의. 정수 리스트와 회전 방향 입력.
#     if direction == 'right':  # if는 조건, ==는 문자열 같음 비교. 오른쪽 회전인지 검사.
#         return numbers[-1:] + numbers[:-1]  # [-1:]은 마지막 원소 리스트, [:-1]은 그 앞부분. +로 마지막을 맨 앞에 연결.
#     return numbers[1:] + numbers[:1]  # [1:]은 첫 원소 이후, [:1]은 첫 원소 리스트. 첫 원소를 맨 뒤에 연결.

# 풀이 요약
# 회전 방향에 따라 끝 원소를 앞으로 또는 첫 원소를 뒤로 옮깁니다.
# 