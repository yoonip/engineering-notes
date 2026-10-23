def solution(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False
    number = 2
    while number * number <= n:
        if is_prime[number]:
            for multiple in range(number * number, n + 1, number):
                is_prime[multiple] = False
        number += 1
    return sum(is_prime)

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 1부터 n까지에 있는 소수의 개수를 반환하는 함수
#     is_prime = [True] * (n + 1)  # []는 리스트. =는 값 저장. True·False는 참·거짓. 0~n번 위치를 만들고, 우선 모두 소수 후보인 True로 표시
#     is_prime[0] = False  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. True·False는 참·거짓. 0은 소수가 아니므로 제외
#     is_prime[1] = False  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. True·False는 참·거짓. 1도 소수가 아니므로 제외
#     number = 2  # =는 값 저장. 가장 작은 소수인 2부터 확인 시작
#     while number * number <= n:  # while은 조건이 참인 동안 반복. <=는 이하 비교. number의 제곱이 n 이하인 동안 반복
#         if is_prime[number]:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 현재 숫자가 아직 제외되지 않았다면 소수이므로
#             for multiple in range(number * number, n + 1, number):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 제곱부터 n까지 배수를 확인
#                 is_prime[multiple] = False  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. True·False는 참·거짓. 현재 소수의 배수는 소수가 아니므로 제외
#         number += 1  # +=는 더하거나 연결한 값을 저장. 다음 숫자를 확인하기 위해 1 증가. number = number + 1
#     return sum(is_prime)  # return은 결과를 돌려주고 함수 종료. sum은 원소 합. True는 1, False는 0으로 더해지므로 남아 있는 소수의 개수를 반환

# 풀이 요약
# 처음에는 모두 소수 후보로 두고 0과 1을 제외한다. 아직 소수인 수의 배수들을 지우면 합성수만 제거된다. number보다 작은 인수의 배수는 이미 처리했으므로 number²부터 시작하고, number²>n이면 끝낸다.
# 입력 N: 시간 O(N log log N), 공간 O(N).
