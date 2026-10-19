# 가장 많이 받은 선물
# 분류: 해시 / 쌍 비교
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/258712
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(friends, gifts):
    n = len(friends)
    index = {}

    for i, name in enumerate(friends):
        index[name] = i

    given = [[0] * n for _ in range(n)]
    score = [0] * n
    received = [0] * n

    for gift in gifts:
        giver, receiver = gift.split()
        a = index[giver]
        b = index[receiver]

        given[a][b] += 1
        score[a] += 1
        score[b] -= 1

    for i in range(n):
        for j in range(i + 1, n):
            if given[i][j] > given[j][i]:
                received[i] += 1
            elif given[i][j] < given[j][i]:
                received[j] += 1
            elif score[i] > score[j]:
                received[i] += 1
            elif score[i] < score[j]:
                received[j] += 1

    return max(received)


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# # def는 함수를 정의합니다. friends, gifts는 채점기에서 전달받는 매개변수입니다.
# # 콜론(:) 다음의 들여쓴 코드가 함수의 몸체입니다. import는 필요 없습니다.
# def solution(friends, gifts):
#     # len(리스트)는 원소 개수를 반환합니다. n은 친구 수를 담는 변수입니다.
#     n = len(friends)
#     # {}는 빈 딕셔너리입니다. 딕셔너리는 '키: 값'을 연결해 저장합니다.
#     # 예: {"muzi": 0, "ryan": 1}에서 index["ryan"]은 1입니다.
#     index = {}
#
#     # enumerate는 (번호, 원소) 튜플을 순서대로 만듭니다. 번호는 기본적으로 0부터입니다.
#     # 튜플은 여러 값을 묶는 자료형입니다. 만들어진 튜플의 원소는 바꿀 수 없습니다.
#     # i, name은 튜플의 두 값을 각각 받는 '언패킹' 문법입니다.
#     for i, name in enumerate(friends):
#         # 딕셔너리에 이름을 키로, 번호를 값으로 저장합니다.
#         index[name] = i
#
#     # [0] * n은 0이 n개인 리스트입니다.
#     # 리스트 컴프리헨션 [... for ... in ...]은 반복하면서 새 리스트를 만듭니다.
#     # 매번 새 행을 만들므로 서로 독립적인 n개 행을 가진 2차원 리스트가 됩니다.
#     # _는 값을 사용하지 않을 반복 변수에 관례적으로 붙이는 이름입니다.
#     # given[a][b]는 a번 사람이 b번 사람에게 준 횟수입니다.
#     # [[0]*n]*n으로 만들면 행을 공유하므로 여기서는 사용하지 않습니다.
#     given = [[0] * n for _ in range(n)]
#     # score[i]는 i번 친구의 이번 달까지의 선물 지수입니다.
#     score = [0] * n
#     # received[i]는 i번 친구가 '다음 달에 받을 개수'입니다.
#     received = [0] * n
#
#     # for는 gifts의 문자열을 하나씩 꺼내 gift에 대입하며 반복합니다.
#     for gift in gifts:
#         # 문자열.split()은 공백을 기준으로 나눈 문자열 리스트를 반환합니다.
#         # "muzi frodo".split() → ["muzi", "frodo"]
#         # 두 원소를 giver와 receiver에 각각 대입합니다(리스트도 언패킹 가능).
#         giver, receiver = gift.split()
#         # 이름에 연결된 정수 번호를 딕셔너리에서 읽습니다.
#         a = index[giver]
#         b = index[receiver]
#
#         # += 1은 기존 값에 1을 더해 다시 저장합니다.
#         # 2차원 리스트는 [행번호][열번호]로 접근합니다.
#         given[a][b] += 1
#         score[a] += 1
#         # -= 1은 기존 값에서 1을 뺍니다.
#         score[b] -= 1
#
#     # range(n)은 0부터 n-1까지의 정수를 순서대로 제공합니다.
#     for i in range(n):
#         # range(시작, 끝)은 시작 이상, 끝 미만의 정수입니다.
#         # j는 i보다 큰 번호만 받습니다. 자기 자신과 비교하거나 같은 쌍을 반복하지 않습니다.
#         for j in range(i + 1, n):
#             # >는 크다, <는 작다라는 비교 연산입니다.
#             if given[i][j] > given[j][i]:
#                 received[i] += 1
#             # elif는 앞의 if/elif 조건들이 거짓일 때만 검사합니다.
#             elif given[i][j] < given[j][i]:
#                 received[j] += 1
#             # 앞의 >와 <가 모두 거짓이면 서로 준 횟수가 같다는 뜻입니다.
#             # 그때에만 선물 지수 비교로 넘어옵니다.
#             elif score[i] > score[j]:
#                 received[i] += 1
#             elif score[i] < score[j]:
#                 received[j] += 1
#             # 지수도 같으면 실행할 분기가 없으므로 아무것도 더하지 않습니다.
#
#     # max(리스트)는 가장 큰 원소를 반환합니다.
#     # return은 값을 호출한 곳에 전달하고 함수 전체를 종료합니다.
#     return max(received)
