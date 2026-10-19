# 음양 더하기
# 분류: 반복 / 조건
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/76501
# 선택 이유: 절댓값과 부호를 함께 순회해 부호를 적용한 값을 누적한다.
# 비용: 원소 N개: 시간 O(N), 추가 공간 O(1).

def solution(absolutes, signs):
    answer = 0

    for number, positive in zip(absolutes, signs):
        if positive:
            answer += number
        else:
            answer -= number

    return answer
