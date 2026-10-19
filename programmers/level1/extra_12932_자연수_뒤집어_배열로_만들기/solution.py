def solution(n):
    answer = []
    for digit in str(n):
        number = int(digit)
        answer.append(number)
    answer.reverse()
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. n: 입력받은 자연수
#     answer = []  # []는 리스트. =는 값 저장. 뒤집은 숫자들을 저장할 빈 리스트
#     for digit in str(n):  # for·in은 원소를 차례로 꺼내는 반복문. str은 문자열 변환. 숫자를 문자열로 바꿔 자릿수마다 반복.
#         number = int(digit)  # int는 정수 변환. =는 값 저장. 한 자리 문자를 정수로 바꿈.
#         answer.append(number)  # append는 리스트 끝에 추가. 숫자 자릿수를 리스트 뒤에 저장.
#     answer.reverse()  # reverse는 원래 리스트 순서 반전. 리스트 순서를 뒤집어 일의 자리부터 배치.
#     return answer  # return은 결과를 돌려주고 함수 종료. 뒤집어진 숫자들이 들어 있는 리스트 반환

# 풀이 요약
# 정수를 문자열로 바꿔 각 자릿수를 정수로 저장한다. 처음에는 큰 자리부터 들어가므로 마지막에 리스트를 제자리에서 뒤집어 일의 자리부터 나오게 한다.
# 자릿수 D: 시간·공간 O(D).
