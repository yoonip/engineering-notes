# 문제: n진수 게임
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/17687
# 풀이: 필요한 자릿수까지 진법 변환 결과를 이어 붙인다. 참가자 수 간격으로 본인 차례의 문자만 골라 반환한다.
# 복잡도: 필요 문자 L=t·m·최대 변환 자릿수 D: 문자열 앞붙이기 포함 시간 상한 O(LD), 추가 공간 O(L+D).

def solution(n, t, m, p):
    digits = '0123456789ABCDEF'
    stream = []
    number = 0
    while len(stream) < t * m:
        value = number
        converted = '0' if value == 0 else ''
        while value:
            value, remainder = divmod(value, n)
            converted = digits[remainder] + converted
        stream.extend(converted)
        number += 1
    return ''.join(stream[p - 1:t * m:m])
