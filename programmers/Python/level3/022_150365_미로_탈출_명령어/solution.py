# 격자 크기·출발 행열·목표 행열·정확한 이동 횟수 입력.
def solution(n, m, x, y, r, c, k):
    # 장애물이 없는 격자의 최단거리인 맨해튼 거리.
    distance = abs(x - r) + abs(y - c)
    # 너무 멀거나 남는 이동 수가 홀수이면 불가능.
    if distance > k or (k - distance) % 2:
        # return으로 불가능 문자열을 반환하고 종료.
        return 'impossible'
    # () 튜플로 사전순 d·l·r·u와 행·열 변화량 저장.
    directions = (('d', 1, 0), ('l', 0, -1), ('r', 0, 1), ('u', -1, 0))
    # []는 이동 문자들을 모을 빈 리스트.
    answer = []
    # 정확히 k번 이동.
    for step in range(k):
        # 이번 한 칸 이동 뒤 남은 횟수.
        remaining = k - step - 1
        # for로 방향을 사전순 확인하며 세 값을 언패킹.
        for letter, dr, dc in directions:
            # 이 방향으로 갔을 때 새 행·열 계산.
            nx, ny = x + dr, y + dc
            # 격자 밖이면 제외.
            if not (1 <= nx <= n and 1 <= ny <= m):
                # continue는 다음 방향으로 진행.
                continue
            # 새 위치에서 목표까지 필요한 최소 이동 수.
            needed = abs(nx - r) + abs(ny - c)
            # 남은 횟수 안에서 도착하고 왕복으로 남는 짝수 횟수를 채울 수 있는지 검사.
            if needed <= remaining and (remaining - needed) % 2 == 0:
                # 가능한 방향 중 사전순 첫 방향을 확정하는 그리디.
                answer.append(letter)
                # 현재 위치를 새 위치로 동시에 갱신.
                x, y = nx, ny
                break
    # 빈 문자열의 join으로 이동 문자들을 결합해 반환.
    return ''.join(answer)
