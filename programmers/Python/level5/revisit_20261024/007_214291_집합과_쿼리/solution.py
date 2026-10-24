def solution(n, queries):
    left = [0] * (n + 1)
    right = [0] * (n + 1)
    parent = [0] * (n + 1)
    entered = [0] * (n + 1)
    lazy = [-1] * (n + 1)
    priority = [0] * (n + 1)
    mask = (1 << 64) - 1
    for node in range(1, n + 1):
        value = (node + 0x9e3779b97f4a7c15) & mask
        value = ((value ^ (value >> 30)) * 0xbf58476d1ce4e5b9) & mask
        value = ((value ^ (value >> 27)) * 0x94d049bb133111eb) & mask
        priority[node] = value ^ (value >> 31)

    def push(node):
        when = lazy[node]
        if when != -1:
            a, b = left[node], right[node]
            if a:
                entered[a] = lazy[a] = when
            if b:
                entered[b] = lazy[b] = when
            lazy[node] = -1

    def merge(a, b):
        if not a:
            if b:
                parent[b] = 0
            return b
        if not b:
            parent[a] = 0
            return a
        if priority[a] < priority[b]:
            push(a)
            child = merge(right[a], b)
            right[a] = child; parent[child] = a
            parent[a] = 0
            return a
        push(b)
        child = merge(a, left[b])
        left[b] = child; parent[child] = b
        parent[b] = 0
        return b

    def split(node, bound):
        if not node:
            return 0, 0
        push(node)
        if entered[node] <= bound:
            a, b = split(right[node], bound)
            right[node] = a
            if a:
                parent[a] = node
            parent[node] = 0
            return node, b
        a, b = split(left[node], bound)
        left[node] = b
        if b:
            parent[b] = node
        parent[node] = 0
        return a, node

    def root_of(node):
        while parent[node]:
            node = parent[node]
        return node

    def locate(node):
        when = entered[node]
        while True:
            if lazy[node] > when:
                when = lazy[node]
            if not parent[node]:
                return node, when
            node = parent[node]

    answer = []
    for now, (kind, x, y) in enumerate(queries, 1):
        x += 1; y += 1
        if kind == 2:
            root, first = locate(x)
            _, last = locate(y)
            if first > last:
                continue
            before, tail = split(root, first - 1)
            middle, after = split(tail, last)
            entered[middle] = lazy[middle] = now
            merge(before, after)
        else:
            a, b = root_of(x), root_of(y)
            if kind == 1:
                if a != b:
                    entered[b] = lazy[b] = now
                    merge(a, b)
            else:
                answer.append('Yes' if a == b else 'No')
    return answer

# 전체 코드 줄별 설명
# def solution(n, queries):  # 집합 합치기·도착 시각 구간 분리·같은 집합 확인을 순서대로 처리
#     left = [0] * (n + 1)  # 각 원소보다 앞선 도착 시각 구간의 트립 자식
#     right = [0] * (n + 1)  # 각 원소보다 뒤인 도착 시각 구간의 트립 자식
#     parent = [0] * (n + 1)  # 원소가 현재 속한 집합 루트를 찾을 부모 포인터
#     entered = [0] * (n + 1)  # 원소가 현재 집합에 들어온 시각; 초기 원소는 모두 0
#     lazy = [-1] * (n + 1)  # 부분 집합 전체에 아직 내려보내지 않은 도착 시각 대입
#     priority = [0] * (n + 1)  # 집합을 나눠도 원소에 고정되는 트립 균형 우선순위
#     mask = (1 << 64) - 1  # 우선순위 혼합의 곱셈 결과를 64비트 안으로 제한
#     for node in range(1, n + 1):  # 원소마다 번호와 상관이 적은 고정 우선순위 생성
#         value = (node + 0x9e3779b97f4a7c15) & mask  # 원소 번호에 비트 혼합 시작 상수 더하기
#         value = ((value ^ (value >> 30)) * 0xbf58476d1ce4e5b9) & mask  # 상위·하위 비트를 첫 곱셈으로 섞기
#         value = ((value ^ (value >> 27)) * 0x94d049bb133111eb) & mask  # 두 번째 비트 혼합으로 인접 번호의 우선순위 분리
#         priority[node] = value ^ (value >> 31)  # 마지막 혼합 결과를 원소의 우선순위로 저장

#     def push(node):  # 자식을 바꾸기 전에 부분 집합의 일괄 도착 시각을 자손에게 전달
#         when = lazy[node]  # 현재 트립 루트에 남아 있는 지연 대입 시각
#         if when != -1:  # -1이면 전달할 도착 시각 대입이 없음
#             a, b = left[node], right[node]  # 같은 도착 시각을 넘겨줄 양쪽 자식
#             if a:  # 왼쪽 부분 집합이 존재하면
#                 entered[a] = lazy[a] = when  # 왼쪽 루트 값과 그 자손의 지연 대입을 함께 갱신
#             if b:  # 오른쪽 부분 집합이 존재하면
#                 entered[b] = lazy[b] = when  # 오른쪽 루트 값과 그 자손의 지연 대입도 갱신
#             lazy[node] = -1  # 자식에게 전달한 현재 루트의 지연 표시 해제

#     def merge(a, b):  # 도착 시각이 앞선 집합 a 뒤에 집합 b를 이어 붙이기
#         if not a:  # 앞부분이 비어 있으면 뒤 트리가 그대로 결과
#             if b:  # 뒤 트리도 빈 경우에는 빈 원소의 부모를 건드리지 않음
#                 parent[b] = 0  # 반환할 집합의 루트에는 부모가 없음
#             return b  # 뒤 부분 집합을 결과로 반환
#         if not b:  # 뒤부분이 비어 있으면 앞 트리만 남음
#             parent[a] = 0  # 앞 트리를 독립 집합 루트로 지정
#             return a  # 앞 부분 집합을 결과로 반환
#         if priority[a] < priority[b]:  # 더 작은 우선순위의 앞 루트를 유지하는 경우
#             push(a)  # 뒤 집합을 연결하기 전에 기존 자손의 도착 시각 확정
#             child = merge(right[a], b)  # a의 뒷부분과 새 뒤 집합을 합치기
#             right[a] = child; parent[child] = a  # 합친 구간을 오른쪽 자식으로 연결하고 부모 갱신
#             parent[a] = 0  # 반환되는 합집합 루트의 부모 해제
#             return a  # 앞 루트를 합친 집합의 루트로 반환
#         push(b)  # 앞 집합을 붙이기 전에 뒤 루트의 지연 시각 전달
#         child = merge(a, left[b])  # 앞 집합과 b의 앞부분을 합치기
#         left[b] = child; parent[child] = b  # 합친 구간을 왼쪽 자식으로 연결하고 부모 갱신
#         parent[b] = 0  # 반환되는 합집합 루트의 부모 해제
#         return b  # 뒤 루트를 합친 집합의 루트로 반환

#     def split(node, bound):  # 도착 시각이 bound 이하인 원소와 그 뒤 원소로 집합 분리
#         if not node:  # 빈 집합을 나누는 경우
#             return 0, 0  # 앞·뒤 부분 집합 모두 빈 결과
#         push(node)  # 도착 시각을 비교하거나 자식을 떼기 전에 지연 대입 전달
#         if entered[node] <= bound:  # 현재 원소가 앞부분에 들어가면
#             a, b = split(right[node], bound)  # 오른쪽 자식에서 앞부분에 더 포함될 원소 분리
#             right[node] = a  # 앞부분에 남는 오른쪽 구간만 현재 원소에 연결
#             if a:  # 남겨 둔 오른쪽 자식이 있으면
#                 parent[a] = node  # 자식의 새 부모를 현재 원소로 지정
#             parent[node] = 0  # 앞부분 루트는 독립 집합의 루트로 반환
#             return node, b  # 현재 원소를 포함한 앞부분과 뒤부분 반환
#         a, b = split(left[node], bound)  # 현재 원소가 뒤부분이면 왼쪽 자식에서 경계 찾기
#         left[node] = b  # 뒤부분에 남는 왼쪽 구간만 현재 원소에 연결
#         if b:  # 남겨 둔 왼쪽 자식이 있으면
#             parent[b] = node  # 자식의 새 부모를 현재 원소로 지정
#         parent[node] = 0  # 뒤부분 루트도 독립 집합의 루트로 반환
#         return a, node  # 앞부분과 현재 원소를 포함한 뒤부분 반환

#     def root_of(node):  # 시각이 필요 없는 쿼리에서 부모만 따라 현재 집합 찾기
#         while parent[node]:  # 부모가 없는 집합 루트까지 올라가기
#             node = parent[node]  # 현재 트립 부모로 한 단계 이동
#         return node  # 원소가 속한 집합의 루트 반환

#     def locate(node):  # 현재 집합 루트와 실제 도착 시각을 함께 찾기
#         when = entered[node]  # 현재 원소 자체에 기록된 도착 시각으로 시작
#         while True:  # 부모의 아직 전파하지 않은 대입 시각까지 확인
#             if lazy[node] > when:  # 시각은 단조 증가하므로 더 나중 대입이 현재 실제 시각
#                 when = lazy[node]  # 아직 내려오지 않은 도착 시각 반영
#             if not parent[node]:  # 더 올라갈 부모가 없으면 현재 집합 루트
#                 return node, when  # 집합 식별자와 원소의 실제 도착 시각 반환
#             node = parent[node]  # 다음 조상에 남은 지연 대입 확인

#     answer = []  # 세 번째 종류 쿼리의 Yes·No 결과만 저장
#     for now, (kind, x, y) in enumerate(queries, 1):  # 쿼리 순서를 새 집합의 도착 시각으로 사용
#         x += 1; y += 1  # 빈 트립 표시 0과 겹치지 않도록 원소 번호를 1부터 사용
#         if kind == 2:  # 같은 집합 안의 도착 시각 구간을 새 집합으로 분리
#             root, first = locate(x)  # 분리할 집합과 x가 들어온 실제 시각 찾기
#             _, last = locate(y)  # y가 들어온 실제 시각을 구간 끝으로 사용
#             if first > last:  # 시작 시각이 끝보다 늦으면 선택되는 원소가 없음
#                 continue  # 빈 구간 분리는 현재 집합을 바꾸지 않음
#             before, tail = split(root, first - 1)  # x보다 먼저 도착한 원소들을 앞부분으로 분리
#             middle, after = split(tail, last)  # x부터 y까지의 도착 시각 구간과 그 뒤 원소 분리
#             entered[middle] = lazy[middle] = now  # 새 집합의 모든 원소가 지금 함께 들어온 것으로 일괄 대입
#             merge(before, after)  # 선택 구간 밖 원소들은 원래 집합으로 다시 이어 붙이기
#         else:  # 집합 합치기와 같은 집합 확인에는 루트만 필요
#             a, b = root_of(x), root_of(y)  # 두 원소가 현재 속한 집합 식별
#             if kind == 1:  # y 집합 전체를 x 집합으로 이동
#                 if a != b:  # 이미 같은 집합이면 들어온 시각도 바꾸지 않음
#                     entered[b] = lazy[b] = now  # 이동할 y 집합 원소들의 도착 시각을 지금으로 지정
#                     merge(a, b)  # 기존 x 집합 뒤에 이동한 원소들을 함께 연결
#             else:  # 세 번째 종류는 두 집합의 동일 여부만 조회
#                 answer.append('Yes' if a == b else 'No')  # 두 루트가 같으면 같은 집합으로 판정
#     return answer  # 집합 확인 결과를 쿼리 발생 순서대로 반환

# 풀이 요약
# 각 집합을 현재 집합에 들어온 시각 순서의 트립으로 표현; 같은 시각의 원소들은 한 구간에 모여 있음
# 합치기는 이동하는 집합 전체의 시각을 현재 쿼리 번호로 바꾼 뒤 기존 집합 뒤에 연결
# 분리는 x의 도착 시각 이상 y의 도착 시각 이하인 구간을 두 번의 시각 분할로 떼고, 남은 앞뒤 구간을 다시 연결
# 이동한 묶음의 시각은 지연 대입으로 저장하고 부모 포인터로 각 원소의 현재 집합 루트를 확인
# 시각은 증가만 하므로 조상에 남은 지연 대입 중 가장 큰 값이 원소의 실제 도착 시각
# 원소 N개·쿼리 Q개에서 기대 시간 O(N+Q log N), 트립의 보조 공간 O(N); 반환 문자열 배열은 별도
