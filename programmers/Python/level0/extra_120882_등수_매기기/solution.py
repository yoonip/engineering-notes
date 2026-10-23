def solution(score):
    totals = [sum(pair) for pair in score]
    return [1 + sum(other > value for other in totals) for value in totals]

# 전체 코드 줄별 설명
# def solution(score):  # def는 함수 정의. 영어·수학 점수 쌍 리스트 입력.
#     totals = [sum(pair) for pair in score]  # 리스트 내포로 두 과목 합계 계산. 평균을 비교하는 것과 순서가 같음.
#     return [1 + sum(other > value for other in totals) for value in totals]  # 현재 합계보다 큰 학생 수를 sum으로 세고 1을 더함. 동점자는 같은 등수.

# 풀이 요약
# 자신보다 점수가 높은 학생 수+1이 등수입니다. 평균 대신 합계를 비교해도 같습니다.
# 