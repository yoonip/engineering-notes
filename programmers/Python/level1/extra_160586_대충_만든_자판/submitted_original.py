
def solution(keymap, targets):
    min_press = {}

    for keys in keymap:
        for i, ch in enumerate(keys):
            count = i + 1

            if ch not in min_press or count < min_press[ch]:
                min_press[ch] = count

    answer = []

    for target in targets:
        total = 0

        for ch in target:
            if ch not in min_press:
                total = -1
                break

            total += min_press[ch]

        answer.append(total)

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(keymap, targets):                  # 함수 정의, 자판 배열과 목표 문자열 배열을 입력받음
#     min_press = {}                              # 각 문자의 최소 입력 횟수를 저장할 딕셔너리 생성
#
#     for keys in keymap:                        # 여러 자판 중 하나를 꺼내 반복
#         for i, ch in enumerate(keys):          # 자판의 문자와 인덱스를 함께 가져옴
#             count = i + 1                      # 인덱스는 0부터 시작하므로 1을 더해 입력 횟수 계산
#
#             if ch not in min_press or count < min_press[ch]:  # 처음 등장하거나 기존보다 적은 횟수라면
#                 min_press[ch] = count          # 해당 문자의 최소 입력 횟수를 갱신
#
#     answer = []                                # 각 목표 문자열의 결과를 저장할 리스트
#
#     for target in targets:                     # 목표 문자열을 하나씩 확인
#         total = 0                              # 현재 목표 문자열의 총 입력 횟수를 0으로 초기화
#
#         for ch in target:                      # 목표 문자열의 문자를 하나씩 확인
#             if ch not in min_press:            # 자판에 존재하지 않는 문자라면
#                 total = -1                     # 입력할 수 없으므로 -1 저장
#                 break                          # 현재 목표 문자열에 대한 반복문 종료
#
#             total += min_press[ch]             # 해당 문자의 최소 입력 횟수를 총합에 더함
#
#         answer.append(total)                   # 현재 목표 문자열의 결과를 리스트에 추가
#
#     return answer                              # 모든 목표 문자열의 결과 반환
