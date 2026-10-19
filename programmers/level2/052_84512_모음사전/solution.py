# 문제: 모음사전
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/84512
# 풀이: 각 자리의 앞선 모음이 차지하는 단어 수를 미리 계산한 가중치로 더한다. 사전 전체를 생성하지 않고 순위를 구한다.
# 복잡도: 단어 길이 L≤5: 시간 O(L), 추가 공간 O(1).

def solution(word):
    weights = [781, 156, 31, 6, 1]
    answer = 0
    for index, character in enumerate(word):
        answer += 'AEIOU'.index(character) * weights[index] + 1
    return answer
