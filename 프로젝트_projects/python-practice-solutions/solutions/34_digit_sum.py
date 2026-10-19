# 자릿수 더하기
# 분류: 형 변환 / 반복
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12931
# 선택 이유: 문자열로 바꾼 각 자릿수를 정수로 읽어 합한다.
# 비용: 자릿수 D개: 시간 O(D), 추가 공간 O(D).

def solution(n):
    answer = 0

    for digit in str(n):
        answer += int(digit)

    return answer
