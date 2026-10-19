# 가장 많이 받은 선물
# 분류: 해시 / 쌍 비교
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/258712
# 선택 이유: 이름은 해시로 번호에 연결하고, 선물 기록을 한 번 집계한 뒤 친구 쌍을 한 번씩 비교한다.
# 비용: 친구 F명, 기록 G개: 평균 시간 O(G+F²), 추가 공간 O(F²).

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
