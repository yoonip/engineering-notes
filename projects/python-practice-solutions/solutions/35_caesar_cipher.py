# 시저 암호
# 분류: 문자 코드 / 나머지 연산
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12926
# 선택 이유: 대소문자의 시작 코드에서 상대 위치를 구하고 26으로 나눈 나머지로 순환시킨다.
# 비용: 문자열 길이 L: 시간 O(L), 추가 공간 O(L). 결과는 join으로 한 번에 연결한다.

def solution(s, n):
    answer = []

    for char in s:
        if char == " ":
            answer.append(char)
        elif char.isupper():
            shifted = (ord(char) - ord("A") + n) % 26
            answer.append(chr(ord("A") + shifted))
        else:
            shifted = (ord(char) - ord("a") + n) % 26
            answer.append(chr(ord("a") + shifted))

    return "".join(answer)
