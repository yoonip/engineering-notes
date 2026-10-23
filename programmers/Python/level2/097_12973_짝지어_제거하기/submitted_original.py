def solution(s):
    stack = []
    for character in s:
        if stack and stack[-1] == character:
            stack.pop()
        else:
            stack.append(character)
    return int(not stack)

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. s는 소문자 문자열 입력.
#     stack = []  # []는 빈 리스트. 아직 제거되지 않은 문자 스택.
#     for character in s:  # for~in으로 문자를 왼쪽부터 순회.
#         if stack and stack[-1] == character:  # and는 둘 다 참, [-1]은 마지막 문자, ==는 같음. 새 문자와 인접한 짝 검사.
#             stack.pop()  # pop은 마지막 원소 삭제. 기존 문자와 새 문자를 함께 제거한 효과.
#         else:  # else는 제거할 짝이 없는 경우.
#             stack.append(character)  # append로 새 문자를 스택 끝에 추가.
#     return int(not stack)  # not은 빈 스택이면 참. int는 참을 1·거짓을 0으로 바꿔 반환.

# 풀이 요약
# 스택에는 처리한 부분에서 제거되지 않은 문자만 남깁니다. 다음 문자가 스택 위와 같으면 짝을 지우고 아니면 넣습니다.
# 예: baabaa는 aa→bb→aa가 제거되어 빈 스택, 답 1. 시간·공간 O(N).
