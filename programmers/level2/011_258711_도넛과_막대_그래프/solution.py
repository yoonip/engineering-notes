# 문제: 도넛과 막대 그래프
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/258711
# 풀이: 진입·진출 차수로 생성 정점, 막대 끝, 8자 중심을 구분한다. 생성 정점의 간선 수에서 막대와 8자 수를 빼 도넛 수를 얻는다.
# 복잡도: 간선 E개·최대 정점 번호 M: 시간 O(E+M), 추가 공간 O(M).

def solution(edges):
    size = max(max(a, b) for a, b in edges) + 1
    incoming = [0] * size
    outgoing = [0] * size
    for a, b in edges:
        outgoing[a] += 1
        incoming[b] += 1
    created = sticks = eights = 0
    for node in range(1, size):
        if incoming[node] == 0 and outgoing[node] >= 2:
            created = node
        elif outgoing[node] == 0 and incoming[node] > 0:
            sticks += 1
        elif outgoing[node] == 2 and incoming[node] >= 2:
            eights += 1
    donuts = outgoing[created] - sticks - eights
    return [created, donuts, sticks, eights]
