# 자릿수 더하기
# 분류: 형 변환 / 반복
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12931
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(n):
    answer = 0

    for digit in str(n):
        answer += int(digit)

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(n):  # def로 함수를 정의합니다. n은 입력 자연수를 받는 매개변수입니다.
#     answer = 0  # =는 대입입니다. 자릿수 합을 0으로 시작합니다.
#
#     for digit in str(n):  # str()로 정수를 문자열로 바꿉니다. for로 그 문자열에서 글자를 하나씩 꺼냅니다.
#         answer += int(digit)  # int()로 숫자 글자를 정수로 바꾸어 더합니다. +=는 더한 값을 다시 저장합니다.
#
#     return answer  # 반복문이 끝나면 자릿수 합을 반환하고 함수를 종료합니다.
#
