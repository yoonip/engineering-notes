# 중력 작용
# 분류: HLD / implicit treap / 구간 합
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/77887
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

from random import Random


def solution(values, edges, queries):
    n = len(values)
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a - 1].append(b - 1)
        graph[b - 1].append(a - 1)

    parent = [-1] * n
    order = [0]
    for u in order:
        for v in graph[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)

    subtree = [1] * n
    heavy = [-1] * n
    for u in reversed(order):
        p = parent[u]
        if p != -1:
            subtree[p] += subtree[u]
            if heavy[p] == -1 or subtree[u] > subtree[heavy[p]]:
                heavy[p] = u

    head = [0] * n
    position = [0] * n
    stack = [(0, 0)]
    timer = 0
    while stack:
        u, top = stack.pop()
        while u != -1:
            head[u] = top
            position[u] = timer
            timer += 1
            for v in graph[u]:
                if parent[v] == u and v != heavy[u]:
                    stack.append((v, v))
            u = heavy[u]

    left = [0] * (n + 1)
    right = [0] * (n + 1)
    size = [0] + [1] * n
    weight = [0] * (n + 1)
    for u in range(n):
        weight[position[u] + 1] = values[u]
    total = weight.copy()
    rng = Random(77887)
    priority = [rng.getrandbits(64) for _ in range(n + 1)]

    def pull(u):
        size[u] = size[left[u]] + size[right[u]] + 1
        total[u] = total[left[u]] + weight[u] + total[right[u]]

    def merge(a, b):
        if not a or not b:
            return a or b
        if priority[a] < priority[b]:
            right[a] = merge(right[a], b)
            pull(a)
            return a
        left[b] = merge(a, left[b])
        pull(b)
        return b

    def split(u, count):
        if not u:
            return 0, 0
        if count <= 0:
            return 0, u
        if count >= size[u]:
            return u, 0
        if count <= size[left[u]]:
            a, left[u] = split(left[u], count)
            pull(u)
            return a, u
        right[u], b = split(right[u], count - size[left[u]] - 1)
        pull(u)
        return u, b

    def prefix_sum(u, count):
        result = 0
        while u and count > 0:
            left_size = size[left[u]]
            if count <= left_size:
                u = left[u]
            else:
                result += total[left[u]] + weight[u]
                count -= left_size + 1
                u = right[u]
        return result

    root = 0
    for u in range(1, n + 1):
        root = merge(root, u)

    answer = []
    for u, w in queries:
        u -= 1
        if w == -1:
            start = position[u]
            end = start + subtree[u]
            answer.append(prefix_sum(root, end) - prefix_sum(root, start))
        else:
            segments = []
            while u != -1:
                top = head[u]
                segments.append((position[top], position[u]))
                u = parent[top]

            carry = w
            for start, end in reversed(segments):
                before, rest = split(root, start)
                segment, after = split(rest, end - start + 1)
                middle, last = split(segment, end - start)
                carry, weight[last] = weight[last], carry
                pull(last)
                root = merge(merge(before, merge(last, middle)), after)

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# from random import Random  # random 모듈에서 난수 생성기 Random을 가져옵니다. 별도 설치는 필요 없습니다.
#
#
# def solution(values, edges, queries):  # def는 함수 정의입니다. 세 매개변수로 초기 값, 간선, 명령을 받습니다.
#     n = len(values)  # len은 원소 수를 구합니다. n은 원래 트리의 노드 수입니다.
#     graph = [[] for _ in range(n)]  # 리스트 컴프리헨션으로 독립적인 빈 리스트 n개를 만듭니다. _는 쓰지 않을 반복 변수입니다.
#     for a, b in edges:  # 각 간선 리스트의 두 값을 a,b에 나누어 받는 언패킹입니다.
#         graph[a - 1].append(b - 1)  # 번호를 0부터 시작하도록 1을 빼고, append로 이웃 번호를 추가합니다.
#         graph[b - 1].append(a - 1)  # 간선은 양방향이므로 반대쪽 이웃 정보도 저장합니다.
#
#     parent = [-1] * n  # 원소가 -1인 리스트를 n칸 만듭니다. -1은 부모가 없다는 표시입니다.
#     order = [0]  # 루트의 내부 번호 0을 리스트에 넣어 시작합니다. 원래 번호는 1번입니다.
#     for u in order:  # order의 노드를 하나씩 읽습니다. 뒤에 append된 노드도 이어서 방문합니다.
#         for v in graph[u]:  # u번 노드의 이웃 번호를 v에 넣으며 반복합니다.
#             if v != parent[u]:  # !=는 같지 않다는 비교입니다. 트리에서 부모로 되돌아가는 간선을 제외합니다.
#                 parent[v] = u  # 리스트의 v번 칸에 부모 번호 u를 대입합니다.
#                 order.append(v)  # v를 뒤에 추가하여 이후 그 노드의 이웃도 방문합니다.
#
#     subtree = [1] * n  # 각 부분 트리의 노드 수입니다. 자기 자신을 세어 1로 시작합니다.
#     heavy = [-1] * n  # 가장 큰 부분 트리를 가진 자식 번호입니다. 자식이 없으면 -1입니다.
#     for u in reversed(order):  # reversed로 방문 순서를 뒤집어 자식의 계산을 부모보다 먼저 끝냅니다.
#         p = parent[u]  # u의 부모 번호를 p에 저장합니다.
#         if p != -1:  # 부모가 있는 노드만 처리합니다. 루트는 부모가 없습니다.
#             subtree[p] += subtree[u]  # +=는 더한 값을 다시 저장합니다. 자식의 노드 수를 부모 쪽에 더합니다.
#             if heavy[p] == -1 or subtree[u] > subtree[heavy[p]]:  # ==는 같음, or는 둘 중 하나가 참이면 참입니다. 자식이 처음이거나 더 큰 경우입니다.
#                 heavy[p] = u  # 가장 큰 자식 번호를 갱신합니다. 이 자식을 따라 하나의 긴 경로를 만듭니다.
#
#     head = [0] * n  # 각 노드가 속한 경로의 맨 위 노드 번호를 저장할 리스트입니다.
#     position = [0] * n  # 원래 트리의 각 노드가 배열에서 몇 번째 칸인지 저장합니다.
#     stack = [(0, 0)]  # 리스트에 (시작 노드, 경로의 맨 위) 튜플을 넣습니다. 튜플은 값의 묶음입니다.
#     timer = 0  # 배열 위치를 하나씩 부여할 정수 변수입니다.
#     while stack:  # 리스트가 비어 있지 않은 동안 반복합니다.
#         u, top = stack.pop()  # pop은 리스트의 마지막 원소를 꺼냅니다. 튜플의 두 값을 각각 받습니다.
#         while u != -1:  # u가 -1이 될 때까지 반복합니다. -1은 더 이어갈 노드가 없다는 표시입니다.
#             head[u] = top  # u가 속한 경로의 맨 위 노드를 기록합니다.
#             position[u] = timer  # u의 배열 위치를 기록합니다.
#             timer += 1  # 다음 노드에 쓸 위치를 1 늘립니다.
#             for v in graph[u]:  # u번 노드의 이웃 번호를 v에 넣으며 반복합니다.
#                 if parent[v] == u and v != heavy[u]:  # and는 두 조건이 모두 참일 때 참입니다. 가장 큰 자식 이외의 자식들을 고릅니다.
#                     stack.append((v, v))  # 이 자식에서 새 경로를 시작하도록 튜플을 스택에 넣습니다.
#             u = heavy[u]  # 가장 큰 자식으로 내려갑니다. 이 방식이 HLD라는 트리 분할입니다.
#
#     left = [0] * (n + 1)  # 별도의 자료구조인 트립에서 왼쪽 자식 번호를 저장합니다. 0은 빈 자식입니다.
#     right = [0] * (n + 1)  # 트립의 오른쪽 자식 번호를 저장합니다. 원래 트리의 자식과는 다른 정보입니다.
#     size = [0] + [1] * n  # 리스트를 +로 연결합니다. 트립의 0번은 크기 0, 실제 노드는 크기 1로 시작합니다.
#     weight = [0] * (n + 1)  # 트립의 각 항목이 담을 값을 저장합니다. 항목 번호는 1부터입니다.
#     for u in range(n):  # range(n)은 0부터 n-1까지의 정수를 제공합니다.
#         weight[position[u] + 1] = values[u]  # 원래 노드의 값을 새 배열 순서에 맞춰 저장합니다. 트립 항목 번호는 위치+1입니다.
#     total = weight.copy()  # copy로 새 리스트를 만듭니다. total은 각 트립 부분 트리의 값 합입니다.
#     rng = Random(77887)  # 고정된 시작값으로 난수 생성기를 만듭니다. 난수는 자료구조의 모양을 정하는 데만 씁니다.
#     priority = [rng.getrandbits(64) for _ in range(n + 1)]  # 64비트 난수 우선순위를 만듭니다. 작은 우선순위의 항목이 트립 위쪽에 옵니다.
#
#     def pull(u):  # solution 안에 정의한 보조 함수입니다. 바깥 함수의 리스트들을 읽고 원소를 변경합니다.
#         size[u] = size[left[u]] + size[right[u]] + 1  # 자식의 크기와 자기 자신 1개를 합쳐 크기를 다시 계산합니다.
#         total[u] = total[left[u]] + weight[u] + total[right[u]]  # 왼쪽 합, 자기 값, 오른쪽 합을 더합니다. 빈 자식 0번의 합은 0입니다.
#
#     def merge(a, b):  # 배열 순서상 a의 뒤에 b를 이어 붙인 트립의 루트를 반환하는 함수입니다.
#         if not a or not b:  # not은 참/거짓을 뒤집습니다. 번호 0은 거짓이므로 둘 중 하나가 빈 트립인지 검사합니다.
#             return a or b  # Python의 or는 값 자체를 반환합니다. 비어 있지 않은 쪽 번호를 돌려줍니다.
#         if priority[a] < priority[b]:  # <는 작다는 비교입니다. 우선순위가 작은 쪽을 합친 트립의 루트로 고릅니다.
#             right[a] = merge(right[a], b)  # 함수가 자신을 다시 부르는 재귀입니다. a의 오른쪽 부분에 b를 이어 붙입니다.
#             pull(a)  # 구조가 바뀐 뒤 a의 크기와 합을 갱신합니다.
#             return a  # a를 결과 트립의 루트 번호로 반환합니다.
#         left[b] = merge(a, left[b])  # b가 루트인 경우 그 왼쪽 부분 앞에 a를 이어 붙입니다.
#         pull(b)  # b의 크기와 합을 갱신합니다.
#         return b  # b를 결과 트립의 루트 번호로 반환합니다.
#
#     def split(u, count):  # 앞 count개 항목과 나머지 항목으로 나눈 두 트립의 루트를 반환합니다.
#         if not u:  # u가 0이면 빈 트립입니다.
#             return 0, 0  # 반환값 둘을 튜플로 묶어 돌려줍니다.
#         if count <= 0:  # <=는 작거나 같다는 비교입니다. 앞쪽으로 가져갈 항목이 없는 경우입니다.
#             return 0, u  # 앞쪽은 빈 트립, 뒤쪽은 기존 트립입니다.
#         if count >= size[u]:  # >=는 크거나 같다는 비교입니다. 전체 항목을 앞쪽으로 가져가는 경우입니다.
#             return u, 0  # 앞쪽은 기존 트립, 뒤쪽은 빈 트립입니다.
#         if count <= size[left[u]]:  # 나눌 경계가 왼쪽 부분 안에 있는지 확인합니다.
#             a, left[u] = split(left[u], count)  # 왼쪽 부분을 재귀적으로 나눕니다. 변수와 리스트 원소에 결과를 각각 대입합니다.
#             pull(u)  # u의 크기와 합을 갱신합니다.
#             return a, u  # 분리된 앞쪽 a와 남은 뒤쪽 u를 반환합니다.
#         right[u], b = split(right[u], count - size[left[u]] - 1)  # 왼쪽 크기와 자기 자신 1개를 제외하고 오른쪽 부분을 나눕니다.
#         pull(u)  # u의 크기와 합을 갱신합니다.
#         return u, b  # 앞쪽 u와 뒤쪽 b를 반환합니다.
#
#     def prefix_sum(u, count):  # 현재 배열에서 앞 count개 값의 합을 구하는 보조 함수입니다.
#         result = 0  # 합계를 정수 0으로 시작합니다.
#         while u and count > 0:  # 트립이 남아 있고 더 셀 항목이 있을 때 반복합니다.
#             left_size = size[left[u]]  # 왼쪽 부분의 항목 수를 읽습니다.
#             if count <= left_size:  # 필요한 항목이 전부 왼쪽 안에 있는지 확인합니다.
#                 u = left[u]  # 왼쪽 부분으로 내려갑니다.
#             else:  # 짝인 if 조건이 거짓인 경우 실행합니다.
#                 result += total[left[u]] + weight[u]  # 왼쪽 전체 합과 자기 값을 한 번에 더합니다.
#                 count -= left_size + 1  # -=는 뺀 값을 다시 저장합니다. 이미 센 항목 수를 제외합니다.
#                 u = right[u]  # 아직 필요한 항목을 오른쪽에서 찾습니다.
#         return result  # 구한 누적 합을 반환하고 보조 함수를 종료합니다.
#
#     root = 0  # 현재 배열 전체를 나타내는 트립의 루트입니다. 원래 트리의 루트 번호와 다릅니다.
#     for u in range(1, n + 1):  # range의 끝은 포함하지 않으므로 항목 번호 1부터 n까지 반복합니다.
#         root = merge(root, u)  # 항목 하나를 배열 뒤에 붙이며 전체 트립을 만듭니다.
#
#     answer = []  # 부분 트리 합 질문의 결과만 모을 빈 리스트입니다.
#     for u, w in queries:  # 각 명령의 두 정수를 u,w에 언패킹합니다.
#         u -= 1  # 입력 노드 번호를 내부의 0부터 시작하는 번호로 바꿉니다.
#         if w == -1:  # w가 -1이면 부분 트리 합을 묻는 명령입니다.
#             start = position[u]  # 부분 트리 구간의 시작 위치입니다.
#             end = start + subtree[u]  # 부분 트리의 끝 다음 위치입니다. end 자체는 구간에 포함하지 않습니다.
#             answer.append(prefix_sum(root, end) - prefix_sum(root, start))  # 끝까지의 누적 합에서 시작 전의 누적 합을 뺀 구간 합을 결과에 추가합니다.
#         else:  # 짝인 if 조건이 거짓인 경우 실행합니다.
#             segments = []  # 루트에서 목표 노드까지의 경로를 나눈 구간들을 저장할 리스트입니다.
#             while u != -1:  # u가 -1이 될 때까지 반복합니다. -1은 더 이어갈 노드가 없다는 표시입니다.
#                 top = head[u]  # 현재 노드가 속한 경로의 맨 위 노드를 읽습니다.
#                 segments.append((position[top], position[u]))  # (시작 위치, 마지막 위치) 튜플을 저장합니다. 여기서는 마지막 위치도 포함합니다.
#                 u = parent[top]  # 이 경로보다 위에 있는 다음 경로로 올라갑니다.
#
#             carry = w  # 현재 구간의 앞에 넣을 값입니다. 첫 구간에는 새 루트 값 w를 넣습니다.
#             for start, end in reversed(segments):  # 아래에서 모은 구간을 뒤집어 루트에 가까운 쪽부터 처리합니다.
#                 before, rest = split(root, start)  # 현재 배열을 구간 앞부분과 나머지로 나눕니다.
#                 segment, after = split(rest, end - start + 1)  # 나머지에서 대상 구간을 떼어냅니다. 끝을 포함하므로 길이에 +1을 합니다.
#                 middle, last = split(segment, end - start)  # 구간의 마지막 항목 1개를 분리합니다. middle에는 그 앞 항목들이 남습니다.
#                 carry, weight[last] = weight[last], carry  # 오른쪽 값들을 먼저 읽은 뒤 대입합니다. 마지막 옛 값을 넘기고 그 항목에는 carry를 넣습니다.
#                 pull(last)  # 분리한 항목의 값이 바뀌었으므로 합을 갱신합니다.
#                 root = merge(merge(before, merge(last, middle)), after)  # 앞부분 + 새 첫 항목 + 나머지 구간 + 뒷부분 순서로 합칩니다. 구간 값이 한 칸씩 밀립니다.
#
#     return answer  # 모든 질문의 합 결과를 순서대로 반환하고 solution을 종료합니다.
