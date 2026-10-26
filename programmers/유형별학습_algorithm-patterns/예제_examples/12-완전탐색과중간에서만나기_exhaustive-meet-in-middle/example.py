from bisect import bisect_left, bisect_right # 같은 보완 합의 양쪽 경계 검색
import sys # 정수 토큰 입력
data = list(map(int, sys.stdin.buffer.read().split())) # 입력을 정수로 변환
n, target = data[:2] # 원소 수와 목표 합
values = data[2:] # 위치별 원소 값
left_sums, right_sums = [0], [0] # 양쪽 빈 부분집합의 합
for value in values[:n // 2]: # 왼쪽 절반의 원소를 하나씩 반영
    left_sums += [total + value for total in left_sums] # 확장 전 각 선택에 이번 원소를 넣는 경우 추가
for value in values[n // 2:]: # 오른쪽 절반의 원소를 하나씩 반영
    right_sums += [total + value for total in right_sums] # 이번 원소를 넣는 오른쪽 선택 추가
right_sums.sort() # 같은 부분합을 연속 위치로 모으기
answer = 0 # 목표 합을 만드는 부분집합 수
for left in left_sums: # 왼쪽 선택마다 보완 합 검색
    need = target - left # 오른쪽에서 필요한 합
    answer += bisect_right(right_sums, need) - bisect_left(right_sums, need) # 같은 값의 전체 개수 누적
print(answer) # 목표 합의 부분집합 수 출력
