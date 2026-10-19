# 문제: 문자열 압축
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/60057
# 풀이: 가능한 단위 길이마다 연속한 같은 조각의 수를 센다. 압축 문자열 전체 대신 조각 길이와 반복 횟수의 자릿수만 합한다.
# 복잡도: 길이 N: 시간 O(N²), 임시 문자열 공간 O(N).

def solution(s):
    answer = len(s)
    for size in range(1, len(s) // 2 + 1):
        previous = s[:size]
        count, length = 1, 0
        for start in range(size, len(s), size):
            current = s[start:start + size]
            if current == previous:
                count += 1
            else:
                length += len(previous) + (len(str(count)) if count > 1 else 0)
                previous, count = current, 1
        length += len(previous) + (len(str(count)) if count > 1 else 0)
        answer = min(answer, length)
    return answer
