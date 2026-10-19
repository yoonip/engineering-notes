# 문제: 가장 큰 수
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42746
# 풀이: 입력이 1000 이하인 조건에서 반복 문자열을 정렬 키로 쓴다. 이어 붙인 결과가 커지는 순서로 배치하고 전부 0이면 하나만 남긴다.
# 복잡도: 수 N개: 수가 1000 이하인 조건에서 시간 O(N log N), 추가 공간 O(N).

def solution(numbers):
    parts = list(map(str, numbers))
    parts.sort(key=lambda value: value * 4, reverse=True)
    if parts[0] == '0':
        return '0'
    return ''.join(parts)
