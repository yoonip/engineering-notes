import heapq # 최솟값 힙 연산
import sys # 표준 입력 토큰 읽기
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수로 변환
n, k = data[:2] # 입력 개수와 남길 개수 분리
heap = [] # 현재까지 큰 값 K개를 보관할 최소 힙
for value in data[2:]: # 후보 값을 입력 순서대로 처리
    if len(heap) < k: # 아직 K개를 채우지 못한 경우
        heapq.heappush(heap, value) # 후보를 힙에 추가
    elif value > heap[0]: # 가장 작은 보관 값보다 큰 후보인지 확인
        heapq.heappop(heap) # 상위 K개에서 빠질 최솟값 제거
        heapq.heappush(heap, value) # 새 후보를 넣어 크기 유지
result = [heapq.heappop(heap) for _ in range(k)] # 최솟값부터 꺼내 오름차순 배열 구성
print(*reversed(result)) # 역순으로 큰 값부터 출력
