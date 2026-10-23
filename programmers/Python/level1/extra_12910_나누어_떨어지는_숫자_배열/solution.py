def solution(arr, divisor):
    answer = []
    for number in arr:
        if number % divisor == 0:
            answer.append(number)
    if len(answer) == 0:
        return [-1]
    answer.sort()
    return answer

def solution(arr, divisor):
    answer = []
    for number in arr:
        if number % divisor ==0:
            answer.append(number)
    if len(answer) ==0:
        return [-1]
    answer.sort()
    return answer

# 전체 코드 줄별 설명
# def solution(arr, divisor):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 숫자 배열 arr와 나눌 수 divisor를 입력받습니다.
#     answer = []  # []는 리스트. =는 값 저장. 조건에 맞는 숫자를 담을 빈 리스트를 만듭니다.
#     for number in arr:  # for·in은 원소를 차례로 꺼내는 반복문. 배열의 각 수를 확인.
#         if number % divisor == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. 지정한 수로 나누어떨어지는지 확인.
#             answer.append(number)  # append는 리스트 끝에 추가. 나누어떨어지는 수를 결과에 저장.
#     if len(answer) == 0:  # if는 조건이 참일 때 실행. len은 길이. ==는 같음 비교. 조건을 만족한 수가 없는지 확인.
#         return [-1]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 정수가 아닌, -1을 담은 리스트를 반환합니다.
#     answer.sort()  # sort는 원래 리스트 정렬. 남긴 수들을 오름차순 정렬.
#     return answer  # return은 결과를 돌려주고 함수 종료. 정렬한 결과 리스트 반환.
# 
# def solution(arr, divisor):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 숫자 배열 arr와 나눌 수 divisor를 입력받습니다.
#     answer = []  # []는 리스트. =는 값 저장. 조건에 맞는 숫자를 담을 빈 리스트를 만듭니다.
#     for number in arr:  # for·in은 원소를 차례로 꺼내는 반복문. 배열 원소를 하나씩 확인.
#         if number % divisor ==0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. 나눗셈의 나머지가 0인지 확인.
#             answer.append(number)  # append는 리스트 끝에 추가. 조건을 만족한 수를 추가.
#     if len(answer) ==0:  # if는 조건이 참일 때 실행. len은 길이. ==는 같음 비교. 남은 수가 없는지 확인.
#         return [-1]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 정수가 아닌, -1을 담은 리스트를 반환합니다.
#     answer.sort()  # sort는 원래 리스트 정렬. 결과를 작은 수부터 정렬.
#     return answer  # return은 결과를 돌려주고 함수 종료. 최종 결과 반환.

# 풀이 요약
# 각 수를 divisor로 나눈 나머지가 0일 때만 남긴다. 남은 값이 없으면 [-1]을 반환하고, 있으면 오름차순 정렬한다. 입력 순서를 그대로 반환하면 정렬 조건을 놓친다.
# 원소 N개, 남긴 K개: 시간 O(N+K log K), 공간 O(K).
