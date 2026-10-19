# 문제: 테이블 해시 함수
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/147354
# 풀이: 지정 열 오름차순·기본키 내림차순으로 정렬한다. 필요한 행들의 나머지 합만 계산해 XOR로 누적한다.
# 복잡도: 행 N·열 M: 시간 O(N log N+NM), 정렬 추가 공간 O(N). 입력을 정렬한다.

def solution(data, col, row_begin, row_end):
    data.sort(key=lambda row: (row[col - 1], -row[0]))
    answer = 0
    for index in range(row_begin, row_end + 1):
        value = sum(number % index for number in data[index - 1])
        answer ^= value
    return answer
