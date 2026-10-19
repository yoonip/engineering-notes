
def solution(t, p):
    answer = 0
    n = len(p)

    for i in range(len(t) - n + 1):
        num = int(t[i:i+n])

        if num <= int(p):
            answer += 1

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(t, p):                    # 문자열 t와 비교할 숫자 문자열 p를 입력받음
#     answer = 0                        # 조건을 만족하는 부분 문자열의 개수를 저장
#     n = len(p)                        # p의 문자열 길이를 구함
#
#     for i in range(len(t) - n + 1):   # t에서 길이가 n인 부분 문자열을 추출할 시작 위치 반복
#         num = int(t[i:i+n])           # t[i:i+n]으로 n글자를 추출하고 int()로 정수 변환
#
#         if num <= int(p):             # 추출한 숫자가 p보다 작거나 같으면
#             answer += 1               # 조건을 만족하므로 개수를 1 증가
#
#     return answer                     # 조건을 만족한 부분 문자열의 총개수 반환
