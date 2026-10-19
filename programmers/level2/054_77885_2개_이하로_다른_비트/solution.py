# 문제: 2개 이하로 다른 비트
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/77885
# 풀이: 오른쪽 첫 0 비트를 찾아 가장 작은 증가량을 계산한다. 홀수는 그 바로 아래 1도 바꿔 달라진 비트를 두 개로 제한한다.
# 복잡도: 수 N개: 제한 범위 정수 연산 기준 시간 O(N), 반환 배열 외 추가 공간 O(1).

def solution(numbers):
    answer = []
    for number in numbers:
        zero = (~number) & (number + 1)
        answer.append(number + zero - (zero >> 1))
    return answer
