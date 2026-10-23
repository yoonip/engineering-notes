
def solution(a, b, n):
    answer = 0

    while n >= a:
        exchanged = (n // a) * b
        n = (n % a) + exchanged
        answer += exchanged

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(a, b, n):                    # a: 교환에 필요한 빈 병 수, b: 받는 콜라 수, n: 현재 빈 병 수
#     answer = 0                           # 교환으로 받은 콜라의 총개수를 저장
#
#     while n >= a:                        # 빈 병이 a개 이상이면 계속 교환
#         exchanged = (n // a) * b         # 교환 가능한 횟수에 b를 곱해 새로 받는 콜라 수 계산
#         n = (n % a) + exchanged          # 교환하고 남은 빈 병 + 새로 받은 콜라를 마신 뒤 생긴 빈 병
#         answer += exchanged              # 이번에 받은 콜라 수를 총합에 추가
#
#     return answer                        # 교환으로 받은 콜라의 총개수 반환
