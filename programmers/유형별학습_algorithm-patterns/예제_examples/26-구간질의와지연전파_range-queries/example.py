import sys  # 전체 연산을 공백 단위로 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 정수 토큰 순회
n, q = next(tokens), next(tokens)  # 원소 수와 연산 수
values = [next(tokens) for _ in range(n)]  # 두 자료구조의 같은 초기 값
bit = [0] * (n + 1)  # Fenwick의 1기반 블록 합
tree = [0] * (4 * n)  # 세그먼트 구간 합
lazy = [0] * (4 * n)  # 자손으로 전달할 덧셈
def bit_add(index, delta):  # Fenwick 한 점 덧셈
    index += 1  # 내부 1기반 번호로 변환
    while index <= n:  # 해당 점이 들어가는 상위 블록 순회
        bit[index] += delta  # 블록 합 갱신
        index += index & -index  # 다음 상위 블록
def prefix(end):  # [0,end)의 접두 합
    result = 0  # 누적 블록 합
    while end:  # 겹치지 않는 블록을 뒤에서부터 합산
        result += bit[end]  # 현재 블록 추가
        end -= end & -end  # 처리한 블록 제거
    return result  # Fenwick 접두 결과
def build(node, left, right):  # 초기 구간 합 구축
    if right - left == 1:  # 리프 원소 확인
        tree[node] = values[left]  # 원소의 합 저장
        return  # 리프 구축 종료
    middle = (left + right) // 2  # 자식 경계
    build(node * 2, left, middle)  # 왼쪽 구축
    build(node * 2 + 1, middle, right)  # 오른쪽 구축
    tree[node] = tree[node * 2] + tree[node * 2 + 1]  # 부모 합 결합
def apply(node, length, delta):  # 전체 구간 갱신
    tree[node] += length * delta  # 자기 합에는 즉시 반영
    lazy[node] += delta  # 자손 전달은 미루기
def push(node, left, right):  # 자손 방문 전 태그 전달
    if not lazy[node] or right - left == 1:  # 전달 값이나 자식이 없는 상태
        return  # 전달 생략
    middle = (left + right) // 2  # 두 자식의 길이 계산
    apply(node * 2, middle - left, lazy[node])  # 왼쪽 반영
    apply(node * 2 + 1, right - middle, lazy[node])  # 오른쪽 반영
    lazy[node] = 0  # 부모 태그 해제
def range_add(node, left, right, first, last, delta):  # 반열린 구간 덧셈
    if last <= left or right <= first:  # 교차가 없는 구간
        return  # 갱신 제외
    if first <= left and right <= last:  # 완전히 포함된 구간
        apply(node, right - left, delta)  # 요약과 태그만 갱신
        return  # 자손 방문 생략
    push(node, left, right)  # 기존 조상 갱신 전달
    middle = (left + right) // 2  # 분할 경계
    range_add(node * 2, left, middle, first, last, delta)  # 왼쪽 갱신
    range_add(node * 2 + 1, middle, right, first, last, delta)  # 오른쪽 갱신
    tree[node] = tree[node * 2] + tree[node * 2 + 1]  # 부모 합 복구
def range_sum(node, left, right, first, last):  # 반열린 구간 합
    if last <= left or right <= first:  # 교차가 없는 구간
        return 0  # 합의 항등원
    if first <= left and right <= last:  # 완전히 포함된 요약
        return tree[node]  # 현재 구간 합 사용
    push(node, left, right)  # 읽을 자손에 갱신 전달
    middle = (left + right) // 2  # 분할 경계
    return range_sum(node * 2, left, middle, first, last) + range_sum(node * 2 + 1, middle, right, first, last)  # 부분 합 결합
for i, value in enumerate(values):  # 초기 Fenwick 원소 반영
    bit_add(i, value)  # 한 점씩 블록 합에 추가
build(1, 0, n)  # 초기 지연 트리 구축
for _ in range(q):  # 입력 순서의 연산 실행
    kind, left, right = next(tokens), next(tokens), next(tokens)  # 연산과 구간
    if kind == 0:  # 구간 덧셈
        delta = next(tokens)  # 더할 값
        for position in range(left, right):  # 비교용 Fenwick의 각 점 처리
            bit_add(position, delta)  # 기본 점 덧셈 반복
        if left < right:  # 빈 구간은 갱신 생략
            range_add(1, 0, n, left, right, delta)  # 지연 태그 구간 갱신
    else:  # 합 질의
        print(prefix(right) - prefix(left), range_sum(1, 0, n, left, right))  # 같은 결과 비교
