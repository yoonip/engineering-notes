# 자체 창작 연습 03 · 작업 완료시간 합 최소화 
# 핵심 상태: elapsed는 현재 작업까지의 완료시각, answer는 모든 완료시각의 누적합이다.
# Python 3: 파일의 위에서 아래로 실행한다. 들여쓰기가 반복문·조건문·함수의 범위다.
# sys.stdin은 표준입력이다. read()는 EOF까지 읽으므로 파일 입력과 온라인 채점에 편하다.
# 터미널에 직접 붙여 넣을 때 read()가 대기하면 Windows에서 Ctrl+Z 후 Enter로 EOF를 보낸다.

import sys
data = list(map(int, sys.stdin.buffer.read().split()))
n = data[0]
# 헤더 N을 제외한 수행시간 n개를 별도 리스트로 담는다.
# 슬라이스 끝 n+1은 포함되지 않는다. 리스트 위치는 0부터 센다.
# 이후 a.sort()가 a 자체를 바꾸므로 원본 입력 순서가 필요하면 별도로 보관해야 한다.
a = data[1:n + 1]
# sort는 리스트를 제자리에서 오름차순으로 정렬한다.
# 반환값은 None이므로 a=a.sort()라고 쓰면 a를 잃는다.
# 짧은 작업을 먼저 처리하는 그리디의 근거는 큰 작업을 앞으로 바꾸면 완료시각 합이 증가하기 때문이다.
a.sort()
elapsed = answer = 0
# elapsed는 현재 작업이 끝나는 시각이고 answer는 완료시각들의 합이다.
# elapsed=answer=0은 두 변수를 모두 0으로 초기화한다.
# 정렬된 1,2,3,3,4에서 완료시각 1,3,6,9,13을 더해 32를 출력한다.
for x in a:
    elapsed += x
    answer += elapsed  # 이번 완료시각까지 answer에 누적한다.
print(answer)

# 복잡도: 일반적인 정렬 구현에서 시간 O(N log N), 공간 O(N). C 표준 qsort는 표준 자체가 최악 시간 복잡도를 보장하지 않는다.
# 마지막 경계 확인:
# - 완료시각과 대기시간을 구분한다. 이 문제는 자기 수행시간을 포함한다.
# - answer와 elapsed는 long long을 사용한다.
# - C qsort 비교함수에서 큰 정수의 단순 뺄셈은 일반적으로 오버플로 위험이 있다. 비교식을 쓴다.
