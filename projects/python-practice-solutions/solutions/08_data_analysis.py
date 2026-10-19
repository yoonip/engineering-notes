# 데이터 분석
# 분류: 필터 / 정렬
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/250121
# 선택 이유: 필요한 행부터 거른 뒤 한 번만 정렬한다. 전체 데이터를 정렬하는 비용을 줄인다.
# 비용: 입력 N행, 조건을 통과한 K행: 시간 O(N+K log K), 추가 공간 O(K).

def solution(data, ext, val_ext, sort_by):
    columns = {"code": 0, "date": 1, "maximum": 2, "remain": 3}
    filter_index = columns[ext]
    sort_index = columns[sort_by]
    answer = []

    for row in data:
        if row[filter_index] < val_ext:
            answer.append(row)

    answer.sort(key=lambda row: row[sort_index])
    return answer
