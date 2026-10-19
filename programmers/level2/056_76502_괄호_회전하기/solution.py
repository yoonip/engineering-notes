# 문제: 괄호 회전하기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/76502
# 풀이: 각 회전을 스택으로 검사한다. 닫는 괄호가 가장 최근 여는 괄호와 맞는지 확인하고 마지막에 스택이 비어야 한다.
# 복잡도: 문자열 길이 N: 시간 O(N²), 추가 공간 O(N).

def solution(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    answer = 0
    for offset in range(len(s)):
        stack = []
        for character in s[offset:] + s[:offset]:
            if character in '([{':
                stack.append(character)
            elif not stack or stack.pop() != pairs[character]:
                break
        else:
            if not stack:
                answer += 1
    return answer
