def solution(s):
    length = len(s)
    return s[(length - 1) // 2:length // 2 + 1]

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 가운데를 구할 문자열 입력.
#     length = len(s)  # len은 문자 개수. 전체 길이 저장.
#     return s[(length - 1) // 2:length // 2 + 1]  # //는 정수 나눗셈. 홀수 길이는 가운데 한 글자, 짝수 길이는 가운데 두 글자가 되는 슬라이싱 범위.

# 풀이 요약
# 시작을 (길이-1)//2, 끝을 길이//2+1로 잡으면 홀수·짝수를 같은 식으로 처리합니다.
# 