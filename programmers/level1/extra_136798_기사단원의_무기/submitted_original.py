
def solution(number, limit, power):
    counts = [0] * (number + 1)

    for i in range(1, number + 1):
        for j in range(i, number + 1, i):
            counts[j] += 1

    answer = 0

    for i in range(1, number + 1):
        if counts[i] > limit:
            answer += power
        else:
            answer += counts[i]

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(number, limit, power):             # 기사단원 수, 공격력 제한, 대체 공격력을 입력받음
#     counts = [0] * (number + 1)                 # 각 숫자의 약수 개수를 저장할 리스트 생성 (0으로 초기화)
#
#     for i in range(1, number + 1):             # 1부터 number까지 모든 숫자 i를 확인
#         for j in range(i, number + 1, i):      # i의 배수들을 i 간격으로 순회 (range의 세 번째 값은 증가 간격)
#             counts[j] += 1                     # i는 j의 약수이므로 j의 약수 개수를 1 증가
#
#     answer = 0                                 # 필요한 철의 총무게를 0으로 초기화
#
#     for i in range(1, number + 1):             # 각 기사단원의 번호를 1부터 순회
#         if counts[i] > limit:                  # 약수 개수가 공격력 제한을 초과하면
#             answer += power                    # 지정된 대체 공격력을 더함
#         else:                                  # 공격력 제한 이하라면
#             answer += counts[i]                # 실제 약수 개수를 더함
#
#     return answer                              # 필요한 철의 총무게 반환
