# 문제: 마법의 엘리베이터
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/148653
# 풀이: 낮은 자리부터 올림·내림 중 짧은 쪽을 고른다. 현재 자리가 5이면 다음 자리까지 보아 올림 여부를 결정한다.
# 복잡도: 층수 X: 시간 O(log₁₀X), 추가 공간 O(1).

def solution(storey):
    answer = 0
    while storey:
        storey, digit = divmod(storey, 10)
        if digit > 5 or (digit == 5 and storey % 10 >= 5):
            answer += 10 - digit
            storey += 1
        else:
            answer += digit
    return answer
