# 문제: 구명보트
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42885
# 풀이: 정렬 후 가장 무거운 사람을 가장 가벼운 사람과 짝지을 수 있는지 본다. 못 태우면 다른 누구와도 함께 탈 수 없다.
# 복잡도: 사람 N명: 시간 O(N log N), 정렬 추가 공간 O(N). 입력을 정렬한다.

def solution(people, limit):
    people.sort()
    left, right = 0, len(people) - 1
    answer = 0
    while left <= right:
        if left < right and people[left] + people[right] <= limit:
            left += 1
        right -= 1
        answer += 1
    return answer
