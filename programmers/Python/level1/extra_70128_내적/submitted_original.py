
def solution(a, b):
    answer = 0

    for x, y in zip(a, b):
        answer += x * y

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(a, b):                  # 두 정수 배열 a와 b를 입력받는 함수
#     answer = 0                       # 내적 결과를 저장할 변수를 0으로 초기화
#
#     for x, y in zip(a, b):           # zip()으로 두 배열의 같은 위치에 있는 값을 묶어 순회
#         answer += x * y              # 같은 위치의 두 숫자를 곱해서 answer에 누적
#
#     return answer                    # 계산한 내적 결과 반환
