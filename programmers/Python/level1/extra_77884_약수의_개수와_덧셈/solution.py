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

# 전체 코드 줄별 설명
# def solution(left, right):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 두 매개변수로 검사할 구간의 양 끝값을 받습니다.
#     answer = 0  # =는 값 저장. 더하고 뺀 결과를 저장할 변수입니다.
#     for number in range(left, right + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. range는 끝값을 제외하므로 +1하여 right까지 포함합니다.
#         count = 0  # =는 값 저장. 현재 수의 약수 개수입니다. number가 바뀔 때마다 0으로 초기화합니다.
#         for divisor in range(1, number + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 1부터 현재 수까지 하나씩 나눠 봅니다.
#             if number % divisor == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. %는 나머지 연산입니다. 나머지가 0이면 divisor는 약수입니다.
#                 count += 1  # +=는 더하거나 연결한 값을 저장. count = count + 1과 같습니다. 약수 개수를 늘립니다.
#         if count % 2 == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. 약수 개수를 2로 나눈 나머지가 0이면 짝수입니다.
#             answer += number  # +=는 더하거나 연결한 값을 저장. 약수 개수가 아니라 원래 수를 결과에 더합니다.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 약수 개수가 홀수일 때 실행합니다.
#             answer -= number  # -=는 빼서 저장. answer = answer - number와 같습니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 수를 처리한 뒤 결과를 반환하고 함수를 종료합니다.

# 풀이 요약
# 각 수를 1부터 자기 자신까지 나눠 나머지가 0인 약수를 센다. 약수 개수가 짝수면 더하고 홀수면 뺀다. 이 제출본은 제곱수 판정 공식 대신 약수를 직접 세는 구현이다.
# 구간 [L,R]: 시간 상한 O((R-L+1)R), 보조 공간 O(1).
