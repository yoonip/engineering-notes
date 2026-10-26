import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n = int(next(tokens))  # 검산 배열 길이
    values = [int(next(tokens)) for _ in range(n)]  # 작은 범위의 입력 배열
    slow = -10 ** 9  # 모든 허용 합보다 작은 초기값
    for left in range(n):  # 구간 시작점 전수 확인
        for right in range(left, n):  # 비어 있지 않은 끝점 확인
            total = 0  # 구간마다 합을 새로 계산
            for i in range(left, right + 1):  # 실제 구간의 원소 직접 순회
                total += values[i]  # 정의에 따른 합산
            slow = max(slow, total)  # 느린 기준의 최댓값
    current = fast = values[0]  # 빈 구간을 허용하지 않는 초기 상태
    for i in range(1, n):  # 복사 배열 없이 빠른 풀이의 한 번 순회
        value = values[i]  # 이번에 이어 붙일 원소
        current = max(value, current + value)  # 새로 시작하거나 직전 최적 구간 연장
        fast = max(fast, current)  # 전체 최대합 갱신
    print(slow, fast)  # 두 구현의 결과를 같은 줄에 출력

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
