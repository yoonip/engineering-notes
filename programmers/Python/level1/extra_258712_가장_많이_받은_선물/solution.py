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

# 전체 코드 줄별 설명
# def solution(friends, gifts):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 친구 이름과 선물 기록을 입력받음.
#     n = len(friends)  # len은 길이. =는 값 저장. 친구 수 계산.
#     index = {}  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 이름을 번호로 바꿀 딕셔너리.
#     for i, name in enumerate(friends):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 각 친구의 번호와 이름을 함께 순회.
#         index[name] = i  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 이름에 해당하는 번호 등록.
#     given = [[0] * n for _ in range(n)]  # range는 끝값 직전까지 정수 순서 생성. in은 포함 여부. []는 리스트. 내포문은 반복하면서 원소를 구성. =는 값 저장. 보낸 사람·받은 사람별 선물 수를 저장할 2차원 리스트.
#     score = [0] * n  # []는 리스트. =는 값 저장. 준 수에서 받은 수를 뺀 선물 지수.
#     received = [0] * n  # []는 리스트. =는 값 저장. 다음 달에 받을 선물 수.
#     for gift in gifts:  # for·in은 원소를 차례로 꺼내는 반복문. 현재까지의 선물 기록을 순회.
#         giver, receiver = gift.split()  # split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 보낸 사람과 받은 사람 이름으로 분리.
#         a = index[giver]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 보낸 사람의 번호 조회.
#         b = index[receiver]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 받은 사람의 번호 조회.
#         given[a][b] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 두 사람 사이에서 보낸 선물 횟수 증가.
#         score[a] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 보낸 사람의 선물 지수 증가.
#         score[b] -= 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. -=는 빼서 저장. 받은 사람의 선물 지수 감소.
#     for i in range(n):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 첫 친구 번호를 순회.
#         for j in range(i + 1, n):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. i보다 큰 번호만 골라 친구 쌍의 중복을 방지.
#             if given[i][j] > given[j][i]:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. >는 큼 비교. i가 j에게 더 많이 줬는지 비교.
#                 received[i] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. i가 다음 달에 하나 받음.
#             elif given[i][j] < given[j][i]:  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. <는 작음 비교. j가 i에게 더 많이 줬는지 비교.
#                 received[j] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. j가 다음 달에 하나 받음.
#             elif score[i] > score[j]:  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. >는 큼 비교. 주고받은 수가 같으면 i의 선물 지수가 큰지 비교.
#                 received[i] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. i가 하나 받음.
#             elif score[i] < score[j]:  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. <는 작음 비교. j의 선물 지수가 큰지 비교.
#                 received[j] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. j가 하나 받음.
#     return max(received)  # return은 결과를 돌려주고 함수 종료. max는 최댓값. 친구별 다음 달 수령 수 중 최댓값 반환.

# 풀이 요약
# 이름을 번호로 바꾸고 누가 누구에게 몇 번 줬는지를 표에 저장한다. 준 수-받은 수인 선물 지수도 함께 계산한다. 친구 쌍마다 주고받은 수를 먼저 비교하고 동률일 때만 선물 지수를 비교한다. 다음 달에 받는 수의 최댓값을 고른다.
# 친구 N명, 선물 기록 M개: 평균 시간 O(M+N²), 공간 O(N²).
