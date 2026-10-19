
def solution(numbers):
    answer = 45 - sum(numbers)

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(numbers):                    # 0~9 중 일부 숫자가 담긴 리스트를 입력받음
#     answer = 45 - sum(numbers)            # 0부터 9까지의 합 45에서 리스트에 존재하는 숫자의 합을 뺌
#
#     return answer                         # 리스트에 없는 숫자들의 합을 반환
