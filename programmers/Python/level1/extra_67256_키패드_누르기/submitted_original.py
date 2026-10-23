def solution(numbers, hand):
    positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 9: (2, 2),
        0: (3, 1)
    }

    left_pos = (3, 0)
    right_pos = (3, 2)
    answer = []

    for number in numbers:
        target = positions[number]

        if number in (1, 4, 7):
            used_hand = "L"
        elif number in (3, 6, 9):
            used_hand = "R"
        else:
            left_distance = abs(left_pos[0] - target[0]) + abs(left_pos[1] - target[1])
            right_distance = abs(right_pos[0] - target[0]) + abs(right_pos[1] - target[1])

            if left_distance < right_distance:
                used_hand = "L"
            elif left_distance > right_distance:
                used_hand = "R"
            elif hand == "left":
                used_hand = "L"
            else:
                used_hand = "R"

        if used_hand == "L":
            left_pos = target
        else:
            right_pos = target

        answer.append(used_hand)

    return "".join(answer)


# ============================================================
# 학습용: 위와 같은 코드 + 각 줄의 설명
# 아래는 전체가 주석이므로 실행되지 않음
# ============================================================

# def solution(numbers, hand):  # numbers: 누를 번호 목록, hand: "left" 또는 "right"
#     positions = {  # 각 숫자와 그 숫자의 (행, 열) 좌표를 연결한 딕셔너리
#         1: (0, 0), 2: (0, 1), 3: (0, 2),  # 첫 번째 행의 숫자와 좌표
#         4: (1, 0), 5: (1, 1), 6: (1, 2),  # 두 번째 행의 숫자와 좌표
#         7: (2, 0), 8: (2, 1), 9: (2, 2),  # 세 번째 행의 숫자와 좌표
#         0: (3, 1)  # 숫자 0은 마지막 행의 가운데에 있음
#     }  # 딕셔너리 정의 끝
#
#     left_pos = (3, 0)  # 왼손 시작 위치: "*"의 좌표
#     right_pos = (3, 2)  # 오른손 시작 위치: "#"의 좌표
#     answer = []  # 번호를 누를 때마다 사용한 손 "L" 또는 "R"을 저장
#
#     for number in numbers:  # 눌러야 할 번호를 순서대로 하나씩 꺼냄
#         target = positions[number]  # 현재 누를 번호의 좌표. 예: 번호 5 → (1, 1)
#
#         if number in (1, 4, 7):  # 현재 번호가 왼쪽 열의 숫자라면
#             used_hand = "L"  # 거리와 상관없이 왼손을 선택
#         elif number in (3, 6, 9):  # 현재 번호가 오른쪽 열의 숫자라면
#             used_hand = "R"  # 거리와 상관없이 오른손을 선택
#         else:  # 나머지 숫자 2, 5, 8, 0은 두 손의 거리를 비교
#             left_distance = abs(left_pos[0] - target[0]) + abs(left_pos[1] - target[1])  # 왼손 거리
#             right_distance = abs(right_pos[0] - target[0]) + abs(right_pos[1] - target[1])  # 오른손 거리
#
#             if left_distance < right_distance:  # 왼손이 더 가까우면
#                 used_hand = "L"  # 왼손을 선택
#             elif left_distance > right_distance:  # 오른손이 더 가까우면
#                 used_hand = "R"  # 오른손을 선택
#             elif hand == "left":  # 두 거리가 같고, 왼손잡이라면
#                 used_hand = "L"  # 왼손을 선택
#             else:  # 두 거리가 같고, 오른손잡이라면
#                 used_hand = "R"  # 오른손을 선택
#
#         if used_hand == "L":  # 이번 번호를 왼손으로 눌렀다면
#             left_pos = target  # 왼손 위치만 누른 번호의 좌표로 변경
#         else:  # 이번 번호를 오른손으로 눌렀다면
#             right_pos = target  # 오른손 위치만 누른 번호의 좌표로 변경
#
#         answer.append(used_hand)  # 이번에 사용한 손을 결과 리스트 맨 뒤에 추가
#
#     return "".join(answer)  # ["L", "R", "L"]처럼 저장된 결과를 "LRL"로 연결해서 반환
#
# ------------------------------------------------------------
# 헷갈리기 쉬운 부분
# ------------------------------------------------------------
# 키패드의 좌표는 (행, 열) 순서이며, 0부터 시작함.
#
#           열 0       열 1       열 2
# 행 0      1          2          3
# 행 1      4          5          6
# 행 2      7          8          9
# 행 3      *          0          #
#
# target이 (1, 2)라면:
# target[0] → 행 번호 1
# target[1] → 열 번호 2
#
# abs()는 절댓값을 구하는 함수.
# abs(-2)도 2이고, abs(2)도 2임.
# 이동 거리는 음수가 아니므로 좌표 차이에 abs()를 사용함.
#
# 상하좌우로만 이동하므로 거리는 '행 차이 + 열 차이'로 계산함.
# 대각선으로 한 번에 이동하는 것으로 계산하면 안 됨.
#
# 예: 왼손이 4번 (1, 0), 오른손이 3번 (0, 2)에 있고 5번 (1, 1)을 누를 때
# 왼손 거리: abs(1 - 1) + abs(0 - 1) = 0 + 1 = 1
# 오른손 거리: abs(0 - 1) + abs(2 - 1) = 1 + 1 = 2
# 왼손이 가까우므로 "L"을 기록하고, 왼손 위치를 (1, 1)로 변경함.
# 오른손은 이동하지 않았으므로 (0, 2)에 그대로 남음.
#
# hand는 거리가 같은 경우에만 사용함.
# 왼손잡이라도 오른손이 더 가까우면 가운데 숫자를 오른손으로 눌러야 함.
#
# 사용한 손의 위치를 반드시 갱신해야 다음 번호의 거리를 올바르게 계산할 수 있음.
# 손은 번호를 누른 뒤 시작 위치인 "*"나 "#"로 돌아가지 않음.
#
# ------------------------------------------------------------
# 예제
# ------------------------------------------------------------
# numbers = [1, 3, 4, 5, 8, 2, 1, 4, 5, 9, 5]
# hand = "right"
#
# 사용한 손: L, R, L, L, L, R, L, L, R, R, L
# 최종 반환값: "LRLLLRLLRRL"