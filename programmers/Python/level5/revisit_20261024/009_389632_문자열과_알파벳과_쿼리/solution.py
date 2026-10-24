from array import array
from bisect import bisect_left, bisect_right


def solution(s, query):
    positions = [[] for _ in range(26)]
    occurrence = [0] * len(s)
    for index, char in enumerate(s):
        letter = ord(char) - 97
        occurrence[index] = len(positions[letter])
        positions[letter].append(index + 1)
    parent = array('i', [-1])
    owner = array('i', [0])
    count = array('i', [0])
    groups = [{}]
    boundaries = [[] for _ in range(26)]
    colors = [[] for _ in range(26)]

    def find(token):
        root = token
        while parent[root] >= 0:
            root = parent[root]
        while token != root:
            following = parent[token]
            parent[token] = root
            token = following
        return root

    def new_token(group, letter, amount):
        token = len(parent)
        parent.append(-1)
        owner.append(group)
        count.append(amount)
        groups[group][letter] = token
        return token

    def locate(position):
        letter = ord(s[position - 1]) - 97
        run = bisect_right(boundaries[letter], occurrence[position - 1]) - 1
        return owner[find(colors[letter][run])]

    for letter, points in enumerate(positions):
        if points:
            token = new_token(0, letter, len(points))
            boundaries[letter] = [0, len(points)]
            colors[letter] = [token]
    result = []
    for command in query:
        parts = command.split()
        kind = parts[0]
        if kind == '1':
            result.append('YES' if locate(int(parts[1])) == locate(int(parts[2])) else 'NO')
        elif kind == '2':
            source = locate(int(parts[1]))
            destination = len(groups)
            moved = {}
            groups.append(moved)
            old = groups[source]
            for char in set(parts[2]):
                letter = ord(char) - 97
                token = old.pop(letter, 0)
                if token:
                    token = find(token)
                    owner[token] = destination
                    moved[letter] = token
            if not old:
                old.clear()
        elif kind == '3':
            first, last = int(parts[1]), int(parts[2])
            destination = len(groups)
            moved = {}
            groups.append(moved)
            for char in set(parts[3]):
                letter = ord(char) - 97
                points = positions[letter]
                begin = bisect_left(points, first)
                end = bisect_right(points, last)
                if begin == end:
                    continue
                bounds = boundaries[letter]
                tags = colors[letter]
                left = bisect_right(bounds, begin) - 1
                right = bisect_left(bounds, end)
                amount = end - begin
                old_root = find(tags[left])
                if right == left + 1 and count[old_root] == amount:
                    old = groups[owner[old_root]]
                    del old[letter]
                    if not old:
                        old.clear()
                    owner[old_root] = destination
                    moved[letter] = old_root
                    continue
                new_bounds = []
                new_colors = []
                if bounds[left] < begin:
                    new_bounds.append(bounds[left])
                    new_colors.append(tags[left])
                token = new_token(destination, letter, amount)
                new_bounds.append(begin)
                new_colors.append(token)
                if end < bounds[right]:
                    new_bounds.append(end)
                    new_colors.append(tags[right - 1])
                for run in range(left, right):
                    root = find(tags[run])
                    removed = min(end, bounds[run + 1]) - max(begin, bounds[run])
                    count[root] -= removed
                    if count[root] == 0:
                        old = groups[owner[root]]
                        del old[letter]
                        if not old:
                            old.clear()
                bounds[left:right] = new_bounds
                tags[left:right] = new_colors
        elif kind == '4':
            a, b = locate(int(parts[1])), locate(int(parts[2]))
            if a == b:
                continue
            if a > b:
                a, b = b, a
            earlier, later = groups[a], groups[b]
            for letter, token in later.items():
                token = find(token)
                other = earlier.get(letter, 0)
                if other:
                    other = find(other)
                    if parent[other] > parent[token]:
                        other, token = token, other
                    if parent[other] == parent[token]:
                        parent[other] -= 1
                    parent[token] = other
                    count[other] += count[token]
                    token = other
                owner[token] = a
                earlier[letter] = token
            later.clear()
        else:
            for group in groups:
                if group:
                    output = []
                    for letter in sorted(group):
                        amount = count[find(group[letter])]
                        if amount:
                            output.extend((chr(letter + 97), str(amount)))
                    result.append(' '.join(output))
    return result

# 전체 코드 줄별 설명
# from array import array  # 토큰별 정수를 4바이트 배열에 저장해 Python 정수 리스트보다 메모리 절약
# from bisect import bisect_left, bisect_right  # 원래 번호와 연속 소속 구간의 경계를 이분 탐색
#
#
# def solution(s, query):  # 초기 문자열과 순서대로 수행할 쿼리를 받는 함수
#     positions = [[] for _ in range(26)]  # 알파벳별 원래 문자 번호를 모을 독립 리스트
#     occurrence = [0] * len(s)  # 고유 번호에서 같은 알파벳 안의 압축 순번으로 이동할 표
#     for index, char in enumerate(s):  # 원래 위치와 알파벳을 함께 읽기
#         letter = ord(char) - 97  # a~z를 0~25의 배열 번호로 변환
#         occurrence[index] = len(positions[letter])  # 이 문자가 알파벳 목록에서 차지할 순번
#         positions[letter].append(index + 1)  # 문제의 1기반 고유 번호를 오름차순으로 추가
#     parent = array('i', [-1])  # 양수는 DSU 부모, 음수는 대표의 병합 높이; 0번 토큰은 비워 둠
#     owner = array('i', [0])  # 대표 토큰이 속한 현재 문자열의 생성 번호
#     count = array('i', [0])  # 대표 토큰에 남아 있는 실제 문자 수
#     groups = [{}]  # 문자열별 알파벳→토큰 사전; 0번은 초기 문자열
#     boundaries = [[] for _ in range(26)]  # 알파벳별 압축 위치에서 연속 소속이 바뀌는 경계
#     colors = [[] for _ in range(26)]  # 각 경계 구간을 담당하는 토큰 번호
#
#     def find(token):  # 병합 전 색 번호를 현재 유효한 대표로 연결
#         root = token  # 대표를 찾기 시작할 토큰
#         while parent[root] >= 0:  # 음수 높이를 가진 대표가 나올 때까지 부모 탐색
#             root = parent[root]  # 다음 부모로 이동
#         while token != root:  # 지나온 경로를 대표에 바로 연결
#             following = parent[token]  # 기존 부모를 다음 순회용으로 보관
#             parent[token] = root  # 다음 조회를 줄이는 경로 압축
#             token = following  # 기존 부모에서 압축 계속
#         return root  # 현재 소속과 개수를 읽을 대표 번호
#
#     def new_token(group, letter, amount):  # 새 문자열의 한 알파벳을 담당할 토큰 생성
#         token = len(parent)  # 배열 끝에 붙일 새 토큰 번호
#         parent.append(-1)  # 처음에는 높이0인 단독 대표
#         owner.append(group)  # 새 토큰의 문자열 생성 번호
#         count.append(amount)  # 이번 토큰이 담당할 실제 문자 수
#         groups[group][letter] = token  # 문자열의 해당 알파벳 칸에 연결
#         return token  # 구간의 새 색으로 쓸 번호
#
#     def locate(position):  # 고유 번호가 현재 어느 문자열에 있는지 찾기
#         letter = ord(s[position - 1]) - 97  # 원래 알파벳은 이동해도 바뀌지 않음
#         run = bisect_right(boundaries[letter], occurrence[position - 1]) - 1  # 압축 순번을 포함하는 연속 소속 구간
#         return owner[find(colors[letter][run])]  # 구간 토큰의 현재 대표가 가리키는 문자열
#
#     for letter, points in enumerate(positions):  # 처음 등장한 알파벳의 전체 위치 준비
#         if points:  # 해당 알파벳이 실제로 있는 경우만
#             token = new_token(0, letter, len(points))  # 처음에는 알파벳 전체가 초기 문자열 소속
#             boundaries[letter] = [0, len(points)]  # 알파벳 전체를 한 구간으로 표시
#             colors[letter] = [token]  # 그 구간의 단일 소속 토큰
#     result = []  # 조회 응답과 마지막 알파벳 구성을 담을 배열
#     for command in query:  # 입력 순서대로 쿼리 실행
#         parts = command.split()  # 공백으로 쿼리 종류·번호·word 분리
#         kind = parts[0]  # 첫 문자열이 쿼리 종류
#         if kind == '1':  # 두 문자가 같은 문자열에 속하는지 조회
#             result.append('YES' if locate(int(parts[1])) == locate(int(parts[2])) else 'NO')  # 두 현재 소속의 비교 결과 추가
#         elif kind == '2':  # 한 문자열에서 선택 알파벳 전체를 이동
#             source = locate(int(parts[1]))  # x가 이동하더라도 원래 소속을 계속 사용할 수 있게 먼저 고정
#             destination = len(groups)  # 새 문자열의 생성 번호
#             moved = {}  # 새 문자열의 알파벳 토큰 사전
#             groups.append(moved)  # 빈 경우에도 생성 순서를 하나 소비
#             old = groups[source]  # 쿼리 시작 때 확정한 원래 문자열
#             for char in set(parts[2]):  # word 중복을 없애 같은 알파벳은 한 번만 처리
#                 letter = ord(char) - 97  # 선택 알파벳의 배열 번호
#                 token = old.pop(letter, 0)  # 원래 문자열에서 토큰을 꺼내고 없는 알파벳은 0
#                 if token:  # 실제로 이동할 알파벳이 있는 경우
#                     token = find(token)  # 병합 후 대표로 정규화
#                     owner[token] = destination  # 전체 알파벳 이동은 대표 소속만 변경
#                     moved[letter] = token  # 새 문자열에 같은 대표 연결
#             if not old:  # 모든 알파벳이 빠져 빈 문자열이 된 경우
#                 old.clear()  # 사전의 이전 저장 공간도 비우기
#         elif kind == '3':  # 원래 번호 범위에서 선택 알파벳을 모으기
#             first, last = int(parts[1]), int(parts[2])  # 포함할 고유 번호 양끝
#             destination = len(groups)  # 이번에 생성할 문자열 번호
#             moved = {}  # 모은 알파벳 토큰을 담을 새 사전
#             groups.append(moved)  # 이후 결과에서 지킬 생성 순서 등록
#             for char in set(parts[3]):  # 같은 선택 알파벳은 한 번만 이동
#                 letter = ord(char) - 97  # 알파벳의 위치 목록 선택
#                 points = positions[letter]  # 고유 번호가 정렬된 알파벳 전용 목록
#                 begin = bisect_left(points, first)  # first 이상인 첫 압축 순번
#                 end = bisect_right(points, last)  # last까지 포함한 끝 다음 순번
#                 if begin == end:  # 범위 안에 이 알파벳이 없는 경우
#                     continue  # 토큰이나 경계를 만들 필요 없음
#                 bounds = boundaries[letter]  # 현재 압축 위치의 소속 경계 목록
#                 tags = colors[letter]  # 경계 사이의 소속 토큰 목록
#                 left = bisect_right(bounds, begin) - 1  # 이동 범위 시작을 포함하는 구간
#                 right = bisect_left(bounds, end)  # 이동 끝 다음 경계의 삽입 위치
#                 amount = end - begin  # 이번에 모을 이 알파벳의 문자 수
#                 old_root = find(tags[left])  # 첫 겹친 구간의 현재 대표
#                 if right == left + 1 and count[old_root] == amount:  # 한 토큰 전체를 옮기는 경우 경계 재작성 생략
#                     old = groups[owner[old_root]]  # 그 토큰을 가진 원래 문자열
#                     del old[letter]  # 원래 문자열에서 이 알파벳 연결 제거
#                     if not old:  # 모든 알파벳이 사라진 경우
#                         old.clear()  # 빈 문자열의 사전 저장 공간 정리
#                     owner[old_root] = destination  # 토큰의 실제 소속만 새 문자열로 이동
#                     moved[letter] = old_root  # 새 문자열에 기존 토큰 재사용
#                     continue  # 문자 수와 위치 경계는 이미 맞으므로 다음 알파벳으로 이동
#                 new_bounds = []  # 교체 범위에 남길 새 경계
#                 new_colors = []  # 새 경계 사이를 담당할 토큰
#                 if bounds[left] < begin:  # 왼쪽 기존 구간 일부가 이동 범위 밖에 남는 경우
#                     new_bounds.append(bounds[left])  # 원래 왼쪽 시작 경계 유지
#                     new_colors.append(tags[left])  # 남은 왼쪽 부분은 이전 토큰 소속
#                 token = new_token(destination, letter, amount)  # 모을 문자 전체를 담을 새 대표 생성
#                 new_bounds.append(begin)  # 새 소속 구간의 시작
#                 new_colors.append(token)  # 이동 범위 전체는 새 토큰 소속
#                 if end < bounds[right]:  # 오른쪽 기존 구간 일부가 이동 범위 밖에 남는 경우
#                     new_bounds.append(end)  # 남은 오른쪽 부분의 시작 경계
#                     new_colors.append(tags[right - 1])  # 그 부분은 마지막 기존 토큰을 유지
#                 for run in range(left, right):  # 덮어쓰는 기존 소속 구간마다 실제 이동분 차감
#                     root = find(tags[run])  # 병합된 색은 대표 토큰에서 개수 관리
#                     removed = min(end, bounds[run + 1]) - max(begin, bounds[run])  # 이번 범위와 기존 구간의 교집합 길이
#                     count[root] -= removed  # 이전 문자열의 해당 알파벳 수에서 이동분 제외
#                     if count[root] == 0:  # 이 알파벳이 원래 문자열에서 모두 사라진 경우
#                         old = groups[owner[root]]  # 사라진 알파벳을 연결했던 문자열
#                         del old[letter]  # 빈 알파벳 토큰 연결 제거
#                         if not old:  # 문자열 자체도 비게 된 경우
#                             old.clear()  # 사전의 이전 저장 공간 비우기
#                 bounds[left:right] = new_bounds  # 슬라이스 대입으로 겹친 경계 구간 교체
#                 tags[left:right] = new_colors  # 같은 위치의 소속 토큰도 함께 교체
#         elif kind == '4':  # 두 현재 문자열을 하나로 합치기
#             a, b = locate(int(parts[1])), locate(int(parts[2]))  # 병합 전 두 고유 번호의 소속
#             if a == b:  # 이미 같은 문자열인 경우
#                 continue  # 병합 상태를 바꿀 필요 없음
#             if a > b:  # 늦게 생성된 번호가 앞에 온 경우
#                 a, b = b, a  # 먼저 생성된 문자열을 a로 통일
#             earlier, later = groups[a], groups[b]  # 남길 문자열과 사라질 문자열의 알파벳 사전
#             for letter, token in later.items():  # 늦은 문자열이 가진 알파벳만 순회
#                 token = find(token)  # 현재 대표 토큰 조회
#                 other = earlier.get(letter, 0)  # 남길 문자열에도 같은 알파벳이 있는지 확인
#                 if other:  # 같은 알파벳의 소속 색을 DSU로 병합
#                     other = find(other)  # 남길 문자열 쪽의 현재 대표
#                     if parent[other] > parent[token]:  # 음수 높이가 더 작은 쪽을 대표로 선택
#                         other, token = token, other  # 낮은 트리를 높은 트리 밑으로 붙일 준비
#                     if parent[other] == parent[token]:  # 두 트리 높이가 같은 경우
#                         parent[other] -= 1  # 병합 후 대표 높이를 한 단계 올림
#                     parent[token] = other  # 이전 색을 새 대표에 연결
#                     count[other] += count[token]  # 살아 있는 문자 수를 대표 한 곳에 합산
#                     token = other  # 병합된 대표로 정규화
#                 owner[token] = a  # DSU 대표와 별개로 문자열은 먼저 생성된 번호를 남김
#                 earlier[letter] = token  # 남길 문자열의 알파벳 대표 갱신
#             later.clear()  # 늦게 생성된 문자열은 사라짐
#         else:  # 마지막5번 쿼리에서 모든 문자열의 구성 출력
#             for group in groups:  # 사전 리스트 순서가 문자열 생성 순서
#                 if group:  # 빈 문자열은 출력에서 제외
#                     output = []  # 한 문자열의 알파벳·개수 항목
#                     for letter in sorted(group):  # a~z 순서로 알파벳 정렬
#                         amount = count[find(group[letter])]  # 현재 대표에 남은 실제 문자 수
#                         if amount:  # 남은 문자가 있는 알파벳만 출력
#                             output.extend((chr(letter + 97), str(amount)))  # 알파벳과 개수를 문자열 항목으로 추가
#                     result.append(' '.join(output))  # 공백 하나로 이어 한 결과 문자열 생성
#     return result  # 조회 응답과 최종 알파벳 구성을 순서대로 반환

# 풀이 요약
# 원래 알파벳·고유 번호는 바뀌지 않으므로 알파벳별 위치만 모아 압축. 같은 소속이 이어지는 구간을 경계 목록과 토큰 목록으로 관리.
# 토큰의 현재 문자열 번호와 실제 개수는 DSU 대표에 저장. 2번은 알파벳 전체 토큰의 소속만 옮기고, 4번은 같은 알파벳 토큰끼리 순위 병합.
# 3번은 번호 범위를 압축 위치로 바꿔 겹친 소속 구간의 개수를 차감한 뒤 새 토큰으로 교체. 한 토큰 전체가 이동하면 새 토큰·경계 교체 없이 기존 대표 재사용.
# 위치 조회는 bisect로 경계를 찾고 DSU 대표의 현재 소속 확인. word는 set으로 중복을 없애고, 먼저 생성된 문자열 번호와 DSU 대표 번호는 별개로 관리.
# 구간 경계를 찾는 이분 탐색과 슬라이스 교체는 Python 내장 연산을 활용해 재귀 호출을 줄임. 덮인 구간 순회는 생성·제거되는 경계 수에 비례.
# 목록 중간의 슬라이스 삽입·삭제는 뒤 원소 이동 비용이 있어, 최악 시간은 입력 분포에 영향을 받음. 큰 분할·병합·구간 이동 입력의 로컬 성능을 따로 확인.
# 토큰 정수는 array('i')로 저장해 누적 생성 토큰의 메모리를 줄이고, 최종 출력은 생성 번호·알파벳 순서로 비어 있지 않은 문자열만 반환.
