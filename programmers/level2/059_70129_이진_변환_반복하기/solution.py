# 문제: 이진 변환 반복하기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/70129
# 풀이: 1의 개수로 다음 문자열의 길이를 계산한다. 0을 하나씩 지우는 대신 개수만 세고 이진수로 바꾼다.
# 복잡도: 초기 길이 N: 시간 O(N), 추가 공간 O(N). 변환마다 문자열 길이가 크게 줄어든다.

def solution(s):
    conversions = removed = 0
    while s != '1':
        ones = s.count('1')
        removed += len(s) - ones
        s = bin(ones)[2:]
        conversions += 1
    return [conversions, removed]
