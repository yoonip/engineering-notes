def solution(word):
    weights = [781, 156, 31, 6, 1]
    answer = 0
    for index, character in enumerate(word):
        answer += 'AEIOU'.index(character) * weights[index] + 1
    return answer

# 전체 코드 줄별 설명
# def solution(word):  # def는 함수 정의, word는 사전에서 찾을 단어 문자열.
#     weights = [781, 156, 31, 6, 1]  # []는 리스트. 자리별 건너뛸 단어 수: 1+5+...+5^(남은 자리 수).
#     answer = 0  # =는 대입. 사전 순위 초기화.
#     for index, character in enumerate(word):  # enumerate는 (인덱스,문자) 제공. for로 각 자리 순회.
#         answer += 'AEIOU'.index(character) * weights[index] + 1  # index는 문자 위치를 0부터 반환, []는 자리 가중치 접근. *로 앞선 모음들의 단어 수 계산, +=로 누적.
#     return answer  # return으로 1부터 시작하는 사전 순위 반환.

# 풀이 요약
# 각 자리에서 앞선 모음으로 시작하는 모든 접미 단어를 건너뛰고, 현재 접두 단어 자체의 순위 1을 더합니다.
# 예: 'I'는 앞의 A·E 그룹 781개씩을 지나 2×781+1=1563. 단어 길이 L에 대해 시간 O(L), 공간 O(1).
