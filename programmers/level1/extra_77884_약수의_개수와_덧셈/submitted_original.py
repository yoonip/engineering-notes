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


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(left, right):  # def로 함수를 정의합니다. 두 매개변수로 검사할 구간의 양 끝값을 받습니다.
#     answer = 0  # 더하고 뺀 결과를 저장할 변수입니다.
#
#     for number in range(left, right + 1):  # range는 끝값을 제외하므로 +1하여 right까지 포함합니다.
#         count = 0  # 현재 수의 약수 개수입니다. number가 바뀔 때마다 0으로 초기화합니다.
#
#         for divisor in range(1, number + 1):  # 1부터 현재 수까지 하나씩 나눠 봅니다.
#             if number % divisor == 0:  # %는 나머지 연산입니다. 나머지가 0이면 divisor는 약수입니다.
#                 count += 1  # count = count + 1과 같습니다. 약수 개수를 늘립니다.
#
#         if count % 2 == 0:  # 약수 개수를 2로 나눈 나머지가 0이면 짝수입니다.
#             answer += number  # 약수 개수가 아니라 원래 수를 결과에 더합니다.
#         else:  # 약수 개수가 홀수일 때 실행합니다.
#             answer -= number  # answer = answer - number와 같습니다.
#
#     return answer  # 모든 수를 처리한 뒤 결과를 반환하고 함수를 종료합니다.