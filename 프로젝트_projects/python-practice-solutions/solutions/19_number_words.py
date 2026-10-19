# 숫자 문자열과 영단어
# 분류: 문자열 치환
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/81301
# 선택 이유: 숫자 단어는 열 개로 고정되어 있어 각 단어를 치환하는 방식이 간단하다.
# 비용: 문자열 길이 L: 시간 O(L), 추가 공간 O(L). 치환은 고정된 10회다.

def solution(s):
    words = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine"
    ]

    for number, word in enumerate(words):
        s = s.replace(word, str(number))

    return int(s)
