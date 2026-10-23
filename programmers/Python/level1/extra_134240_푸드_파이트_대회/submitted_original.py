
def solution(food):
    left = ""

    for i in range(1, len(food)):
        count = food[i] // 2
        left += str(i) * count

    answer = left + "0" + left[::-1]

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(food):                       # 음식 종류별 개수가 담긴 리스트를 입력받음
#     left = ""                             # 왼쪽 선수의 음식 배치를 저장할 빈 문자열
#
#     for i in range(1, len(food)):         # 1번 음식부터 마지막 음식까지 반복 (0번은 물이므로 제외)
#         count = food[i] // 2              # 두 선수가 똑같이 먹어야 하므로 음식 개수를 2로 나눈 몫 계산
#         left += str(i) * count            # 음식 번호를 문자열로 변환하고 개수만큼 반복해서 추가
#
#     answer = left + "0" + left[::-1]       # 왼쪽 배치 + 가운데 물(0) + 왼쪽 배치를 뒤집은 오른쪽 배치
#
#     return answer                         # 완성된 음식 배치 문자열 반환
