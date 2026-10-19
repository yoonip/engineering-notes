# 성격 유형 검사하기
# 분류: 해시 / 집계
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/118666
# 선택 이유: 유형별 점수를 집계한 뒤 각 쌍의 우세한 유형을 고른다. 동점은 사전순으로 처리한다.
# 비용: 질문 N개, 유형 수 고정: 평균 시간 O(N), 추가 공간 O(1).

def solution(survey, choices):
    points = {char: 0 for char in "RTCFJMAN"}

    for pair, choice in zip(survey, choices):
        if choice < 4:
            points[pair[0]] += 4 - choice
        elif choice > 4:
            points[pair[1]] += choice - 4

    answer = ""

    for first, second in ["RT", "CF", "JM", "AN"]:
        if points[first] >= points[second]:
            answer += first
        else:
            answer += second

    return answer
