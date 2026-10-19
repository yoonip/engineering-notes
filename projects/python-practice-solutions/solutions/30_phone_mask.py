# 핸드폰 번호 가리기
# 분류: 문자열 슬라이싱
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12948
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(phone_number):
    return "*" * (len(phone_number) - 4) + phone_number[-4:]


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(phone_number):  # def로 함수를 정의합니다. phone_number는 전화번호 문자열을 받는 매개변수입니다.
#     return "*" * (len(phone_number) - 4) + phone_number[-4:]  # len()은 길이, 문자열 * 정수는 반복, +는 문자열 연결, [-4:]는 뒤 네 글자의 슬라이싱입니다. 결과를 반환합니다.
#
