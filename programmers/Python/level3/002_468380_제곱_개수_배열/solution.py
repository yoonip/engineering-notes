from bisect import bisect_right

def solution(arr, l, r):
    # 각 값 묶음의 끝 위치를 누적 저장.
    lengths = [0]
    sums = [0]
    for value in arr:
        # 값 value가 value번 등장하므로 전체 길이에 value 추가.
        lengths.append(lengths[-1] + value)
        sums.append(sums[-1] + value * value)

    def prefix(count):
        # count가 속하는 묶음을 이진 탐색.
        index = min(len(arr) - 1, bisect_right(lengths, count) - 1)
        return sums[index] + (count - lengths[index]) * arr[index]

    target = prefix(r) - prefix(l - 1)
    # 비교할 모든 구간의 길이.
    window = r - l + 1
    last_start = lengths[-1] - window
    # 시작 위치가 0인 첫 구간의 합.
    current = prefix(window)
    start = left = 0
    # 구간을 오른쪽으로 옮길 때 들어오는 원소의 묶음 번호.
    right = bisect_right(lengths, window) - 1
    answer = 0
    while start < last_start:
        # 나가는 값과 들어오는 값이 모두 일정한 이동 횟수.
        span = min(lengths[left + 1] - start, lengths[right + 1] - start - window, last_start - start)
        slope = arr[right] - arr[left]
        # 변화량 0이면 합이 계속 일정.
        if slope == 0:
            if current == target:
                # span개의 시작 위치를 한꺼번에 추가.
                answer += span
        else:
            difference = target - current
            # 정수 이동 횟수가 현재 구간 안에 있는지 and로 함께 검사.
            if difference % slope == 0 and 0 <= difference // slope < span:
                answer += 1
        current += slope * span
        # 시작점도 span만큼 이동.
        start += span
        if start == lengths[left + 1]:
            left += 1
        # 들어오는 원소도 현재 묶음 끝에 도달했는지 확인.
        if start + window == lengths[right + 1]:
            right += 1
    answer += int(current == target)
    return [target, answer]
