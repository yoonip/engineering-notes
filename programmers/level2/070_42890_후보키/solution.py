from itertools import combinations

def solution(relation):
    rows, columns = len(relation), len(relation[0])
    keys = []
    for size in range(1, columns + 1):
        for selected in combinations(range(columns), size):
            selected_set = set(selected)
            if any(key <= selected_set for key in keys):
                continue
            values = {tuple(row[column] for column in selected) for row in relation}
            if len(values) == rows:
                keys.append(selected_set)
    return len(keys)

# 전체 코드 줄별 설명
# from itertools import combinations  # itertools의 combinations를 import. 열 번호를 중복 없이 고르는 조합 생성 함수.
# 
# def solution(relation):  # def는 함수 정의. relation은 행·열로 된 문자열 표 입력.
#     rows, columns = len(relation), len(relation[0])  # len은 길이. 행 수·열 수 각각 대입.
#     keys = []  # []는 리스트. 찾은 최소 후보키의 열 집합 저장.
#     for size in range(1, columns + 1):  # range는 끝 미포함. 열을 적게 쓰는 조합부터 검사.
#         for selected in combinations(range(columns), size):  # 열 번호에서 size개를 선택한 튜플 순회.
#             selected_set = set(selected)  # set은 중복 없는 집합. 부분집합 검사에 사용.
#             if any(key <= selected_set for key in keys):  # 집합의 <=는 부분집합. any는 하나라도 참. 기존 후보키를 포함하면 최소성 위반.
#                 continue  # continue로 불필요한 조합 건너뜀.
#             values = {tuple(row[column] for column in selected) for row in relation}  # {} 집합 내포·tuple로 선택한 열의 행별 값을 묶음. 문자열 경계가 보존돼 잘못 합쳐지지 않음.
#             if len(values) == rows:  # ==는 같음. 모든 행의 묶음이 서로 다르면 유일성 만족.
#                 keys.append(selected_set)  # append로 유일성과 최소성을 만족한 후보키 저장.
#     return len(keys)  # return으로 전체 후보키 수 반환.

# 풀이 요약
# 열 개수가 작은 조합부터 검사합니다. 기존 후보키를 포함하면 제외하고, 선택 열의 값 튜플이 모든 행에서 다르면 새 후보키입니다.
# 예: 학번 단독과 이름+전공이 후보키여서 2개. 열 C·행 R·후보키 K개일 때 시간 상한 O(2^C*C*(R+K)), 공간 O(C(R+K)).
