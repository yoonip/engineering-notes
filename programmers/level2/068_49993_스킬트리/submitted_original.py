def solution(skill, skill_trees):
    required = set(skill)
    answer = 0
    for tree in skill_trees:
        filtered = ''.join(character for character in tree if character in required)
        if skill.startswith(filtered):
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(skill, skill_trees):  # def는 함수 정의. 선행 순서 문자열·검사할 스킬트리 목록 입력.
#     required = set(skill)  # set은 중복 없는 집합. 선행 조건이 있는 스킬들을 빠르게 찾도록 저장.
#     answer = 0  # =는 대입. 가능한 스킬트리 수 초기화.
#     for tree in skill_trees:  # for~in으로 각 스킬트리 순회.
#         filtered = ''.join(character for character in tree if character in required)  # 생성식의 if·in으로 선행 대상만 남기고 join으로 문자열 연결.
#         if skill.startswith(filtered):  # startswith는 주어진 문자열로 시작하는지 검사. 선행 순서의 접두부여야 유효.
#             answer += 1  # +=는 더해 저장. 유효한 트리 수 증가.
#     return answer  # return으로 가능한 트리 수 반환.

# 풀이 요약
# 선행 조건이 없는 스킬을 지운 뒤, 남은 순서가 skill의 앞부분과 같으면 가능합니다. 앞 스킬을 생략하고 뒤 스킬만 배울 수 없습니다.
# 예: CBD에서 CBADF→CBD, AECB→CB는 가능해 2개. 전체 문자열 길이 합 L에 대해 시간 O(L), 임시 공간 O(스킬트리 길이).
