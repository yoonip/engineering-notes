# 삼총사
# 분류: 완전탐색 / 조합
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/131705
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(number):
    n = len(number)
    answer = 0

    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if number[i] + number[j] + number[k] == 0:
                    answer += 1

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(number):  # def는 함수를 정의합니다. number는 학생 번호 리스트를 받는 매개변수입니다.
#     n = len(number)  # len은 리스트 원소 수입니다. =로 학생 수를 n에 저장합니다.
#     answer = 0  # 합이 0인 조합의 개수를 0으로 시작합니다.
#
#     for i in range(n - 2):  # range(끝)은 0부터 끝-1까지입니다. 뒤에 두 명을 남기고 첫 학생을 고릅니다.
#         for j in range(i + 1, n - 1):  # range(시작,끝)은 끝을 제외합니다. i 다음부터 고르고 뒤에 한 명을 남깁니다.
#             for k in range(j + 1, n):  # j 다음부터 마지막 인덱스 n-1까지 고릅니다. 항상 i < j < k가 됩니다.
#                 if number[i] + number[j] + number[k] == 0:  # 리스트[인덱스]로 값을 읽고 더합니다. ==는 두 값이 같은지 비교합니다.
#                     answer += 1  # answer = answer + 1과 같습니다. 조건을 만족하면 개수를 늘립니다.
#
#     return answer  # 세 반복문 바깥에서 최종 개수를 반환하고 함수를 종료합니다.
#
