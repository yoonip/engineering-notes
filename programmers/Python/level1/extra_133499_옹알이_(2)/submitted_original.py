
def solution(babbling):
    words = ["aya", "ye", "woo", "ma"]
    answer = 0

    for sound in babbling:
        i = 0
        prev = ""
        valid = True

        while i < len(sound):
            matched = False

            for word in words:
                if sound.startswith(word, i) and word != prev:
                    prev = word
                    i += len(word)
                    matched = True
                    break

            if not matched:
                valid = False
                break

        if valid:
            answer += 1

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(babbling):                               # 옹알이 문자열들이 담긴 리스트를 입력받음
#     words = ["aya", "ye", "woo", "ma"]                 # 발음할 수 있는 네 가지 단어
#     answer = 0                                       # 발음 가능한 문자열의 개수
#
#     for sound in babbling:                           # 옹알이 문자열을 하나씩 확인
#         i = 0                                        # 현재 검사할 문자의 인덱스를 0으로 초기화
#         prev = ""                                    # 직전에 사용한 발음을 저장
#         valid = True                                 # 현재 문자열이 발음 가능한지 표시
#
#         while i < len(sound):                        # 문자열 끝에 도달할 때까지 반복
#             matched = False                          # 현재 위치에서 발음을 찾았는지 표시
#
#             for word in words:                       # 가능한 네 가지 발음을 하나씩 확인
#                 if sound.startswith(word, i) and word != prev:  # 현재 위치에서 단어가 시작하고 직전 발음과 다르면
#                     prev = word                      # 현재 발음을 직전 발음으로 저장
#                     i += len(word)                   # 발음한 단어의 길이만큼 인덱스 이동
#                     matched = True                   # 발음 가능한 단어를 찾았다고 표시
#                     break                            # 발음을 찾았으므로 for 반복문 종료
#
#             if not matched:                          # 현재 위치에서 가능한 발음을 찾지 못했다면
#                 valid = False                        # 발음할 수 없는 문자열로 표시
#                 break                                # while 반복문 종료
#
#         if valid:                                    # 문자열 전체를 올바르게 발음할 수 있다면
#             answer += 1                              # 발음 가능한 문자열 개수를 1 증가
#
#     return answer                                    # 발음 가능한 문자열의 총개수 반환
