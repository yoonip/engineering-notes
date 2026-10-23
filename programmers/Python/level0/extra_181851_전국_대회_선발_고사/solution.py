def solution(rank, attendance):
    candidates = [i for i, available in enumerate(attendance) if available]
    a, b, c = sorted(candidates, key=lambda i: rank[i])[:3]
    return 10000 * a + 100 * b + c

# 전체 코드 줄별 설명
# def solution(rank, attendance):  # def는 함수 정의. 학생별 등수와 참석 여부 입력.
#     candidates = [i for i, available in enumerate(attendance) if available]  # enumerate는 학생 번호와 참석 여부 제공. 리스트 내포로 참석 가능한 학생 번호만 선택.
#     a, b, c = sorted(candidates, key=lambda i: rank[i])[:3]  # sorted는 정렬, lambda는 이름 없는 함수. 등수가 작은 순으로 정렬해 세 학생 번호를 분해 대입.
#     return 10000 * a + 100 * b + c  # *는 곱셈, +는 덧셈. 문제에서 지정한 식으로 학생 번호 결합.

# 풀이 요약
# 참석할 수 있는 학생만 고른 뒤 등수가 작은 세 명의 번호를 사용합니다.
# 