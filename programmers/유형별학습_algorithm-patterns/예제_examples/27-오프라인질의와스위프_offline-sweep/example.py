import sys  # 정수 입력 읽기
from bisect import bisect_right  # value 이하 좌표 개수 탐색
tokens = iter(map(int, sys.stdin.read().split()))  # 공백 토큰 순회
n, q = next(tokens), next(tokens)  # 점과 질의 수
points = [(next(tokens), next(tokens), i) for i in range(n)]  # 점 좌표와 동률 번호
queries = [(next(tokens), next(tokens), i) for i in range(q)]  # 원래 질의 번호
coordinates = sorted({y for x, y, i in points})  # y의 순서만 압축
points.sort(key=lambda event: (event[0], event[2]))  # 작은 x의 점부터 추가
queries.sort(key=lambda event: (event[0], event[2]))  # 질의도 같은 x순
bit = [0] * (len(coordinates) + 1)  # 활성 점의 빈도 트리
answer = [0] * q  # 원래 번호별 결과
cursor = 0  # 아직 추가하지 않은 점
def add(index):  # 1기반 압축 좌표 추가
    while index < len(bit):  # 해당 점의 상위 블록
        bit[index] += 1  # 점 한 개 추가
        index += index & -index  # 다음 상위 블록
def prefix(end):  # y 접두 개수
    result = 0  # 집계 결과
    while end:  # 접두사를 서로소 블록으로 분리
        result += bit[end]  # 블록 개수 추가
        end -= end & -end  # 마지막 블록 제거
    return result  # 조건에 맞는 점 개수
for x, y, identity in queries:  # 정렬한 질의 처리
    while cursor < n and points[cursor][0] <= x:  # 같은 x도 포함
        add(bisect_right(coordinates, points[cursor][1]))  # 점의 압축 순위에 추가
        cursor += 1  # 다음 점으로 이동
    answer[identity] = prefix(bisect_right(coordinates, y))  # y 이하 빈도와 원래 번호
for value in answer:  # 원래 질의 순서
    print(value)  # 한 답씩 출력
