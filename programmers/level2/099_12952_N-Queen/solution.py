def solution(n):
    # 아래 n비트가 모두 1인 마스크로 유효 열 표시.
    full = (1 << n) - 1
    def search(columns, left, right):
        if columns == full:
            return 1
        # 현재 행에서 열·대각선 공격을 안 받는 열만 선택.
        available = full & ~(columns | left | right)
        count = 0
        while available:
            # 음수와 비트 AND를 취해 가장 오른쪽 1비트 하나 추출.
            position = available & -available
            available -= position
            # 다음 행의 대각선은 <<1·>>1로 한 열씩 옮겨 재귀 호출, +=로 경우의 수 누적.
            count += search(columns | position, (left | position) << 1, (right | position) >> 1)
        return count
    return search(0, 0, 0)
