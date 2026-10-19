def solution(number):
    n = len(number)
    answer = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if number[i] + number[j] + number[k] == 0:
                    answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(number):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. number는 학생 번호 리스트를 받습니다.
#     n = len(number)  # len은 길이. =는 값 저장. len()으로 학생 수를 구해 n에 저장합니다.
#     answer = 0  # =는 값 저장. 조건을 만족하는 조합의 개수를 0으로 시작합니다.
#     for i in range(n - 2):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. range(끝)은 끝을 제외합니다. 뒤에 두 명을 남기고 첫 학생을 고릅니다.
#         for j in range(i + 1, n - 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. i 다음 위치부터 고릅니다. 뒤에 한 명을 남깁니다.
#             for k in range(j + 1, n):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. j 다음 위치부터 마지막 인덱스 n-1까지 고릅니다.
#                 if number[i] + number[j] + number[k] == 0:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. [인덱스]로 값을 읽습니다. ==는 같은지 비교합니다.
#                     answer += 1  # +=는 더하거나 연결한 값을 저장. answer = answer + 1과 같습니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 반복이 끝난 뒤 개수를 반환하고 함수를 종료합니다.

# 풀이 요약
# 인덱스를 i<j<k로 골라 서로 다른 세 학생의 모든 조합을 한 번씩 확인한다. 세 수의 합이 0일 때만 센다. 순서를 바꾼 같은 세 사람을 다시 세지 않도록 각 반복의 시작값을 다음 인덱스로 둔다.
# 학생 수 N: 시간 O(N³), 보조 공간 O(1).
