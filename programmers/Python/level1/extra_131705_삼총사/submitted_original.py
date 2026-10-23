def solution(number):
    n = len(number)
    answer = 0

    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if number[i] + number[j] + number[k] == 0:
                    answer += 1

    return answer


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(number):  # def로 함수를 정의합니다. number는 학생 번호 리스트를 받습니다.
#     n = len(number)  # len()으로 학생 수를 구해 n에 저장합니다.
#     answer = 0  # 조건을 만족하는 조합의 개수를 0으로 시작합니다.
#
#     for i in range(n - 2):  # range(끝)은 끝을 제외합니다. 뒤에 두 명을 남기고 첫 학생을 고릅니다.
#         for j in range(i + 1, n - 1):  # i 다음 위치부터 고릅니다. 뒤에 한 명을 남깁니다.
#             for k in range(j + 1, n):  # j 다음 위치부터 마지막 인덱스 n-1까지 고릅니다.
#                 if number[i] + number[j] + number[k] == 0:  # [인덱스]로 값을 읽습니다. ==는 같은지 비교합니다.
#                     answer += 1  # answer = answer + 1과 같습니다.
#
#     return answer  # 모든 반복이 끝난 뒤 개수를 반환하고 함수를 종료합니다.