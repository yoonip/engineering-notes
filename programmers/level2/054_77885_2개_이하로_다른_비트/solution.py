def solution(numbers):
    answer = []
    for number in numbers:
        zero = (~number) & (number + 1)
        answer.append(number + zero - (zero >> 1))
    return answer

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의, numbers는 정수 목록 입력.
#     answer = []  # []는 빈 리스트. 각 수의 다음 조건 만족 수 저장.
#     for number in numbers:  # for~in으로 입력 순서대로 정수 순회.
#         zero = (~number) & (number + 1)  # ~는 비트 반전, &는 비트 AND. 오른쪽에서 처음인 0비트의 자릿값을 추출.
#         answer.append(number + zero - (zero >> 1))  # >>1은 오른쪽 한 비트 이동(양수의 절반). 그 0을 1로, 바로 아래 1을 0으로 바꾼 값을 append로 추가.
#     return answer  # return으로 결과 목록 반환. zero=1인 짝수는 아래 자리가 없어 단순히 +1.

# 풀이 요약
# 짝수는 마지막 0을 1로 바꾸면 됩니다. 홀수는 오른쪽 첫 0을 1로, 바로 아래 1을 0으로 바꾸면 가장 작은 증가량입니다.
# 예: 7(111)→11(1011), 바뀐 비트는 두 개. 제한 내 정수 연산 기준 시간·결과 공간 O(N).
