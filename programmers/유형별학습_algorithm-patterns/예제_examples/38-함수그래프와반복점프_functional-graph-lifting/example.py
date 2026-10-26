import sys  # 후속 정점과 질의 입력
tokens = iter(map(int, sys.stdin.read().split()))  # 공백 정수 순회
n, q = next(tokens), next(tokens)  # 정점 수와 질의 수
jump = [[next(tokens) for _ in range(n)]]  # 한 단계 전이
for bit in range(1, 20):  # 두 배 길이의 표
    previous = jump[-1]  # 직전 층의 이동
    jump.append([previous[previous[v]] for v in range(n)])  # 두 절반의 합성
for _ in range(q):  # 각 시작점 질의
    vertex, steps = next(tokens), next(tokens)  # 현재 정점과 남은 단계
    bit = 0  # 낮은 비트부터 확인
    while steps:  # 남은 단계의 이진수
        if steps & 1:  # 현재 길이의 이동 선택
            vertex = jump[bit][vertex]  # 갱신된 현재 정점에서 출발
        steps >>= 1  # 처리한 자리 제거
        bit += 1  # 다음 이동 길이
    print(vertex)  # 최종 정점 출력
