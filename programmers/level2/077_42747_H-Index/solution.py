# 문제: H-Index
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42747
# 풀이: 인용 수를 내림차순으로 정렬한다. H번째 값이 H 이상인 마지막 위치를 찾아 모든 H 후보를 다시 세지 않는다.
# 복잡도: 논문 N편: 시간 O(N log N), 정렬 추가 공간 O(N). 입력을 정렬한다.

def solution(citations):
    citations.sort(reverse=True)
    answer = 0
    for count, cited in enumerate(citations, 1):
        if cited < count:
            break
        answer = count
    return answer
