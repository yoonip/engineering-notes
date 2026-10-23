from bisect import bisect_left, bisect_right
from array import array

def solution(s, query):
    positions = [[] for _ in range(26)]
    letters, ranks = [], []
    for index, char in enumerate(s):
        letter = ord(char) - 97
        letters.append(letter)
        ranks.append(len(positions[letter]))
        positions[letter].append(index + 1)
    parent, owner, counts = array('i'), array('i'), array('i')
    rank = bytearray()
    groups, totals = [{}], [len(s)]
    trees = [None] * 26
    runs = [{} for _ in range(26)]
    def new_bucket(group, letter):
        bucket = len(parent)
        parent.append(bucket)
        rank.append(0)
        owner.append(group)
        counts.append(0)
        groups[group][letter] = bucket
        return bucket
    def find(bucket):
        while parent[bucket] != bucket:
            parent[bucket] = parent[parent[bucket]]
            bucket = parent[bucket]
        return bucket
    def locate(index):
        index -= 1
        letter = letters[index]
        tree = trees[letter]
        node, left, right = 1, 0, len(positions[letter]) - 1
        target = ranks[index]
        while tree[node] == -1:
            if right - left < 64:
                ends, buckets = runs[letter][node]
                return owner[find(buckets[bisect_right(ends, target)])]
            middle = (left + right) // 2
            if target <= middle:
                node, right = node * 2, middle
            else:
                node, left = node * 2 + 1, middle + 1
        return owner[find(tree[node])]
    def deduct(tag, amount, letter):
        old = find(tag)
        counts[old] -= amount
        source = owner[old]
        totals[source] -= amount
        if counts[old] == 0:
            groups[source].pop(letter, None)
        if totals[source] == 0:
            groups[source].clear()
    def assign(tree, node, left, right, begin, end, bucket, letter):
        tag = tree[node]
        if begin <= left and right <= end and tag != -1:
            deduct(tag, right - left + 1, letter)
            tree[node] = bucket
            return
        if right - left < 64:
            low, high = max(begin, left), min(end, right) + 1
            if tag != -1:
                deduct(tag, high - low, letter)
                ends, buckets = [], []
                if left < low:
                    ends.append(low); buckets.append(tag)
                ends.append(high); buckets.append(bucket)
                if high <= right:
                    ends.append(right + 1); buckets.append(tag)
            else:
                ends, buckets = runs[letter][node]
                first, last = bisect_right(ends, low), bisect_left(ends, high)
                previous = ends[first - 1] if first else left
                first_start = previous
                for index in range(first, last + 1):
                    amount = min(high, ends[index]) - max(low, previous)
                    deduct(buckets[index], amount, letter)
                    previous = ends[index]
                new_ends, new_buckets = ends[:first], buckets[:first]
                if first_start < low:
                    new_ends.append(low); new_buckets.append(buckets[first])
                new_ends.append(high); new_buckets.append(bucket)
                if high < ends[last]:
                    new_ends.append(ends[last]); new_buckets.append(buckets[last])
                new_ends.extend(ends[last + 1:]); new_buckets.extend(buckets[last + 1:])
                ends, buckets = new_ends, new_buckets
            runs[letter][node] = ends, buckets
            tree[node] = buckets[0] if len(buckets) == 1 else -1
            return
        if tag != -1:
            tree[node * 2] = tree[node * 2 + 1] = tag
        middle = (left + right) // 2
        if begin <= middle:
            assign(tree, node * 2, left, middle, begin, end, bucket, letter)
        if end > middle:
            assign(tree, node * 2 + 1, middle + 1, right, begin, end, bucket, letter)
        a, b = tree[node * 2], tree[node * 2 + 1]
        tree[node] = a if a == b else -1
    for letter in range(26):
        size = len(positions[letter])
        if size:
            bucket = new_bucket(0, letter)
            counts[bucket] = size
            trees[letter] = [bucket] * (4 * size)
    result = []
    for command in query:
        parts = command.split()
        kind = parts[0]
        if kind == '1':
            result.append('YES' if locate(int(parts[1])) == locate(int(parts[2])) else 'NO')
        elif kind == '2':
            source = locate(int(parts[1]))
            destination = len(groups)
            groups.append({})
            totals.append(0)
            for char in set(parts[2]):
                letter = ord(char) - 97
                bucket = groups[source].pop(letter, None)
                if bucket is not None:
                    bucket = find(bucket)
                    groups[destination][letter] = bucket
                    owner[bucket] = destination
                    totals[source] -= counts[bucket]
                    totals[destination] += counts[bucket]
        elif kind == '3':
            begin, end = int(parts[1]), int(parts[2])
            destination = len(groups)
            groups.append({})
            totals.append(0)
            for char in set(parts[3]):
                letter = ord(char) - 97
                locations = positions[letter]
                low, high = bisect_left(locations, begin), bisect_right(locations, end)
                if low < high:
                    bucket = new_bucket(destination, letter)
                    assign(trees[letter], 1, 0, len(locations) - 1, low, high - 1, bucket, letter)
                    counts[bucket] = high - low
                    totals[destination] += high - low
        elif kind == '4':
            a, b = locate(int(parts[1])), locate(int(parts[2]))
            if a == b:
                continue
            if a > b:
                a, b = b, a
            for letter, bucket in groups[b].items():
                bucket = find(bucket)
                if letter in groups[a]:
                    other = find(groups[a][letter])
                    if rank[other] < rank[bucket]:
                        other, bucket = bucket, other
                    parent[bucket] = other
                    counts[other] += counts[bucket]
                    if rank[other] == rank[bucket]:
                        rank[other] += 1
                    bucket = other
                groups[a][letter] = bucket
                owner[bucket] = a
            groups[b].clear()
            totals[a] += totals[b]
            totals[b] = 0
        else:
            for group, total in enumerate(totals):
                if total:
                    output = []
                    for letter in sorted(groups[group]):
                        amount = counts[find(groups[group][letter])]
                        if amount:
                            output.extend((chr(letter + 97), str(amount)))
                    result.append(' '.join(output))
    return result

# 전체 코드 줄별 설명
# from bisect import bisect_left, bisect_right  # from A import B는 모듈에서 함수 가져오기. bisect는 정렬된 위치 목록을 이진 탐색.
# from array import array  # array는 같은 형식의 숫자를 연속 메모리에 저장하는 압축 배열 자료구조.
# 
# def solution(s, query):  # def는 함수 정의. 초기 문자열과 쿼리 목록을 입력받음.
#     positions = [[] for _ in range(26)]  # 리스트 내포. 알파벳별 원래 문자 번호를 오름차순 저장.
#     letters, ranks = [], []  # []는 빈 리스트. 각 문자의 알파벳 번호와 같은 알파벳 내 순번 저장.
#     for index, char in enumerate(s):  # enumerate는 (인덱스, 값) 제공. 초기 문자열 순회.
#         letter = ord(char) - 97  # ord는 문자 코드 반환. a~z를 0~25로 변환.
#         letters.append(letter)  # append는 끝에 추가. 현재 문자의 알파벳 번호 저장.
#         ranks.append(len(positions[letter]))  # len은 길이. 해당 알파벳 목록에서 현재 문자의 순번 저장.
#         positions[letter].append(index + 1)  # 문제의 문자 번호는 1부터 시작하므로 1을 더해 위치 등록.
#     parent, owner, counts = array('i'), array('i'), array('i')  # array('i')는 정수 압축 배열. 버킷별 부모·소속 문자열·문자 수를 저장.
#     rank = bytearray()  # bytearray는 1바이트 정수 배열. 작은 병합 순위를 저장해 메모리 절약.
#     groups, totals = [{}], [len(s)]  # {}는 딕셔너리. 문자열별 알파벳 버킷과 전체 문자 수 저장. 문자열 번호는 생성 순서.
#     trees = [None] * 26  # 알파벳별 구간 트리 저장. None은 해당 알파벳이 없다는 표시.
#     runs = [{} for _ in range(26)]  # 작은 말단 구간은 정렬된 경계·버킷 목록으로 저장하여 문자 단위 재귀를 생략.
#     def new_bucket(group, letter):  # 특정 문자열·알파벳의 새 버킷을 만드는 내부 함수.
#         bucket = len(parent)  # 다음 버킷 번호는 현재 버킷 개수.
#         parent.append(bucket)  # 처음에는 자기 자신을 루트로 하는 서로소 집합.
#         rank.append(0)  # 병합 트리의 순위 초기화.
#         owner.append(group)  # 버킷이 속한 문자열 번호 저장.
#         counts.append(0)  # 버킷 문자 수 초기화.
#         groups[group][letter] = bucket  # 문자열의 해당 알파벳에 버킷 연결.
#         return bucket  # 생성한 버킷 번호 반환.
#     def find(bucket):  # 서로소 집합의 대표 버킷을 찾는 함수.
#         while parent[bucket] != bucket:  # while은 조건 반복. 대표는 부모가 자기 자신인 버킷.
#             parent[bucket] = parent[parent[bucket]]  # 부모를 조부모로 바꾸는 경로 압축으로 다음 검색 단축.
#             bucket = parent[bucket]  # 위쪽 대표 후보로 이동.
#         return bucket  # 대표 버킷 반환.
#     def locate(index):  # 원래 문자 번호가 현재 어느 문자열에 속하는지 조회.
#         index -= 1  # -=는 뺀 값 저장. 1부터 시작하는 번호를 인덱스로 변환.
#         letter = letters[index]  # 원래 문자의 알파벳 번호 조회.
#         tree = trees[letter]  # 해당 알파벳 구간 트리 선택.
#         node, left, right = 1, 0, len(positions[letter]) - 1  # 루트와 전체 알파벳 순번 범위 초기화.
#         target = ranks[index]  # 해당 알파벳 안에서 찾을 순번.
#         while tree[node] == -1:  # -1은 여러 버킷이 섞인 구간. 단일 소속 구간까지 탐색.
#             if right - left < 64:  # if는 조건문. 64칸 이하 구간은 내부 경계 목록을 직접 검색.
#                 ends, buckets = runs[letter][node]  # 말단 구간의 끝 경계와 소속 버킷 목록 조회.
#                 return owner[find(buckets[bisect_right(ends, target)])]  # bisect_right로 목표를 포함하는 경계를 찾아 대표 소속 반환.
#             middle = (left + right) // 2  # //는 정수 나눗셈. 구간 중간 계산.
#             if target <= middle:  # 찾는 위치가 왼쪽 절반이면 실행.
#                 node, right = node * 2, middle  # 왼쪽 자식과 범위로 이동.
#             else:  # 오른쪽 절반이면 실행.
#                 node, left = node * 2 + 1, middle + 1  # 오른쪽 자식과 범위로 이동.
#         return owner[find(tree[node])]  # 단일 구간 버킷의 대표 문자열 반환.
#     def deduct(tag, amount, letter):  # 기존 소속에서 이동할 문자의 개수를 차감하는 내부 함수.
#         old = find(tag)  # 경로 압축으로 대표 버킷 조회.
#         counts[old] -= amount  # 기존 알파벳 버킷 문자 수 감소.
#         source = owner[old]  # 기존 소속 문자열 번호.
#         totals[source] -= amount  # 기존 문자열 전체 길이 감소.
#         if counts[old] == 0:  # 해당 알파벳이 전부 이동한 경우.
#             groups[source].pop(letter, None)  # pop은 키 제거·반환. 비어 버린 알파벳 슬롯 정리.
#         if totals[source] == 0:  # 문자열 전체가 빈 경우.
#             groups[source].clear()  # clear는 딕셔너리의 항목과 사용 공간을 정리.
#     def assign(tree, node, left, right, begin, end, bucket, letter):  # 번호 범위의 해당 알파벳을 새 버킷으로 이동.
#         tag = tree[node]  # 단일 버킷 번호 또는 혼합 구간 표시 -1 조회.
#         if begin <= left and right <= end and tag != -1:  # and는 모두 참. 단일 구간 전체 이동이면 한 번에 처리.
#             deduct(tag, right - left + 1, letter)  # 기존 소속 문자 수를 구간 크기만큼 차감.
#             tree[node] = bucket  # 전체 구간을 새 버킷에 연결.
#             return  # 현재 함수 호출 종료.
#         if right - left < 64:  # 작은 구간은 재귀로 더 쪼개지 않고 경계 목록을 수정.
#             low, high = max(begin, left), min(end, right) + 1  # max·min으로 실제 겹치는 구간 계산. high는 끝 다음 위치.
#             if tag != -1:  # 기존에 한 버킷으로 채워져 있던 작은 구간인 경우.
#                 deduct(tag, high - low, letter)  # 겹치는 문자 수만 기존 버킷에서 차감.
#                 ends, buckets = [], []  # []는 빈 리스트. 수정 후의 경계·버킷 목록 생성.
#                 if left < low:  # 이동 범위 왼쪽에 원래 소속을 유지하는 칸이 있는 경우.
#                     ends.append(low); buckets.append(tag)  # append는 끝에 추가. 왼쪽 잔여 구간 등록.
#                 ends.append(high); buckets.append(bucket)  # 새 소속으로 이동한 구간 등록.
#                 if high <= right:  # 오른쪽에도 원래 소속을 유지하는 칸이 있는 경우.
#                     ends.append(right + 1); buckets.append(tag)  # 오른쪽 잔여 구간 등록.
#             else:  # 기존에 여러 소속이 섞인 작은 구간인 경우.
#                 ends, buckets = runs[letter][node]  # 정렬된 기존 경계와 소속 버킷 목록 조회.
#                 first, last = bisect_right(ends, low), bisect_left(ends, high)  # 이진 탐색으로 겹치는 첫·마지막 구간 번호 계산.
#                 previous = ends[first - 1] if first else left  # 첫 겹침 구간의 시작 경계. 조건 표현식으로 왼쪽 끝 처리.
#                 first_start = previous  # 왼쪽 잔여 구간이 있는지 판단할 원래 시작 경계 저장.
#                 for index in range(first, last + 1):  # 겹치는 구간들만 순회. 바깥의 다른 소속 구간은 순회하지 않음.
#                     amount = min(high, ends[index]) - max(low, previous)  # 기존 구간과 이동 범위가 겹치는 문자 수 계산.
#                     deduct(buckets[index], amount, letter)  # 각 구간의 원래 문자열에서 이동 문자 수 차감.
#                     previous = ends[index]  # 다음 기존 구간의 시작 경계로 이동.
#                 new_ends, new_buckets = ends[:first], buckets[:first]  # 슬라이스는 새 리스트를 생성. 영향 없는 왼쪽 구간들을 복사.
#                 if first_start < low:  # 첫 겹침 구간의 왼쪽 일부가 남는 경우.
#                     new_ends.append(low); new_buckets.append(buckets[first])  # 원래 소속을 유지할 왼쪽 잔여 구간 추가.
#                 new_ends.append(high); new_buckets.append(bucket)  # 이동한 전체 구간을 하나의 새 버킷 구간으로 대체.
#                 if high < ends[last]:  # 마지막 겹침 구간의 오른쪽 일부가 남는 경우.
#                     new_ends.append(ends[last]); new_buckets.append(buckets[last])  # 원래 소속의 오른쪽 잔여 구간 추가.
#                 new_ends.extend(ends[last + 1:]); new_buckets.extend(buckets[last + 1:])  # extend는 여러 원소를 이어 붙임. 영향 없는 오른쪽 구간 보존.
#                 ends, buckets = new_ends, new_buckets  # 수정된 경계 목록으로 교체.
#             runs[letter][node] = ends, buckets  # 두 목록을 튜플로 묶어 말단 구간에 저장.
#             tree[node] = buckets[0] if len(buckets) == 1 else -1  # 한 소속만 남으면 단일 태그로 압축, 아니면 혼합 표시.
#             return  # 작은 구간 처리를 마치고 더 깊은 재귀는 생략.
#         if tag != -1:  # 큰 단일 구간의 일부만 이동할 때 실행.
#             tree[node * 2] = tree[node * 2 + 1] = tag  # 현재 소속 태그를 양쪽 자식에 전달.
#         middle = (left + right) // 2  # 자식 구간의 경계 계산.
#         if begin <= middle:  # 왼쪽 자식과 이동 범위가 겹치는 경우.
#             assign(tree, node * 2, left, middle, begin, end, bucket, letter)  # 왼쪽 구간 재귀 갱신.
#         if end > middle:  # 오른쪽 자식과 이동 범위가 겹치는 경우.
#             assign(tree, node * 2 + 1, middle + 1, right, begin, end, bucket, letter)  # 오른쪽 구간 재귀 갱신.
#         a, b = tree[node * 2], tree[node * 2 + 1]  # 갱신된 자식들의 소속 태그 조회.
#         tree[node] = a if a == b else -1  # 두 소속이 같으면 압축하고 다르면 혼합 구간 표시.
#     for letter in range(26):  # range(26)은 0~25 알파벳 번호 순회.
#         size = len(positions[letter])  # 해당 알파벳의 실제 문자 개수.
#         if size:  # 이 알파벳이 존재하면 초기 버킷과 트리 생성.
#             bucket = new_bucket(0, letter)  # 처음에는 모든 문자가 0번 문자열 소속.
#             counts[bucket] = size  # 알파벳 버킷의 초기 문자 수 저장.
#             trees[letter] = [bucket] * (4 * size)  # 구간 트리용 배열. 처음에는 전체 구간이 한 버킷.
#     result = []  # 쿼리 조회 결과를 담을 빈 리스트.
#     for command in query:  # 주어진 쿼리를 순서대로 처리.
#         parts = command.split()  # split은 공백 기준으로 문자열을 나눈 리스트 반환.
#         kind = parts[0]  # 쿼리 종류를 나타내는 첫 문자열 선택.
#         if kind == '1':  # ==는 같음 비교. 두 문자의 문자열 소속 조회.
#             result.append('YES' if locate(int(parts[1])) == locate(int(parts[2])) else 'NO')  # int는 정수 변환. 같은 문자열이면 YES, 아니면 NO 추가.
#         elif kind == '2':  # elif는 다음 조건 검사. 한 문자열에서 지정 알파벳들을 분리.
#             source = locate(int(parts[1]))  # 기준 문자가 속한 문자열 번호 조회.
#             destination = len(groups)  # 새 문자열의 생성 순서 번호 부여.
#             groups.append({})  # 새 문자열의 알파벳 버킷 목록 초기화.
#             totals.append(0)  # 새 문자열 길이 초기화.
#             for char in set(parts[2]):  # set은 중복 없는 집합. 같은 알파벳이 여러 번 주어져도 한 번 처리.
#                 letter = ord(char) - 97  # 알파벳을 0~25 번호로 변환.
#                 bucket = groups[source].pop(letter, None)  # pop은 딕셔너리 항목 제거·반환. 없으면 None 반환.
#                 if bucket is not None:  # is not None은 실제 버킷이 존재함을 검사.
#                     bucket = find(bucket)  # 현재 대표 버킷 조회.
#                     groups[destination][letter] = bucket  # 알파벳 버킷 전체를 새 문자열로 이동.
#                     owner[bucket] = destination  # 대표의 소속만 바꾸면 그 버킷의 모든 문자가 함께 이동.
#                     totals[source] -= counts[bucket]  # 원래 문자열 길이 감소.
#                     totals[destination] += counts[bucket]  # +=는 더한 값 저장. 새 문자열 길이 증가.
#         elif kind == '3':  # 번호 구간과 알파벳 조건을 만족하는 모든 문자를 새 문자열로 이동.
#             begin, end = int(parts[1]), int(parts[2])  # 문자 번호 구간을 두 정수로 변환.
#             destination = len(groups)  # 새 문자열 생성 순서 번호.
#             groups.append({})  # 새 문자열의 알파벳 버킷 딕셔너리 생성.
#             totals.append(0)  # 새 문자열의 문자 수 초기화.
#             for char in set(parts[3]):  # 옮길 알파벳들을 중복 없이 순회.
#                 letter = ord(char) - 97  # 알파벳 번호 계산.
#                 locations = positions[letter]  # 해당 알파벳의 원래 문자 번호 정렬 목록.
#                 low, high = bisect_left(locations, begin), bisect_right(locations, end)  # 이진 탐색으로 번호 범위에 속하는 순번 구간을 구함. high는 끝 다음 위치.
#                 if low < high:  # 이동할 문자가 실제로 있으면 실행.
#                     bucket = new_bucket(destination, letter)  # 이 알파벳을 모을 새 버킷 생성.
#                     assign(trees[letter], 1, 0, len(locations) - 1, low, high - 1, bucket, letter)  # 범위에 포함된 모든 소속 문자열에서 해당 문자들을 새 버킷으로 이동.
#                     counts[bucket] = high - low  # 새 버킷의 문자 수 저장.
#                     totals[destination] += high - low  # 새 문자열 전체 길이에 이동 문자 수 추가.
#         elif kind == '4':  # 두 문자가 속한 문자열 병합.
#             a, b = locate(int(parts[1])), locate(int(parts[2]))  # 병합할 두 문자열 번호 조회.
#             if a == b:  # 이미 같은 문자열이면 병합할 필요 없음.
#                 continue  # continue는 이번 쿼리를 끝내고 다음 쿼리 처리.
#             if a > b:  # 나중에 생성된 문자열 번호가 앞에 있으면 교환.
#                 a, b = b, a  # 동시 대입으로 번호를 교환. 더 먼저 생성된 a를 유지.
#             for letter, bucket in groups[b].items():  # items는 (키, 값) 쌍 제공. 사라질 문자열의 알파벳 버킷 순회.
#                 bucket = find(bucket)  # 병합할 버킷의 대표 조회.
#                 if letter in groups[a]:  # in은 딕셔너리 키 포함 검사. 먼저 생성된 문자열에도 같은 알파벳이 있는 경우.
#                     other = find(groups[a][letter])  # 기존 알파벳 버킷의 대표 조회.
#                     if rank[other] < rank[bucket]:  # 서로소 집합의 높이를 줄이기 위해 낮은 순위 대표를 아래에 붙임.
#                         other, bucket = bucket, other  # 순위가 높은 대표가 other가 되도록 교환.
#                     parent[bucket] = other  # 대표 버킷들을 병합. 구간 트리의 옛 버킷 번호는 find를 통해 새 대표로 연결됨.
#                     counts[other] += counts[bucket]  # 알파벳 문자 수 합산.
#                     if rank[other] == rank[bucket]:  # 같은 순위끼리 합치면 새 대표의 순위가 하나 증가.
#                         rank[other] += 1  # 병합 순위 증가.
#                     bucket = other  # 병합 결과 대표를 현재 버킷으로 지정.
#                 groups[a][letter] = bucket  # 유지되는 문자열의 알파벳 대표를 저장.
#                 owner[bucket] = a  # 대표 버킷의 소속 문자열을 먼저 생성된 문자열로 설정.
#             groups[b].clear()  # clear는 딕셔너리의 모든 항목 제거. 사라진 문자열의 목록 비움.
#             totals[a] += totals[b]  # 두 문자열의 전체 길이 합산.
#             totals[b] = 0  # 나중에 생성된 문자열은 사라졌으므로 길이 0.
#         else:  # 마지막 5번 쿼리. 남아 있는 문자열의 알파벳 구성 출력.
#             for group, total in enumerate(totals):  # 생성 순서대로 문자열 번호와 길이 순회.
#                 if total:  # 길이가 0인 사라진 문자열은 제외.
#                     output = []  # 이번 문자열의 알파벳·개수 조각 목록 초기화.
#                     for letter in sorted(groups[group]):  # sorted는 알파벳 번호 키를 오름차순 정렬.
#                         amount = counts[find(groups[group][letter])]  # 해당 알파벳 대표의 실제 문자 수 조회.
#                         if amount:  # 범위 이동 후 문자 수가 0이 된 버킷은 출력하지 않음.
#                             output.extend((chr(letter + 97), str(amount)))  # chr은 코드→문자, str은 문자열 변환. extend로 두 출력 항목 추가.
#                     result.append(' '.join(output))  # join은 문자열 사이에 공백을 넣어 합침. 완성한 알파벳 구성 추가.
#     return result  # return으로 1번·5번 쿼리 결과를 순서대로 반환.

# 풀이 요약
# 첫 번째 Python 풀이와 같은 알파벳별 버킷·서로소 집합 구조를 사용하되, 작은 구간은 경계 목록과 이진 탐색으로 처리합니다.
# 말단 64칸을 문자 단위로 재귀 분할하지 않아 함수 호출을 줄이고, 슬라이스·이진 탐색의 빠른 내부 구현을 활용합니다. 첫 Python 코드는 solution_v1.py로 보존했습니다.
# 2번은 버킷 소속 변경, 3번은 범위 소속 덮어쓰기, 4번은 버킷 병합입니다. 문자열 생성 순서와 실제 집합 대표를 따로 관리합니다.
# 