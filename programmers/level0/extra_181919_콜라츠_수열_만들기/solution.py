def solution(n):
    answer = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        answer.append(n)
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 콜라츠 수열의 시작값 입력.
#     answer = [n]  # []는 리스트. 시작값부터 기록.
#     while n != 1:  # while은 조건이 참인 동안 반복, !=는 다름 비교. 1이 되면 종료.
#         n = n // 2 if n % 2 == 0 else 3 * n + 1  # %는 나머지, //는 정수 나눗셈. 조건 표현식으로 짝수·홀수 계산 선택.
#         answer.append(n)  # append는 끝에 추가. 계산 후의 수 기록.
#     return answer  # 시작값부터 마지막 1까지의 수열 반환.

# 풀이 요약
# 현재 수가 짝수면 절반, 홀수면 3배+1로 바꾸고 매번 기록합니다.
# 