import sys  # 공백 단위 표준 입력 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 정수 토큰 순회
n = next(tokens)  # 회의 수
meetings = [(next(tokens), next(tokens)) for _ in range(n)]  # 시작과 종료 저장
meetings.sort(key=lambda item: (item[1], item[0]))  # 종료순과 동률 시작순
count = 0  # 선택한 회의 수
finish = 0  # 직전 선택의 종료
for start, end in meetings:  # 정렬한 후보 순회
    if count == 0 or start >= finish:  # 겹치지 않는 회의만 선택
        finish = end  # 다음 선택의 시작 경계 갱신
        count += 1  # 선택 수 누적
print(count)  # 최대 회의 수 출력
