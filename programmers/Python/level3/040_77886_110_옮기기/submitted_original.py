def solution(s):
    answer = []
    for word in s:
        stack = []
        count = 0
        for char in word:
            stack.append(char)
            if len(stack) >= 3 and stack[-3:] == ['1', '1', '0']:
                del stack[-3:]
                count += 1
        remaining = ''.join(stack)
        index = remaining.rfind('0') + 1
        answer.append(remaining[:index] + '110' * count + remaining[index:])
    return answer

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. s는 0과 1 문자열들의 리스트.
#     answer = []  # []는 빈 리스트. 각 문자열의 최종 결과를 저장.
#     for word in s:  # for로 문자열을 하나씩 순회.
#         stack = []  # 마지막에 넣은 문자를 먼저 꺼내는 스택을 리스트로 구현.
#         count = 0  # 추출한 110의 개수.
#         for char in word:  # 문자열의 글자를 왼쪽부터 하나씩 읽음.
#             stack.append(char)  # append는 리스트 끝에 추가.
#             if len(stack) >= 3 and stack[-3:] == ['1', '1', '0']:  # len은 길이, and는 모두 참, [-3:]는 끝 세 글자, ==는 같음.
#                 del stack[-3:]  # del은 삭제. 끝의 110을 제거하면 새로 이어진 부분도 이후에 확인 가능.
#                 count += 1  # +=는 더해 저장. 추출 개수 증가.
#         remaining = ''.join(stack)  # join은 글자 목록을 구분자 없이 이어 문자열로 만듦.
#         index = remaining.rfind('0') + 1  # rfind는 마지막 0의 위치, 없으면 -1. 마지막 0 바로 뒤를 삽입 위치로 선택.
#         answer.append(remaining[:index] + '110' * count + remaining[index:])  # [:index]와 [index:]는 문자열 자르기, *는 반복. 추출한 110을 한곳에 삽입.
#     return answer  # return은 결과 반환.

# 풀이 요약
# 스택으로 110을 모두 추출한 뒤 남은 문자열의 마지막 0 바로 뒤, 즉 끝에 연속한 1들 앞에 몰아넣는다.
# 예: 1110에서 110을 빼면 1. 남은 0이 없으므로 맨 앞에 110을 넣어 1101이 된다.
# 남은 0은 앞에 유지하고 110은 끝의 1보다 앞에 둬야 사전순으로 작아진다. 시간·공간 O(전체 글자 수).
# 