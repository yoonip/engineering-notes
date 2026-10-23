def solution(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    answer = 0
    for offset in range(len(s)):
        stack = []
        for character in s[offset:] + s[:offset]:
            if character in '([{':
                stack.append(character)
            elif not stack or stack.pop() != pairs[character]:
                break
        else:
            if not stack:
                answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, s는 괄호 문자열 입력.
#     pairs = {')': '(', ']': '[', '}': '{'}  # {}는 딕셔너리. 닫는 괄호를 맞는 여는 괄호에 연결. 따옴표 속 괄호는 문자 데이터.
#     answer = 0  # =는 대입. 올바른 회전 수 초기화.
#     for offset in range(len(s)):  # len은 길이, range는 0~길이-1. 가능한 모든 회전량 순회.
#         stack = []  # []는 스택용 빈 리스트. 아직 닫히지 않은 여는 괄호 저장.
#         for character in s[offset:] + s[:offset]:  # 슬라이스 [시작:끝]과 + 연결로 왼쪽 회전한 문자열 구성.
#             if character in '([{':  # in은 포함 검사. 여는 괄호인지 확인.
#                 stack.append(character)  # append로 여는 괄호를 스택 끝에 추가.
#             elif not stack or stack.pop() != pairs[character]:  # not은 반전, or는 하나 이상 참, pop은 마지막 제거. 빈 스택 또는 종류 불일치 검사.
#                 break  # break로 현재 회전의 검사 중단.
#         else:  # for의 else는 break 없이 모든 문자를 검사했을 때 실행.
#             if not stack:  # 남은 여는 괄호도 없어야 올바른 문자열.
#                 answer += 1  # +=는 더해 저장. 유효 회전 수 증가.
#     return answer  # return으로 올바른 문자열을 만드는 회전 수 반환.

# 풀이 요약
# 각 회전을 스택으로 검사합니다. 닫는 괄호는 가장 최근 여는 괄호와 종류가 맞아야 하며 끝에 스택이 비어야 합니다.
# 예: '[](){}'는 0·2·4칸 회전이 유효해 3. 길이 N일 때 시간 O(N²), 공간 O(N).
