# 나머지가 1이 되는 수 찾기
# 분류: 선형 탐색
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/87389
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(n):
    for x in range(2, n):
        if n % x == 1:
            return x


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(n):  # def로 함수를 정의합니다. n은 채점기가 전달하는 정수를 받는 매개변수입니다.
#     for x in range(2, n):  # range(시작,끝)은 끝을 제외합니다. x에 2부터 n-1까지 차례로 대입하며 반복합니다.
#         if n % x == 1:  # %는 나머지 연산입니다. ==는 같은지 비교하므로 나머지가 1인지 검사합니다.
#             return x  # x를 반환하고 함수 전체를 즉시 종료합니다. 작은 순서로 검사했으므로 첫 발견이 최솟값입니다.
#
