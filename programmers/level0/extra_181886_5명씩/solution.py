def solution(names):
    return names[::5]

# 전체 코드 줄별 설명
# def solution(names):  # def는 함수 정의. 줄 선 사람의 이름 리스트 입력.
#     return names[::5]  # [::5]는 인덱스 0부터 5칸 간격 슬라이싱. 각 5명 묶음의 첫 사람 선택.

# 풀이 요약
# 각 그룹의 첫 위치는 0, 5, 10 순서입니다. 마지막 소규모 그룹도 자동 포함됩니다.
# 