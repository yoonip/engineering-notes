
def solution(s):
    answer = 0
    same = 0
    diff = 0
    first = ""

    for ch in s:
        if same == 0 and diff == 0:
            first = ch

        if ch == first:
            same += 1
        else:
            diff += 1

        if same == diff:
            answer += 1
            same = 0
            diff = 0

    if same > 0 or diff > 0:
        answer += 1

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(s):                         # 문자열 s를 입력받는 함수
#     answer = 0                           # 나눈 문자열의 개수를 저장
#     same = 0                             # 첫 문자와 같은 문자의 개수
#     diff = 0                             # 첫 문자와 다른 문자의 개수
#     first = ""                           # 현재 구간의 첫 문자를 저장
#
#     for ch in s:                         # 문자열 s에서 문자를 하나씩 꺼내 반복
#         if same == 0 and diff == 0:      # 새로운 구간이 시작되었다면
#             first = ch                   # 현재 문자를 새로운 구간의 기준 문자로 지정
#
#         if ch == first:                  # 현재 문자가 기준 문자와 같으면
#             same += 1                    # 같은 문자 개수를 1 증가
#         else:                            # 기준 문자와 다르면
#             diff += 1                    # 다른 문자 개수를 1 증가
#
#         if same == diff:                 # 같은 문자와 다른 문자 개수가 같아지면
#             answer += 1                  # 문자열 하나를 나누었으므로 1 증가
#             same = 0                     # 다음 구간을 위해 같은 문자 개수 초기화
#             diff = 0                     # 다음 구간을 위해 다른 문자 개수 초기화
#
#     if same > 0 or diff > 0:             # 반복 종료 후 아직 나누지 않은 문자열이 남았다면
#         answer += 1                      # 남은 문자열도 하나의 구간으로 계산
#
#     return answer                        # 나눈 문자열의 총개수 반환
