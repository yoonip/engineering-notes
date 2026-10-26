import sys # 정수 토큰 입력
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수로 변환
n, values = data[0], data[1:] # 원소 수와 배열 분리
buffer = [0] * n # 재귀 호출이 공유할 병합 버퍼
def sort_range(left, right): # 반열린 구간을 정렬하는 재귀 함수
    if right - left <= 1: # 빈 구간이나 원소 하나인 경우
        return # 더 나눌 필요 없이 종료
    middle = left + (right - left) // 2 # 두 절반의 경계 계산
    sort_range(left, middle) # 왼쪽 절반 정렬
    sort_range(middle, right) # 오른쪽 절반 정렬
    i, j, out = left, middle, left # 양쪽 읽기 위치와 버퍼 쓰기 위치
    while i < middle and j < right: # 양쪽 모두 남아 있는 동안 비교
        if values[i] <= values[j]: # 같으면 왼쪽을 먼저 선택
            buffer[out] = values[i] # 왼쪽 값을 결과에 배치
            i += 1 # 왼쪽 읽기 위치 전진
        else: # 오른쪽 값이 더 작은 경우
            buffer[out] = values[j] # 오른쪽 값을 결과에 배치
            j += 1 # 오른쪽 읽기 위치 전진
        out += 1 # 병합 결과의 다음 위치로 이동
    while i < middle: # 왼쪽에 남은 원소 복사
        buffer[out] = values[i] # 다음 왼쪽 원소 배치
        i, out = i + 1, out + 1 # 읽기와 쓰기 위치 전진
    while j < right: # 오른쪽에 남은 원소 복사
        buffer[out] = values[j] # 다음 오른쪽 원소 배치
        j, out = j + 1, out + 1 # 읽기와 쓰기 위치 전진
    for position in range(left, right): # 완성된 구간을 원래 배열에 반영
        values[position] = buffer[position] # 현재 위치의 정렬 결과 복사
sort_range(0, n) # 전체 반열린 구간 정렬
print(*values) # 정렬 결과 또는 빈 줄 출력
