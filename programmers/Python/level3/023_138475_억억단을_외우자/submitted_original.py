def solution(e, starts):
    divisors = [1] * (e + 1)
    for prime in range(2, e + 1):
        if divisors[prime] != 1:
            continue
        power, exponent = prime, 1
        while power <= e:
            for multiple in range(power, e + 1, power):
                divisors[multiple] = divisors[multiple] // exponent * (exponent + 1)
            power *= prime
            exponent += 1
    answer = [0] * len(starts)
    cursor = winner = e
    best_count = divisors[e]
    for index, start in sorted(enumerate(starts), key=lambda item: item[1], reverse=True):
        while cursor >= start:
            if divisors[cursor] >= best_count:
                winner = cursor
                best_count = divisors[cursor]
            cursor -= 1
        answer[index] = winner
    return answer

# 전체 코드 줄별 설명
# def solution(e, starts):  # def는 함수 정의. e는 구간의 공통 오른쪽 끝, starts는 여러 왼쪽 끝 목록.
#     divisors = [1] * (e + 1)  # [] 리스트와 * 반복. 각 정수의 약수 개수를 1로 시작.
#     for prime in range(2, e + 1):  # range는 끝 제외. 2부터 e까지 소수 후보 순회.
#         if divisors[prime] != 1:  # if는 조건문, !=는 다름. 이미 작은 소수의 배수로 처리됐다면 합성수.
#             continue  # continue는 다음 후보로 이동.
#         power, exponent = prime, 1  # 두 값을 언패킹. 현재 소수 거듭제곱과 지수.
#         while power <= e:  # while은 조건이 참인 동안 반복. prime, prime², prime³...을 순회.
#             for multiple in range(power, e + 1, power):  # 해당 거듭제곱의 모든 배수를 순회.
#                 divisors[multiple] = divisors[multiple] // exponent * (exponent + 1)  # //는 정수 나눗셈, *는 곱셈. 소수 지수가 증가하면 약수 선택 수가 exponent에서 exponent+1로 증가.
#             power *= prime  # *=는 곱해 저장. 다음 거듭제곱으로 이동.
#             exponent += 1  # +=는 더해 저장. 지수 증가.
#     answer = [0] * len(starts)  # len은 질의 수. 원래 순서대로 답을 보관할 리스트.
#     cursor = winner = e  # 연쇄 대입. 오른쪽부터 스캔할 위치와 현재 최적 정수 초기화.
#     best_count = divisors[e]  # 현재 구간에서 가장 많은 약수 개수.
#     for index, start in sorted(enumerate(starts), key=lambda item: item[1], reverse=True):  # enumerate는 원래 번호·값, sorted는 정렬, lambda는 짧은 기준 함수. 큰 시작점부터 처리.
#         while cursor >= start:  # 이전에 처리하지 않은 왼쪽 부분만 추가로 스캔.
#             if divisors[cursor] >= best_count:  # >=는 이상. 개수가 같아도 더 작은 정수인 현재 cursor로 바꿔 동률 우선순위 처리.
#                 winner = cursor  # =는 대입. 최적 정수 갱신.
#                 best_count = divisors[cursor]  # 최고 등장 횟수 갱신.
#             cursor -= 1  # -=는 빼서 저장. 다음으로 작은 정수 확인.
#         answer[index] = winner  # [인덱스]에 저장해 정렬 전 질의 순서 복원.
#     return answer  # 각 구간의 답 목록 반환.

# 풀이 요약
# 정수 x가 곱셈표에 나오는 횟수는 x의 약수 개수입니다. 소인수 지수가 a일 때 약수 선택 수 a+1을 곱하는 체로 개수를 구합니다.
# 시작점을 내림차순으로 처리하면 오른쪽부터 구간을 늘리며 한 번만 스캔할 수 있습니다. 같은 약수 개수면 더 작은 수로 갱신합니다. 시간 O(E log log E+Q log Q), 공간 O(E+Q).
# 예: 1~8에서 6과 8의 약수는 네 개로 최다입니다. [1,8]·[3,8]은 작은 수 6, [7,8]은 8이 답입니다.
# 