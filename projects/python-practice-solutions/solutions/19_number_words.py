# 숫자 문자열과 영단어
# 분류: 문자열 치환
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/81301
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(s):
    words = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine"
    ]

    for number, word in enumerate(words):
        s = s.replace(word, str(number))

    return int(s)


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(s):  # def로 함수를 정의합니다. s는 입력 문자열을 받는 매개변수입니다.
#     words = [  # 대괄호로 리스트를 만듭니다. 0부터 9까지의 영단어를 순서대로 저장합니다.
#         "zero", "one", "two", "three", "four",  # 리스트 인덱스는 0부터입니다. words[0]은 "zero", words[4]는 "four"입니다.
#         "five", "six", "seven", "eight", "nine"  # 쉼표로 원소를 구분합니다. 따옴표로 감싼 값은 문자열입니다.
#     ]  # 여러 줄에 걸쳐 적은 리스트의 끝입니다.
#
#     for number, word in enumerate(words):  # enumerate는 (인덱스, 원소)를 제공합니다. 두 값을 각각 number와 word에 받는 언패킹입니다.
#         s = s.replace(word, str(number))  # str로 정수를 문자열로 바꾸고, replace(기존,새값)로 일치하는 영단어를 모두 교체합니다. 결과를 s에 다시 대입합니다.
#
#     return int(s)  # int는 숫자 문자열을 정수로 변환합니다. 그 정수를 반환하고 함수를 종료합니다.
#
