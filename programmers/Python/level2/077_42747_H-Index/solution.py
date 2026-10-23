def solution(citations):
    # 많이 인용된 논문부터 배치.
    citations.sort(reverse=True)
    answer = 0
    for count, cited in enumerate(citations, 1):
        # 이 논문까지 count편이 count회 이상 인용되는지 검사.
        if cited < count:
            break
        answer = count
    return answer
