# 문자열 내 마음대로 정렬하기
# 분류: 튜플 정렬 키
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12915
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(strings, n):
    return sorted(strings, key=lambda word: (word[n], word))


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(strings, n):  # def로 함수를 정의합니다. 문자열 리스트와 기준 인덱스를 매개변수로 받습니다.
#     return sorted(strings, key=lambda word: (word[n], word))  # sorted()는 정렬된 새 리스트를 만듭니다. key=에 비교 기준을 구하는 함수를 전달하고 결과 리스트를 반환합니다.
#
