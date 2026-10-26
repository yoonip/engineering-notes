import sys  # 표준 입력 전체를 토큰으로 읽기

def main():  # 입력 한 건을 계산하고 결과 출력
    tokens = iter(sys.stdin.read().split())  # 공백과 줄바꿈을 같은 구분자로 처리
    n = int(next(tokens))  # 배열 길이
    initial = [int(next(tokens)) for _ in range(n)]  # 초기 배열
    target = [int(next(tokens)) for _ in range(n)]  # 목표 배열
    deficit = [b - a for a, b in zip(initial, target)]  # 위치별 필요한 증가량
    total = sum(deficit)  # 한 연산마다 2 줄일 전체 부족량
    if min(deficit) < 0 or total % 2 or 2 * max(deficit) > total:  # 감소 불가·홀짝·짝짓기 조건 검사
        print("IMPOSSIBLE")  # 목표에 도달할 수 없는 경우
        return  # 구성을 시작하지 않고 종료
    steps = total // 2  # 필요한 증가 연산 수
    print("POSSIBLE", steps)  # 연산 수를 포함한 결과 머리
    for _ in range(steps):  # 가장 큰 두 부족량을 반복해서 줄이기
        first = second = -1  # 서로 다른 두 후보 위치
        for i in range(n):  # 작은 인덱스부터 동률 처리
            if first == -1 or deficit[i] > deficit[first]:  # 더 큰 부족량 발견
                second, first = first, i  # 기존 첫 후보를 두 번째로 이동
            elif second == -1 or deficit[i] > deficit[second]:  # 두 번째로 큰 부족량 확인
                second = i  # 두 번째 위치 갱신
        deficit[first] -= 1  # 첫 위치를 실제로 1 올린 효과
        deficit[second] -= 1  # 둘째 위치를 실제로 1 올린 효과
        print(first, second)  # 선택한 연산 출력

if __name__ == "__main__":  # 직접 실행할 때만 예제 시작
    main()  # 표준 입력 한 건 처리
