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

# 전체 코드 줄별 설명
# def solution(edges):  # def는 함수 정의, () 안 edges는 간선 목록 입력, : 아래 들여쓰기는 본문.
#     size = max(max(a, b) for a, b in edges) + 1  # max는 최댓값. for로 간선의 두 번호를 풀어 받아 가장 큰 번호+1 계산.
#     incoming = [0] * size  # [0]은 리스트, * size는 반복. 정점별 들어오는 간선 수 저장.
#     outgoing = [0] * size  # 정점별 나가는 간선 수를 0으로 초기화. =는 대입.
#     for a, b in edges:  # for~in으로 간선을 순회하고 a,b에 시작·끝 번호를 언패킹.
#         outgoing[a] += 1  # [a]는 a번째 원소 접근, +=는 더해 저장. 나가는 간선 증가.
#         incoming[b] += 1  # 끝 정점에 들어오는 간선 수를 1 증가.
#     created = sticks = eights = 0  # 연쇄 대입으로 생성 정점·막대 수·8자 수를 모두 0으로 초기화.
#     for node in range(1, size):  # range(시작,끝)은 끝 미포함 정수 범위. 정점 번호 순회.
#         if incoming[node] == 0 and outgoing[node] >= 2:  # if는 조건 분기, ==는 같음, >=는 이상, and는 둘 다 참.
#             created = node  # 진입 0·진출 2 이상인 정점은 추가한 정점.
#         elif outgoing[node] == 0 and incoming[node] > 0:  # elif는 앞 조건이 거짓일 때 검사. 사용 중인 정점의 막다른 끝 판별.
#             sticks += 1  # 막대마다 끝 정점이 하나이므로 막대 수 증가.
#         elif outgoing[node] == 2 and incoming[node] >= 2:  # 진출 2·진입 2 이상인 정점은 8자의 가운데 정점.
#             eights += 1  # 8자마다 가운데 정점 하나를 셈.
#     donuts = outgoing[created] - sticks - eights  # 생성 정점의 진출 수는 전체 그래프 수. 막대와 8자를 빼 도넛 수 계산.
#     return [created, donuts, sticks, eights]  # return은 결과 반환. []로 네 값을 순서 있는 리스트로 묶음.

# 풀이 요약
# 진입·진출 차수로 추가 정점, 막대의 끝, 8자의 중심을 센 뒤 나머지를 도넛으로 계산합니다.
# 예: 첫 예제는 추가 정점 2의 진출 2개에서 막대 1개를 빼 [2,1,1,0]. 시간 O(E+M), 공간 O(M), M은 최대 정점 번호.
