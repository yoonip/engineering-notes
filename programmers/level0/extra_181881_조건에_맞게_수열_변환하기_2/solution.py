def solution(arr):
    longest = 0
    for value in set(arr):
        steps = 0
        while True:
            following = value // 2 if value >= 50 and value % 2 == 0 else value * 2 + 1 if value < 50 and value % 2 == 1 else value
            if following == value:
                break
            value = following
            steps += 1
        longest = max(longest, steps)
    return longest

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 변환할 정수 리스트 입력.
#     longest = 0  # 원소들이 고정될 때까지 걸리는 횟수의 최댓값 초기화.
#     for value in set(arr):  # set은 중복 없는 집합. 같은 시작값은 변화 과정도 같으므로 한 번만 계산.
#         steps = 0  # 현재 값의 변화 횟수 초기화.
#         while True:  # while은 반복, True는 항상 참. 값이 고정되면 break로 종료.
#             following = value // 2 if value >= 50 and value % 2 == 0 else value * 2 + 1 if value < 50 and value % 2 == 1 else value  # 조건 표현식과 and로 변환 선택. //는 정수 나눗셈, %는 나머지.
#             if following == value:  # if는 조건, ==는 같음 비교. 다음 값이 같으면 고정 상태.
#                 break  # 가장 가까운 반복문 종료. 변화가 없는 마지막 시도는 세지 않음.
#             value = following  # 다음 변환에 사용할 값 갱신.
#             steps += 1  # +=는 더해 저장. 실제로 값이 바뀐 횟수 증가.
#         longest = max(longest, steps)  # max는 최댓값. 가장 늦게 고정되는 원소의 횟수 유지.
#     return longest  # 모든 원소가 동시에 고정되기까지 필요한 반복 횟수 반환.

# 풀이 요약
# 원소들은 독립적으로 변합니다. 각 값이 고정되기까지의 횟수 중 최댓값이 전체 배열의 고정 시점입니다.
# 