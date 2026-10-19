def solution(word):
    # 남은 자리의 모든 접미어 수 1+5+…를 자리별 가중치로 쓴다.
    weights = [781, 156, 31, 6, 1]
    answer = 0
    for index, character in enumerate(word):
        # 앞선 모음의 전체 묶음과 현재 접두 단어 하나를 건너뛴다.
        answer += 'AEIOU'.index(character) * weights[index] + 1
    return answer
