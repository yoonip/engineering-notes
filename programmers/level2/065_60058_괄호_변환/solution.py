# 문제: 괄호 변환
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/60058
# 풀이: 가장 짧은 균형 접두부를 분리한다. 올바른 접두부는 유지하고 잘못된 접두부는 문제의 변환 규칙에 따라 뒤집는다.
# 복잡도: 길이 N: 문자열 복사·연결을 포함한 시간·추가 공간 상한 O(N²), 재귀 깊이 O(N).

def solution(p):
    if not p:
        return ''
    balance = 0
    correct = True
    for index, character in enumerate(p, 1):
        balance += 1 if character == '(' else -1
        if balance < 0:
            correct = False
        if balance == 0:
            u, v = p[:index], p[index:]
            if correct:
                return u + solution(v)
            flipped = ''.join(')' if ch == '(' else '(' for ch in u[1:-1])
            return '(' + solution(v) + ')' + flipped
