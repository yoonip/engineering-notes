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
            middle = (left + right) // 2
            if target <= middle:
                node, right = node * 2, middle
            else:
                node, left = node * 2 + 1, middle + 1
        return owner[find(tree[node])]
    def assign(tree, node, left, right, begin, end, bucket, letter):
        tag = tree[node]
        if begin <= left and right <= end and tag != -1:
            old = find(tag)
            amount = right - left + 1
            counts[old] -= amount
            source = owner[old]
            totals[source] -= amount
            if counts[old] == 0:
                groups[source].pop(letter, None)
            if totals[source] == 0:
                groups[source].clear()
            tree[node] = bucket
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
#         index -= 1  # -=는 뺀 값 저장. 문자 번호를 0부터 시작하는 인덱스로 변환.
#         letter = letters[index]  # 원래 문자의 알파벳 번호 조회.
#         tree = trees[letter]  # 해당 알파벳의 위치별 버킷 구간 트리 선택.
#         node, left, right = 1, 0, len(positions[letter]) - 1  # 구간 트리 루트와 전체 알파벳 위치 범위 초기화.
#         target = ranks[index]  # 해당 알파벳 안에서 찾을 순번.
#         while tree[node] == -1:  # -1은 여러 버킷이 섞인 구간. 한 버킷인 구간까지 내려감.
#             middle = (left + right) // 2  # //는 정수 나눗셈. 구간 중간 위치.
#             if target <= middle:  # if는 조건문. 찾는 위치가 왼쪽 절반인지 확인.
#                 node, right = node * 2, middle  # 왼쪽 자식과 범위로 이동.
#             else:  # 오른쪽 절반에 위치한 경우.
#                 node, left = node * 2 + 1, middle + 1  # 오른쪽 자식과 범위로 이동.
#         return owner[find(tree[node])]  # 해당 구간 버킷의 대표를 찾아 소속 문자열 번호 반환.
#     def assign(tree, node, left, right, begin, end, bucket, letter):  # 알파벳 위치 범위의 문자를 새 버킷으로 옮기는 구간 갱신 함수.
#         tag = tree[node]  # 현재 구간이 단일 버킷이면 번호, 여러 버킷이면 -1.
#         if begin <= left and right <= end and tag != -1:  # and는 모두 참. 전체 구간이 이동 대상이고 단일 버킷인 경우.
#             old = find(tag)  # 기존 버킷의 대표 조회.
#             amount = right - left + 1  # 이동할 실제 문자 개수.
#             counts[old] -= amount  # 기존 알파벳 버킷의 문자 수 감소.
#             source = owner[old]  # 기존 버킷이 속한 문자열 번호 저장.
#             totals[source] -= amount  # 기존 문자열 전체 문자 수 감소. 0이면 마지막 출력에서 제외.
#             if counts[old] == 0:  # 해당 알파벳이 전부 이동했으면 비어 있는 버킷 연결을 정리.
#                 groups[source].pop(letter, None)  # pop은 항목 제거·반환. 더 이상 문자가 없는 알파벳 항목 제거.
#             if totals[source] == 0:  # 원래 문자열 전체가 비었는지 검사.
#                 groups[source].clear()  # clear로 빈 문자열의 딕셔너리 메모리도 정리.
#             tree[node] = bucket  # 구간 전체가 새 버킷 소속임을 한 번에 기록.
#             return  # 이 구간의 처리를 끝내고 호출한 함수로 복귀.
#         if tag != -1:  # 단일 버킷 구간의 일부만 옮기려면 자식으로 정보를 전달.
#             tree[node * 2] = tree[node * 2 + 1] = tag  # 연쇄 대입. 양쪽 자식에 현재 구간 소속을 복사.
#         middle = (left + right) // 2  # 양쪽 자식 구간의 경계 계산.
#         if begin <= middle:  # 이동 범위가 왼쪽 자식과 겹치는 경우.
#             assign(tree, node * 2, left, middle, begin, end, bucket, letter)  # 왼쪽 자식 구간을 재귀 갱신.
#         if end > middle:  # 이동 범위가 오른쪽 자식과 겹치는 경우.
#             assign(tree, node * 2 + 1, middle + 1, right, begin, end, bucket, letter)  # 오른쪽 자식 구간을 재귀 갱신.
#         a, b = tree[node * 2], tree[node * 2 + 1]  # 갱신된 양쪽 구간의 버킷 태그를 가져옴.
#         tree[node] = a if a == b else -1  # 조건 표현식. 소속 태그가 같으면 합치고 다르면 혼합 구간 표시.
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
# 알파벳별 구간 트리에는 문자들이 속한 버킷을 저장합니다. 3번은 구간 버킷을 덮어쓰고, 2번은 알파벳 버킷 전체의 소속만 바꿉니다.
# 4번은 같은 알파벳 버킷의 서로소 집합을 합칩니다. 이전 버킷을 참조하는 문자도 대표 검색으로 새 소속을 찾습니다. 비어 버린 문자열은 길이 0으로 제외합니다.
# 예: abacadae에서 1~4번의 a를 모으면 원래 문자열과 새 aa 문자열이 생깁니다. 알파벳 종류를 A=26, 쿼리 수 Q, 문자 수 N이라 하면 분할·덮어쓰기의 총 시간은 상각 O(A*Q*log N), 공간 O(N+A*Q).
# 