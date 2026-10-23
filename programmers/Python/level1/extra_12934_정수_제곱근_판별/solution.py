from math import isqrt

def solution(n):
    x = isqrt(n)
    if x * x == n:
        return (x + 1) ** 2
    return -1

# 전체 코드 줄별 설명
# from math import isqrt  # from math import는 math 모듈에서 이름을 가져옴. isqrt는 제곱근을 내림한 정수를 구하는 함수. math 모듈에서 정수 제곱근을 구하는 isqrt 함수 가져오기
# 
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 자연수 n을 입력받는 함수
#     x = isqrt(n)  # isqrt는 내림한 정수 제곱근. =는 값 저장. n의 제곱근에서 소수 부분을 버린 정수 구하기
#     if x * x == n:  # if는 조건이 참일 때 실행. ==는 같음 비교. x의 제곱이 n과 같으면 완전제곱수
#         return (x + 1) ** 2  # return은 결과를 돌려주고 함수 종료. **는 거듭제곱. 제곱근에 1을 더한 뒤 제곱하여 반환
#     return -1  # return은 결과를 돌려주고 함수 종료. 완전제곱수가 아니라면 -1 반환

# 풀이 요약
# isqrt는 n의 제곱근을 내림한 정수를 돌려준다. 그 수의 제곱이 n과 같을 때만 완전제곱수이므로 다음 정수의 제곱을 반환한다. 그렇지 않으면 -1이다. 실수 제곱근의 반올림에 의존하지 않는다.
# 정수 제곱근을 한 번 계산한다. 내부 비용은 정수 비트 수에 따르며 문제의 고정 정수 범위에서 보조 공간 O(1).
