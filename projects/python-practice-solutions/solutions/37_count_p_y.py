# 문자열 내 p와 y의 개수
# 분류: 대소문자 정규화 / 개수 집계
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12916
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(s):
    s = s.lower()
    return s.count("p") == s.count("y")


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(s):                          # 문자열 s를 입력받는 함수를 정의합니다.
#     s = s.lower()                        # 대소문자를 구분하지 않도록 모두 소문자로 바꿉니다.
#     return s.count("p") == s.count("y")  # count는 개수를 셉니다. ==는 같으면 True, 다르면 False입니다.
