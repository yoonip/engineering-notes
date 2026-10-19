# 데이터 분석
# 분류: 필터 / 정렬
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/250121
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

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


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# # def는 함수를 정의합니다. 괄호 안의 네 이름은 전달받는 값을 담는 매개변수입니다.
# # 콜론 다음의 들여쓴 코드가 함수에 속합니다. 별도로 import할 기능은 없습니다.
# def solution(data, ext, val_ext, sort_by):
#     # {키: 값, ...}은 딕셔너리를 만드는 문법입니다.
#     # 딕셔너리는 키와 값을 연결합니다. 여기서는 문자열 열 이름을 정수 번호와 연결합니다.
#     # 리스트 인덱스는 0부터 시작하므로 code/date/maximum/remain은 0/1/2/3입니다.
#     columns = {"code": 0, "date": 1, "maximum": 2, "remain": 3}
#     # 딕셔너리[키]는 그 키에 연결된 값을 읽습니다.
#     # ext가 "date"라면 columns[ext]는 1입니다.
#     filter_index = columns[ext]
#     # sort_by가 "remain"이라면 columns[sort_by]는 3입니다.
#     # =는 오른쪽 값을 왼쪽 변수 이름에 대입하는 기호입니다.
#     sort_index = columns[sort_by]
#     # []는 빈 리스트입니다. 조건을 만족하는 행들을 여기에 추가합니다.
#     answer = []
#
#     # for는 data에서 원소를 하나씩 꺼내 row에 대입하며 반복합니다.
#     # data의 각 원소는 리스트이므로 row는 예를 들어 [1,20300104,100,80]입니다.
#     # row라는 이름은 작성자가 정한 변수 이름이며 Python 예약어가 아닙니다.
#     for row in data:
#         # row[번호]는 그 번호에 있는 값을 읽습니다.
#         # <는 '작다'입니다. 기준값과 같은 행은 포함하지 않습니다.
#         if row[filter_index] < val_ext:
#             # 리스트.append(값)는 리스트의 맨 뒤에 원소 하나를 추가합니다.
#             # row 전체가 한 원소로 추가되므로 answer는 2차원 리스트가 됩니다.
#             answer.append(row)
#
#     # 리스트.sort()는 그 리스트 자체의 순서를 정렬합니다. 기본은 오름차순입니다.
#     # key=에는 각 원소에서 비교할 값을 꺼내는 함수를 전달합니다.
#     # lambda 매개변수: 표현식은 이름을 붙이지 않고 짧은 함수를 만드는 문법입니다.
#     # lambda row: row[sort_index]는 행 하나를 받아 지정된 열의 값을 반환합니다.
#     # lambda의 row는 위 for문의 row와 별개인 이 짧은 함수의 매개변수입니다.
#     # 이 호출은 answer의 행 순서만 바꾸며 각 행 안의 값은 바꾸지 않습니다.
#     answer.sort(key=lambda row: row[sort_index])
#     # return은 결과를 전달하고 함수 전체를 종료합니다.
#     return answer
