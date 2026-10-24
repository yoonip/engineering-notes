# 중력 작용 — Python 재풀이

[문제 원문](<https://school.programmers.co.kr/learn/courses/30/lessons/77887>) · [재풀이 목록](<../README.md>)

정답률 1%와 풀이 인원 87명은 이번 목록 확인 시점의 값입니다. 전체 13순위로 진행했습니다.

## 사이트 채점

사이트 채점 합계 100점과 이번 재풀이 이후의 Python3 정답 100점 제출 내역을 확인했습니다. 정답은 실제 1번째 제출이며, 총 1회 제출했습니다.

| 제출 | 결과 | 합계 점수 | 입력 코드 | 채점 기록 |
| --- | --- | ---: | --- | --- |
| 1 | 정답 | 100 | [코드](<solution.py>) | [채점 결과 발췌](<attempts/attempt1_grading.txt>) |

[채점·제출 내역 JSON](<grading.json>)에는 실제 제출 시각, 합계, 테스트별 결과와 시간, 메모리, 입력 SHA256 및 새 제출 내역을 기록합니다. 제출한 입력 파일은 원본 바이트를 보관하며, 화면에 넣을 때의 LF 정규화 해시를 별도 기록합니다.

## 로컬 검증

[제출 전 후보 검증 원본](<local_checks.json>)은 사이트 채점과 별도인 로컬 비교·성능 기록입니다. 로컬 검증에 기록한 코드 해시는 정답 제출 입력과 같습니다.

## 풀이 요약

부분 트리가 가장 큰 자식을 이어 중경로를 만들면 루트까지 지나가는 중경로는 O(log N)개. 중경로 우선 전위 순서에서 각 부분 트리는 연속 구간.
중경로마다 값 순서를 암묵적 트립으로 보관. 중력 쿼리는 중경로 앞부분의 마지막 항목을 앞으로 돌리고 값을 교체하며, 밀려난 값을 다음 중경로로 전달.
중경로 전체 합은 그 시작점의 전위 위치 한 칸에 펜윅 트리로 저장. 부분 트리 합은 그 구간의 중경로 전체 합들과 자기 중경로의 필요한 뒷부분을 합쳐 계산.
트리 순회는 반복문으로 처리하고, 의사난수 우선순위로 균형 잡힌 트립의 분할·병합에만 재귀 사용. 초기화 O(N), 쿼리당 기대 O(log²N), 작업 공간 O(N).

## 정답 제출 코드

실제 1번째 정답 제출 입력의 전체 내용입니다. 원본 파일의 줄바꿈 바이트는 그대로 두며, 아래 표시는 LF로 정규화합니다.

```python
def solution(values, edges, queries):
    n = len(values)
    adjacent = [[] for _ in range(n)]
    for a, b in edges:
        a -= 1
        b -= 1
        adjacent[a].append(b)
        adjacent[b].append(a)
    parent = [-1] * n
    order = [0]
    for node in order:
        for child in adjacent[node]:
            if child != parent[node]:
                parent[child] = node
                order.append(child)
    subtree_size = [1] * n
    heavy = [-1] * n
    for node in reversed(order):
        for child in adjacent[node]:
            if child == parent[node]:
                continue
            subtree_size[node] += subtree_size[child]
            if heavy[node] < 0 or subtree_size[child] > subtree_size[heavy[node]]:
                heavy[node] = child
    head = [0] * n
    position = [0] * n
    roots = [0] * n
    chain_total = [0] * n
    left = [0] * (n + 1)
    right = [0] * (n + 1)
    item_size = [1] * (n + 1)
    item_size[0] = 0
    weight = [0] * (n + 1)
    item_sum = [0] * (n + 1)
    priority = [0] * (n + 1)
    heads = []
    pending = [0]
    timer = 0
    random_state = 2463534242
    while pending:
        first = pending.pop()
        heads.append(first)
        node = first
        cartesian = []
        while node != -1:
            head[node] = first
            position[node] = timer
            timer += 1
            entry = timer
            weight[entry] = item_sum[entry] = values[node]
            chain_total[first] += values[node]
            random_state ^= (random_state << 13) & 0xFFFFFFFF
            random_state ^= random_state >> 17
            random_state ^= (random_state << 5) & 0xFFFFFFFF
            priority[entry] = random_state
            previous = 0
            while cartesian and priority[cartesian[-1]] < priority[entry]:
                previous = cartesian.pop()
            left[entry] = previous
            if cartesian:
                right[cartesian[-1]] = entry
            else:
                roots[first] = entry
            cartesian.append(entry)
            for child in adjacent[node]:
                if child != parent[node] and child != heavy[node]:
                    pending.append(child)
            node = heavy[node]

    def pull(node):
        a, b = left[node], right[node]
        item_size[node] = item_size[a] + item_size[b] + 1
        item_sum[node] = item_sum[a] + weight[node] + item_sum[b]

    item_order = [roots[first] for first in heads]
    for entry in item_order:
        if left[entry]:
            item_order.append(left[entry])
        if right[entry]:
            item_order.append(right[entry])
    for entry in reversed(item_order):
        pull(entry)
    bit = [0] * (n + 1)
    for first in heads:
        bit[position[first] + 1] = chain_total[first]
    for index in range(1, n + 1):
        upper = index + (index & -index)
        if upper <= n:
            bit[upper] += bit[index]

    def fenwick_prefix(count):
        total = 0
        while count:
            total += bit[count]
            count -= count & -count
        return total

    def merge(a, b):
        if not a:
            return b
        if not b:
            return a
        if priority[a] > priority[b]:
            right[a] = merge(right[a], b)
            pull(a)
            return a
        left[b] = merge(a, left[b])
        pull(b)
        return b

    def split(node, count):
        if not node or count <= 0:
            return 0, node
        if count >= item_size[node]:
            return node, 0
        before = item_size[left[node]]
        if count <= before:
            a, b = split(left[node], count)
            left[node] = b
            pull(node)
            return a, node
        a, b = split(right[node], count - before - 1)
        right[node] = a
        pull(node)
        return node, b

    def chain_prefix(node, count):
        if count >= item_size[node]:
            return item_sum[node]
        total = 0
        while node and count > 0:
            before = item_size[left[node]]
            if count <= before:
                node = left[node]
            else:
                total += item_sum[left[node]] + weight[node]
                count -= before + 1
                node = right[node]
        return total

    answer = []
    for node, incoming in queries:
        node -= 1
        if incoming == -1:
            first = head[node]
            begin = position[node]
            total = fenwick_prefix(begin + subtree_size[node]) - fenwick_prefix(begin)
            if node == first:
                total -= chain_total[first]
            total += item_sum[roots[first]] - chain_prefix(roots[first], begin - position[first])
            answer.append(total)
            continue
        tails = []
        current = node
        while current != -1:
            tails.append(current)
            current = parent[head[current]]
        for tail in reversed(tails):
            first = head[tail]
            length = position[tail] - position[first] + 1
            path, after = split(roots[first], length)
            middle, last = split(path, length - 1)
            outgoing = weight[last]
            weight[last] = item_sum[last] = incoming
            roots[first] = merge(merge(last, middle), after)
            change = incoming - outgoing
            if change:
                chain_total[first] += change
                index = position[first] + 1
                while index <= n:
                    bit[index] += change
                    index += index & -index
            incoming = outgoing
    merge = split = None
    return answer

# 전체 코드 줄별 설명
# def solution(values, edges, queries):  # 중력에 따른 경로 값 이동과 부분 트리 합 쿼리 처리
#     n = len(values)  # 트리의 정점 수
#     adjacent = [[] for _ in range(n)]  # 0번부터 사용할 양방향 인접 목록
#     for a, b in edges:  # 입력 정점 번호는 1부터 시작
#         a -= 1  # 첫 끝점을 0 기반 번호로 변환
#         b -= 1  # 둘째 끝점도 변환
#         adjacent[a].append(b)  # 첫 끝점에서 둘째 끝점으로 연결
#         adjacent[b].append(a)  # 반대 방향도 연결
#     parent = [-1] * n  # 루트의 부모는 -1로 유지
#     order = [0]  # 부모가 자식보다 먼저 나오는 방문 순서
#     for node in order:  # 자식을 뒤에 추가하며 트리 순회
#         for child in adjacent[node]:  # 현재 정점의 이웃 검사
#             if child != parent[node]:  # 부모로 되돌아가는 간선은 제외
#                 parent[child] = node  # 자식의 부모 기록
#                 order.append(child)  # 자식을 방문 순서 뒤에 추가
#     subtree_size = [1] * n  # 자기 자신을 포함한 부분 트리 크기
#     heavy = [-1] * n  # 가장 큰 자식 부분 트리로 이어지는 중경로 간선
#     for node in reversed(order):  # 자식 크기를 먼저 구한 뒤 부모에 합산
#         for child in adjacent[node]:  # 아래쪽 자식들의 크기 비교
#             if child == parent[node]:  # 부모 쪽은 합산하지 않기
#                 continue  # 다음 이웃 확인
#             subtree_size[node] += subtree_size[child]  # 자식 부분 트리의 정점 수 추가
#             if heavy[node] < 0 or subtree_size[child] > subtree_size[heavy[node]]:  # 현재까지 가장 큰 자식이면 중경로로 선택
#                 heavy[node] = child  # 중경로로 내려갈 자식 번호
#     head = [0] * n  # 각 정점이 속한 중경로의 맨 위 정점
#     position = [0] * n  # 중경로 우선 방문 순서의 고정 위치
#     roots = [0] * n  # 각 중경로의 값 순서를 저장할 트립 루트
#     chain_total = [0] * n  # 각 중경로 전체의 현재 값 합
#     left = [0] * (n + 1)  # 트립 항목의 왼쪽 자식 번호, 0은 빈 항목
#     right = [0] * (n + 1)  # 트립 항목의 오른쪽 자식 번호
#     item_size = [1] * (n + 1)  # 트립 부분 구간의 항목 수
#     item_size[0] = 0  # 빈 항목의 크기는 0
#     weight = [0] * (n + 1)  # 트립 항목 하나의 현재 값
#     item_sum = [0] * (n + 1)  # 트립 부분 구간의 값 합
#     priority = [0] * (n + 1)  # 트립 균형을 위한 의사난수 우선순위
#     heads = []  # 실제로 존재하는 중경로의 맨 위 정점들
#     pending = [0]  # 아직 위치를 배정하지 않은 중경로 시작점
#     timer = 0  # 다음 정점에 배정할 전위 방문 위치
#     random_state = 2463534242  # 32비트 xorshift의 0이 아닌 고정 시작값
#     while pending:  # 중경로를 끝까지 배정한 뒤 남은 가벼운 가지 처리
#         first = pending.pop()  # 다음 중경로의 시작점
#         heads.append(first)  # 나중에 중경로별 합과 트립 루트를 초기화할 목록
#         node = first  # 현재 중경로에서 위치를 배정할 정점
#         cartesian = []  # 우선순위가 감소하는 트립 구성용 스택
#         while node != -1:  # 가장 큰 자식만 따라 중경로 끝까지 이동
#             head[node] = first  # 현재 정점의 중경로 시작점 기록
#             position[node] = timer  # 부분 트리 구간에도 쓸 고정 전위 방문 위치
#             timer += 1  # 트립 항목 번호는 빈 항목 0과 구분해 1부터 사용
#             entry = timer  # 현재 값에 대응하는 트립 항목 번호
#             weight[entry] = item_sum[entry] = values[node]  # 초기 값과 한 항목짜리 합 설정
#             chain_total[first] += values[node]  # 현재 중경로의 초기 합 누적
#             random_state ^= (random_state << 13) & 0xFFFFFFFF  # 32비트 범위를 유지하며 첫 xorshift 혼합
#             random_state ^= random_state >> 17  # 상위 비트를 하위 비트에 섞기
#             random_state ^= (random_state << 5) & 0xFFFFFFFF  # 마지막 혼합으로 항목 우선순위 만들기
#             priority[entry] = random_state  # 값이 이동해도 항목의 우선순위는 유지
#             previous = 0  # 새 항목의 왼쪽에 붙일 이전 스택 부분
#             while cartesian and priority[cartesian[-1]] < priority[entry]:  # 새 항목보다 우선순위가 낮은 스택 루트들을 꺼내기
#                 previous = cartesian.pop()  # 마지막으로 꺼낸 부분이 새 항목의 왼쪽 자식
#             left[entry] = previous  # 새 항목 앞의 값 순서를 왼쪽 부분 트리로 연결
#             if cartesian:  # 더 높은 우선순위의 앞 항목이 남아 있으면
#                 right[cartesian[-1]] = entry  # 그 항목의 오른쪽에 새 항목 연결
#             else:  # 더 높은 우선순위가 앞에 없으면
#                 roots[first] = entry  # 새 항목이 현재 중경로 트립의 루트
#             cartesian.append(entry)  # 새 항목도 구성 스택에 등록
#             for child in adjacent[node]:  # 가벼운 자식들은 별도 중경로로 나중에 처리
#                 if child != parent[node] and child != heavy[node]:  # 부모와 중경로 자식을 제외한 아래 가지
#                     pending.append(child)  # 가벼운 가지의 시작점 등록
#             node = heavy[node]  # 중경로의 다음 정점으로 이동
#
#     def pull(node):  # 트립 자식이 바뀐 항목의 크기와 합 갱신
#         a, b = left[node], right[node]  # 현재 항목의 양쪽 자식
#         item_size[node] = item_size[a] + item_size[b] + 1  # 두 자식 구간에 현재 항목 하나 추가
#         item_sum[node] = item_sum[a] + weight[node] + item_sum[b]  # 두 자식 구간 합과 현재 값 합산
#
#     item_order = [roots[first] for first in heads]  # 중경로별 트립 루트부터 항목 순회 시작
#     for entry in item_order:  # 자식들을 뒤에 붙여 부모 우선 순서 만들기
#         if left[entry]:  # 왼쪽 부분이 비어 있지 않은 경우
#             item_order.append(left[entry])  # 왼쪽 자식 등록
#         if right[entry]:  # 오른쪽 부분이 비어 있지 않은 경우
#             item_order.append(right[entry])  # 오른쪽 자식 등록
#     for entry in reversed(item_order):  # 자식부터 트립의 초기 구간 정보 계산
#         pull(entry)  # 해당 항목의 크기와 합 완성
#     bit = [0] * (n + 1)  # 중경로 전체 합을 시작점의 전위 위치에 놓을 펜윅 트리
#     for first in heads:  # 각 중경로는 시작점 위치 하나에 합을 저장
#         bit[position[first] + 1] = chain_total[first]  # 펜윅 트리 위치는 1부터 사용
#     for index in range(1, n + 1):  # 점 배열로부터 펜윅 트리를 선형 시간에 구성
#         upper = index + (index & -index)  # 현재 구간을 포함하는 다음 펜윅 노드
#         if upper <= n:  # 트리 범위 안에 있는 상위 노드만 갱신
#             bit[upper] += bit[index]  # 현재 구간 합을 상위 구간에 추가
#
#     def fenwick_prefix(count):  # 전위 순서의 처음 count칸에 놓인 중경로 합
#         total = 0  # 펜윅 구간들의 합 누적
#         while count:  # 가장 낮은 1비트가 담당하는 구간을 차례로 합산
#             total += bit[count]  # 현재 펜윅 구간 합 추가
#             count -= count & -count  # 이미 더한 끝 구간을 제외
#         return total  # 전위 구간 앞부분의 중경로 합 반환
#
#     def merge(a, b):  # 앞 순서 a 뒤에 뒤 순서 b를 이어 붙이는 트립 병합
#         if not a:  # 앞 순서가 비었으면
#             return b  # 뒤 순서를 그대로 사용
#         if not b:  # 뒤 순서가 비었으면
#             return a  # 앞 순서를 그대로 사용
#         if priority[a] > priority[b]:  # 앞 루트의 우선순위가 높으면 결과 루트로 유지
#             right[a] = merge(right[a], b)  # 앞 루트의 오른쪽 뒤에 b 연결
#             pull(a)  # 변경된 오른쪽 부분을 크기와 합에 반영
#             return a  # 앞 루트를 병합 결과로 반환
#         left[b] = merge(a, left[b])  # 뒤 루트가 높으면 그 왼쪽 앞에 a 연결
#         pull(b)  # 변경된 왼쪽 부분을 크기와 합에 반영
#         return b  # 뒤 루트를 병합 결과로 반환
#
#     def split(node, count):  # 값 순서의 처음 count개와 나머지를 나누기
#         if not node or count <= 0:  # 빈 순서이거나 앞에 둘 항목이 없으면
#             return 0, node  # 앞부분은 비우고 전체를 뒷부분으로 반환
#         if count >= item_size[node]:  # 모든 항목을 앞에 두는 경우
#             return node, 0  # 전체와 빈 뒷부분 반환
#         before = item_size[left[node]]  # 현재 항목 앞에 놓인 왼쪽 항목 수
#         if count <= before:  # 분할 위치가 왼쪽 부분 안에 있는 경우
#             a, b = split(left[node], count)  # 왼쪽 부분에서 앞 count개를 분리
#             left[node] = b  # 남은 왼쪽 부분은 현재 항목 앞에 유지
#             pull(node)  # 분리 후 크기와 합 갱신
#             return a, node  # 떼어낸 앞부분과 현재 루트의 나머지 반환
#         a, b = split(right[node], count - before - 1)  # 왼쪽과 현재 항목을 제외한 개수만큼 오른쪽에서 분리
#         right[node] = a  # 앞부분에 속한 오른쪽 항목들을 유지
#         pull(node)  # 분리 후 크기와 합 갱신
#         return node, b  # 현재 루트의 앞부분과 떼어낸 뒷부분 반환
#
#     def chain_prefix(node, count):  # 한 중경로에서 앞 count개 값의 합
#         if count >= item_size[node]:  # 중경로 전체가 범위에 들어오면
#             return item_sum[node]  # 저장해 둔 전체 합을 바로 사용
#         total = 0  # 앞부분의 값 합 누적
#         while node and count > 0:  # 필요한 항목 수만큼 트립을 따라 탐색
#             before = item_size[left[node]]  # 현재 항목 앞의 왼쪽 구간 크기
#             if count <= before:  # 필요한 앞부분이 왼쪽 안에 모두 있으면
#                 node = left[node]  # 왼쪽으로만 이동
#             else:  # 왼쪽 전체와 현재 항목을 포함해야 하면
#                 total += item_sum[left[node]] + weight[node]  # 왼쪽 구간과 현재 값 합산
#                 count -= before + 1  # 이미 합산한 항목 수 제외
#                 node = right[node]  # 남은 앞부분을 오른쪽에서 탐색
#         return total  # 중경로 앞부분의 값 합 반환
#
#     answer = []  # 부분 트리 합 쿼리의 결과를 순서대로 저장
#     for node, incoming in queries:  # 쿼리의 정점과 새 루트 값 또는 -1 구분
#         node -= 1  # 쿼리 정점도 0 기반으로 변환
#         if incoming == -1:  # 부분 트리 합을 묻는 쿼리
#             first = head[node]  # 현재 정점이 속한 중경로의 시작점
#             begin = position[node]  # 부분 트리의 전위 구간 시작 위치
#             total = fenwick_prefix(begin + subtree_size[node]) - fenwick_prefix(begin)  # 부분 트리 안에서 시작하는 중경로 전체 합들
#             if node == first:  # 현재 중경로의 시작점도 이 구간에 포함됐다면
#                 total -= chain_total[first]  # 자기 중경로 전체 합은 빼고 필요한 뒷부분만 더하기
#             total += item_sum[roots[first]] - chain_prefix(roots[first], begin - position[first])  # 자기 중경로에서 현재 정점 아래로 이어지는 값들의 합 추가
#             answer.append(total)  # 현재 부분 트리 합 기록
#             continue  # 다음 쿼리로 이동
#         tails = []  # 루트까지 올라가며 지나갈 중경로 구간의 끝점들
#         current = node  # 중력을 적용할 가장 아래 정점에서 시작
#         while current != -1:  # 중경로 하나씩 건너 부모 방향으로 올라가기
#             tails.append(current)  # 이번 중경로에서 이동시킬 마지막 정점
#             current = parent[head[current]]  # 현재 중경로 바로 위의 부모로 이동
#         for tail in reversed(tails):  # 새 값은 루트부터 아래 중경로로 차례로 전달
#             first = head[tail]  # 이번 구간이 속한 중경로 시작점
#             length = position[tail] - position[first] + 1  # 중경로 맨 위에서 tail까지 이동할 항목 수
#             path, after = split(roots[first], length)  # 이동할 중경로 앞부분과 그대로 둘 뒷부분 분리
#             middle, last = split(path, length - 1)  # 앞부분의 마지막 항목을 따로 꺼내기
#             outgoing = weight[last]  # 아래 중경로로 넘길 기존 마지막 값
#             weight[last] = item_sum[last] = incoming  # 꺼낸 한 항목의 값을 새로 들어온 값으로 교체
#             roots[first] = merge(merge(last, middle), after)  # 마지막 항목을 앞으로 옮겨 기존 값들을 한 칸씩 아래로 이동
#             change = incoming - outgoing  # 중경로 전체 합의 변화량
#             if change:  # 합이 실제로 바뀔 때만 펜윅 트리 갱신
#                 chain_total[first] += change  # 중경로의 전체 합 갱신
#                 index = position[first] + 1  # 합을 저장해 둔 중경로 시작점의 펜윅 위치
#                 while index <= n:  # 그 위치를 포함하는 모든 펜윅 구간 합 갱신
#                     bit[index] += change  # 중경로 합 변화량 추가
#                     index += index & -index  # 상위 펜윅 구간으로 이동
#             incoming = outgoing  # 다음 아래 중경로는 현재 구간에서 밀려난 값을 받음
#     merge = split = None  # 재귀 함수의 자기 참조를 끊어 반복 호출 때 큰 작업 배열이 즉시 해제되게 정리
#     return answer  # 부분 트리 합 쿼리들의 결과 반환

# 풀이 요약
# 부분 트리가 가장 큰 자식을 이어 중경로를 만들면 루트까지 지나가는 중경로는 O(log N)개. 중경로 우선 전위 순서에서 각 부분 트리는 연속 구간.
# 중경로마다 값 순서를 암묵적 트립으로 보관. 중력 쿼리는 중경로 앞부분의 마지막 항목을 앞으로 돌리고 값을 교체하며, 밀려난 값을 다음 중경로로 전달.
# 중경로 전체 합은 그 시작점의 전위 위치 한 칸에 펜윅 트리로 저장. 부분 트리 합은 그 구간의 중경로 전체 합들과 자기 중경로의 필요한 뒷부분을 합쳐 계산.
# 트리 순회는 반복문으로 처리하고, 의사난수 우선순위로 균형 잡힌 트립의 분할·병합에만 재귀 사용. 초기화 O(N), 쿼리당 기대 O(log²N), 작업 공간 O(N).

```
