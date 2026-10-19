def solution(n):
    digits = []
    text = str(n)
    for digit in text:
        digits.append(digit)
    digits.sort()
    digits.reverse()
    answer = ""
    for digit in digits:
        answer = answer + digit
    return int(answer)

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 정수 n을 입력받는 함수
#     digits = []  # []는 리스트. =는 값 저장. 각 자릿수 문자를 모을 리스트.
#     text = str(n)  # str은 문자열 변환. =는 값 저장. 정수를 자릿수 문자열로 변환.
#     for digit in text:  # for·in은 원소를 차례로 꺼내는 반복문. 왼쪽부터 각 자릿수 문자를 읽음.
#         digits.append(digit)  # append는 리스트 끝에 추가. 자릿수 문자를 리스트에 추가.
#     digits.sort()  # sort는 원래 리스트 정렬. 자릿수를 작은 순서로 정렬.
#     digits.reverse()  # reverse는 원래 리스트 순서 반전. 순서를 뒤집어 큰 자릿수가 앞에 오게 함.
#     answer = ""  # =는 값 저장. 결과 문자열 초기화.
#     for digit in digits:  # for·in은 원소를 차례로 꺼내는 반복문. 내림차순 자릿수를 읽음.
#         answer = answer + digit  # =는 값 저장. 현재 자릿수를 결과 뒤에 연결.
#     return int(answer)  # return은 결과를 돌려주고 함수 종료. int는 정수 변환. 완성된 숫자 문자열을 정수로 반환.

# 풀이 요약
# 자릿수 문자를 리스트에 모아 오름차순 정렬한 뒤 뒤집는다. 같은 자릿수들을 큰 수부터 앞에 배치해야 가장 큰 수가 된다. 이어 붙인 문자열을 int로 바꿔 반환한다.
# 자릿수 D: 정렬 O(D log D), 반복 문자열 연결까지 고려한 시간 상한 O(D²), 공간 O(D).
