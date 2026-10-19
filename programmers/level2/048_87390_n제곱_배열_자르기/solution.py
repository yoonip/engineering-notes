# 문제: n제곱 배열 자르기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/87390
# 풀이: 평탄화한 인덱스를 행·열로 바꾸면 값은 max(행,열)+1이다. 필요한 반환 구간만 계산해 N² 배열 생성을 피한다.
# 복잡도: 반환 구간 길이 L: 시간 O(L), 반환 배열 외 추가 공간 O(1).

def solution(n, left, right):
    answer = []
    for index in range(left, right + 1):
        row, column = divmod(index, n)
        answer.append(max(row, column) + 1)
    return answer
