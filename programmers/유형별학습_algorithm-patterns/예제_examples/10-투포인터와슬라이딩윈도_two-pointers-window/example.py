import sys # 정수 토큰 입력
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수로 변환
n, target = data[:2] # 배열 길이와 목표 합 분리
values = data[2:] # 양수 원소 배열
left, total, best = 0, 0, n + 1 # 창의 시작·합·미발견 표식
for right, value in enumerate(values): # 오른쪽 끝을 순서대로 확장
    total += value # 새 원소를 현재 창에 포함
    while total >= target: # 목표를 만족하는 동안 창 축소
        best = min(best, right - left + 1) # 현재 유효 길이로 답 갱신
        total -= values[left] # 빠질 왼쪽 원소의 값 제거
        left += 1 # 왼쪽 경계 한 칸 전진
print(0 if best == n + 1 else best) # 최소 길이 또는 미발견0 출력
