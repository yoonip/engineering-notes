# 다트 게임
# 분류: 문자열 파싱
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/17682
# 선택 이유: 문자를 한 번 순회하며 숫자·보너스·옵션을 처리한다. *는 직전 두 점수에 적용한다.
# 비용: 세 번의 점수 입력은 길이가 제한되어 시간·공간 O(1). 일반화하면 입력 길이에 비례한다.

def solution(dartResult):
    scores = []
    number = 0
    powers = {"S": 1, "D": 2, "T": 3}

    for char in dartResult:
        if char.isdigit():
            number = number * 10 + int(char)
        elif char in powers:
            scores.append(number ** powers[char])
            number = 0
        elif char == "*":
            scores[-1] *= 2
            if len(scores) >= 2:
                scores[-2] *= 2
        elif char == "#":
            scores[-1] *= -1

    return sum(scores)
