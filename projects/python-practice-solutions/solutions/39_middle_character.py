# 가운데 글자 가져오기
# 분류: 인덱스 / 슬라이싱
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12903
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(s):
    mid = len(s) // 2
    if len(s) % 2 == 0:
        return s[mid - 1:mid + 1]
    return s[mid]


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(s):                    # 문자열 s를 입력받는 함수를 정의합니다.
#     mid = len(s) // 2              # len()은 길이, //는 정수 나눗셈입니다. 가운데 인덱스를 구합니다.
#     if len(s) % 2 == 0:            # 길이를 2로 나눈 나머지가 0이면 짝수입니다.
#         return s[mid - 1:mid + 1]  # [시작:끝]은 끝 직전까지 가져옵니다. 가운데 두 글자를 반환합니다.
#     return s[mid]                  # 홀수이면 가운데 인덱스의 한 글자를 반환합니다. 인덱스는 0부터 시작합니다.
