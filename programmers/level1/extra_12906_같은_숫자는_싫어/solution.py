def solution(arr):
    answer = []
    previous = -1
    for number in arr:
        if number != previous:
            answer.append(number)
        previous = number
    return answer

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 연속 중복을 줄일 배열을 입력받음.
#     answer = []  # []는 리스트. =는 값 저장. 결과 리스트 초기화.
#     previous = -1  # =는 값 저장. 입력 범위 0~9와 다른 값으로 이전 수 초기화.
#     for number in arr:  # for·in은 원소를 차례로 꺼내는 반복문. 원래 순서대로 숫자를 확인.
#         if number != previous:  # if는 조건이 참일 때 실행. !=는 다름 비교. 직전 숫자와 달라 새 구간이 시작되는지 검사.
#             answer.append(number)  # append는 리스트 끝에 추가. 처음 나온 연속 구간의 숫자만 추가.
#         previous = number  # =는 값 저장. 다음 비교에 사용할 직전 숫자 갱신.
#     return answer  # return은 결과를 돌려주고 함수 종료. 연속 중복을 제거한 배열 반환.

# 풀이 요약
# 현재 수와 직전 수가 다를 때만 결과에 넣는다. 값이 예전에 나왔더라도 바로 앞과 다르면 다시 넣어야 하므로 집합으로 전체 중복을 지우면 안 된다. 초기 이전 값 -1은 입력 범위 0~9에 없어서 첫 원소가 항상 들어간다.
# 원소 N개: 시간 O(N), 결과 공간 O(N).
