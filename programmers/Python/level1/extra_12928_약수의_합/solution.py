def solution(n):
    answer = 0
    for i in range(1, n + 1):
        if n % i == 0:
            answer += i
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def는 함수를 정의하는 명령어, n은 입력받는 정수
#     answer = 0  # =는 값 저장. 약수의 합을 저장할 변수, 처음에는 0으로 초기화
#     for i in range(1, n + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. for는 반복문, i는 1부터 n까지 차례대로 증가
#         if n % i == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. if는 조건문, %는 나머지 연산, 나머지가 0이면 i는 n의 약수
#             answer += i  # +=는 더하거나 연결한 값을 저장. answer = answer + i 와 같음, 약수 i를 합계에 더함
#     return answer  # return은 결과를 돌려주고 함수 종료. return은 함수의 결과를 반환하고 함수를 종료

# 풀이 요약
# 1부터 n까지의 정수 중 n을 나눈 나머지가 0인 수만 더한다. n=0이면 range가 비어 합계의 초기값 0을 반환한다.
# 입력 N: 시간 O(N), 보조 공간 O(1).
