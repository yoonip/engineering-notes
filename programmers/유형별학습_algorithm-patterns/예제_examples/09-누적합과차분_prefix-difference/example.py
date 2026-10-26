import sys # 정수 토큰 입력
tokens = iter(map(int, sys.stdin.buffer.read().split())) # 입력을 차례로 읽을 반복자
n, q = next(tokens), next(tokens) # 배열 크기와 갱신 개수
values = [next(tokens) for _ in range(n)] # 원래 값 저장
diff, prefix = [0] * (n + 1), [0] * (n + 1) # 끝 경계까지 포함한 차분과 접두 합
for _ in range(q): # 각 구간 갱신을 두 경계에 기록
    left, right, delta = next(tokens), next(tokens), next(tokens) # 반열린 구간과 증가량
    diff[left] += delta # 시작 위치부터 증가량 적용
    diff[right] -= delta # 끝 위치부터 같은 증가량 취소
left, right = next(tokens), next(tokens) # 최종 구간 합의 경계
running = 0 # 현재 위치에 겹치는 증가량
for index in range(n): # 차분 복원과 접두 합 생성
    running += diff[index] # 새 경계의 증가·취소 누적
    values[index] += running # 현재 원소의 최종 값 계산
    prefix[index + 1] = prefix[index] + values[index] # 접두 합 한 칸 확장
print(*values) # 갱신이 끝난 배열 출력
print(prefix[right] - prefix[left]) # 두 접두 합 차이로 최종 구간 합 출력
