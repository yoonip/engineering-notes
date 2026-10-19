def solution(people, limit):
    # sort는 리스트를 제자리 오름차순 정렬.
    people.sort()
    left, right = 0, len(people) - 1
    answer = 0
    # 남은 사람이 있는 동안 진행.
    while left <= right:
        if left < right and people[left] + people[right] <= limit:
            left += 1
        right -= 1
        answer += 1
    return answer
