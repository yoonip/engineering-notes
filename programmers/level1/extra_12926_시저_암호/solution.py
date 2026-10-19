def solution(s, n):
    answer = []
    for char in s:
        if char == ' ':
            answer.append(char)
        else:
            base = ord('A') if char.isupper() else ord('a')
            answer.append(chr((ord(char) - base + n) % 26 + base))
    return ''.join(answer)

# 전체 코드 줄별 설명
# def solution(s, n):  # def는 함수 정의. 영문·공백 문자열과 이동 거리 입력.
#     answer = []  # []는 빈 리스트. 변환한 문자 저장.
#     for char in s:  # for는 문자열의 각 문자 순회.
#         if char == ' ':  # if는 조건, ==는 값 비교. 공백은 이동하지 않음.
#             answer.append(char)  # append로 원래 공백을 결과에 추가.
#         else:  # 알파벳 문자일 때 처리.
#             base = ord('A') if char.isupper() else ord('a')  # isupper는 대문자 검사, ord는 문자 코드. 대·소문자별 기준 코드 선택.
#             answer.append(chr((ord(char) - base + n) % 26 + base))  # 기준을 빼 0~25로 바꾼 뒤 이동. %26으로 순환하고 chr로 문자 복원.
#     return ''.join(answer)  # join은 문자 리스트를 구분자 없이 연결한 문자열 반환.

# 풀이 요약
# 알파벳을 0~25 번호로 바꿔 이동하고 26으로 나눈 나머지로 순환합니다. 대소문자와 공백은 유지합니다.
# 