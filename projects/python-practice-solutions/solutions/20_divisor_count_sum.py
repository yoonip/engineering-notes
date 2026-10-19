# 약수의 개수와 덧셈
# 분류: 약수 완전탐색
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/77884
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(left, right):
    answer = 0

    for number in range(left, right + 1):
        count = 0

        for divisor in range(1, number + 1):
            if number % divisor == 0:
                count += 1

        if count % 2 == 0:
            answer += number
        else:
            answer -= number

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(left, right):  # def로 함수를 정의합니다. left와 right는 검사 구간의 양 끝값을 받습니다.
#     answer = 0  # =는 대입입니다. 더하고 뺀 결과를 0으로 시작합니다.
#
#     for number in range(left, right + 1):  # range는 끝값을 제외하므로 +1하여 right까지 포함합니다.
#         count = 0  # 현재 number의 약수 개수입니다. 수가 바뀔 때마다 0으로 다시 시작합니다.
#
#         for divisor in range(1, number + 1):  # 1부터 number까지 차례로 나눠 봅니다. divisor는 나누는 수를 담는 변수입니다.
#             if number % divisor == 0:  # %는 나머지, ==는 같은지 비교입니다. 나머지가 0이면 divisor는 number의 약수입니다.
#                 count += 1  # count = count + 1과 같습니다. 약수를 하나 발견했으므로 개수를 늘립니다.
#
#         if count % 2 == 0:  # 약수 개수를 2로 나눈 나머지가 0이면 약수 개수가 짝수입니다.
#             answer += number  # answer = answer + number와 같습니다. 약수 개수가 아니라 원래 수를 더합니다.
#         else:  # 위 조건이 거짓, 즉 약수 개수가 홀수이면 실행합니다.
#             answer -= number  # answer = answer - number와 같습니다. 원래 수를 뺍니다.
#
#     return answer  # 바깥 반복문까지 모두 끝낸 뒤 최종 결과를 반환하고 함수를 종료합니다.
#
