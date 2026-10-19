# 사용할 한 자리 숫자와 목표 정수를 받음.
def solution(N, number):
    # 중복은 집합으로 제거.
    values = [set() for _ in range(9)]
    # N 사용 횟수를 1~8 순서로 늘림.
    for count in range(1, 9):
        # 5,55,555처럼 붙인 숫자 추가.
        values[count].add(int(str(N) * count))
        # 전체 수식을 왼쪽과 오른쪽 두 부분으로 나누는 모든 사용 횟수 시도.
        for left_count in range(1, count):
            # 오른쪽 수식에 쓸 N의 개수.
            right_count = count - left_count
            # for로 왼쪽 수식의 가능한 결과 순회.
            for first in values[left_count]:
                # 오른쪽 수식의 가능한 결과 순회.
                for second in values[right_count]:
                    # 덧셈 결과 저장.
                    values[count].add(first + second)
                    # 순서가 다른 경우도 반복에서 포함됨.
                    values[count].add(first - second)
                    # 곱셈 결과 저장.
                    values[count].add(first * second)
                    # 0으로 나누는 연산 제외.
                    if second != 0:
                        # 음수 결과도 나머지를 버리는 규칙 적용.
                        values[count].add(int(first / second))
        # 목표 결과를 만들 수 있는지 검사.
        if number in values[count]:
            # 적은 횟수부터 확인했으므로 처음 발견한 횟수가 최소.
            return count
    # 8번까지 목표를 만들 수 없으면 -1 반환.
    return -1
