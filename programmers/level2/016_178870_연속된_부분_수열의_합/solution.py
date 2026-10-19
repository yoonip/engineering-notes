def solution(sequence, k):
    left = total = 0
    answer = [0, len(sequence)]
    for right, value in enumerate(sequence):
        total += value
        # 양수 수열이므로 왼쪽을 빼야 큰 합을 줄일 수 있다.
        while total > k:
            total -= sequence[left]
            left += 1
        # 길이가 더 짧을 때만 바꿔 같은 길이의 앞선 시작점을 보존한다.
        if total == k and right - left < answer[1] - answer[0]:
            answer = [left, right]
    return answer
