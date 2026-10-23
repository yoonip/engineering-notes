def solution(x):
    digit_sum = sum(map(int, str(x)))
    answer = (x % digit_sum == 0)
    return answer

# 전체 코드 줄별 설명
# def solution(x):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 자연수 x를 입력받는 함수
#     digit_sum = sum(map(int, str(x)))  # str은 문자열 변환. sum은 원소 합. map은 각 원소에 함수 적용. =는 값 저장. x를 문자열로 바꾸고, 각 문자를 정수로 변환한 뒤 모두 더함
#     answer = (x % digit_sum == 0)  # ==는 같음 비교. %는 나머지. =는 값 저장. x를 자릿수의 합으로 나눈 나머지가 0이면 True, 아니면 False
#     return answer  # return은 결과를 돌려주고 함수 종료. 하샤드 수인지 판단한 결과 반환

# 풀이 요약
# 숫자를 문자열로 바꿔 자릿수마다 정수로 변환한 뒤 더한다. 원래 수를 자릿수 합으로 나눈 나머지가 0이면 하샤드 수다. 비교식 자체가 True 또는 False를 만든다.
# 자릿수 D: 시간 O(D), 문자열 저장 공간 O(D).
