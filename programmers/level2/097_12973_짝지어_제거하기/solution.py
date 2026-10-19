# 문제: 짝지어 제거하기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/12973
# 풀이: 처리한 문자열 중 남은 문자만 스택에 둔다. 다음 문자가 스택 위와 같으면 짝을 지워 앞부분을 다시 탐색하지 않는다.
# 복잡도: 문자열 길이 N: 시간 O(N), 추가 공간 O(N).

def solution(s):
    stack = []
    for character in s:
        if stack and stack[-1] == character:
            stack.pop()
        else:
            stack.append(character)
    return int(not stack)
