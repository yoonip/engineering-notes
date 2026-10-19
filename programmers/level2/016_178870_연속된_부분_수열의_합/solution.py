# 문제: 연속된 부분 수열의 합
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/178870
# 풀이: 양수 수열의 합은 오른쪽을 늘리면 증가하고 왼쪽을 옮기면 감소한다. 두 포인터로 각 원소를 한 번씩 더하고 뺀다.
# 복잡도: 수열 길이 N: 시간 O(N), 추가 공간 O(1). 양수 수열 조건을 사용한다.

def solution(sequence, k):
    left = total = 0
    answer = [0, len(sequence)]
    for right, value in enumerate(sequence):
        total += value
        while total > k:
            total -= sequence[left]
            left += 1
        if total == k and right - left < answer[1] - answer[0]:
            answer = [left, right]
    return answer
