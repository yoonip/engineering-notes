def solution(s):
    words = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine"
    ]

    for number, word in enumerate(words):
        s = s.replace(word, str(number))

    return int(s)


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(s):  # def로 함수를 정의합니다. s는 입력 문자열을 받습니다.
#     words = [  # 대괄호로 리스트를 만듭니다. 숫자 순서대로 영단어를 저장합니다.
#         "zero", "one", "two", "three", "four",  # 인덱스는 0부터입니다. words[0]은 "zero"입니다.
#         "five", "six", "seven", "eight", "nine"  # 쉼표로 원소를 구분합니다. 따옴표 안의 값은 문자열입니다.
#     ]  # 리스트의 끝입니다.
#
#     for number, word in enumerate(words):  # enumerate는 인덱스와 원소를 함께 제공합니다. 예: number=1, word="one".
#         s = s.replace(word, str(number))  # str()로 숫자를 문자열로 바꿉니다. replace(기존, 새값)는 일치하는 부분을 모두 교체합니다.
#
#     return int(s)  # int()로 숫자 문자열을 정수로 바꾸어 반환하고 함수를 종료합니다.