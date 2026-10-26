import argparse # 정상 검사와 잘못된 점 로봇 대조 선택
from collections import deque # 독립 BFS의 선입선출 큐
import heapq # A*의 최소 예상 비용 후보
import math # 유한성·기하 거리 검사
import sys # 실패 이유와 종료 코드 전달
EPS_M = 1e-12 # 접촉을 여유 있게 거절할 미터 단위 수치 허용값
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0)) # 대각선 없는 네 이웃
checks = planner_cases = found_paths = invalid_rejections = 0 # 실제 검사·계획·도달·입력 거절 집계
def require(condition, reason): # Python 최적화 옵션과 무관한 검사
    global checks # 실제 비교 수를 바깥 집계에 반영
    checks += 1 # 실행한 조건 수 증가
    if not condition: # 기대한 안전·길이 조건이 틀린 경우
        raise AssertionError(reason) # 조용한 통과 대신 검사 실패
def validate_map(grid, resolution, body_radius, margin): # 작은 실내 정적 지도의 입력 계약
    if not isinstance(grid, (list, tuple)) or not 1 <= len(grid) <= 20: # 빈 지도와 과도한 크기 거절
        raise ValueError('grid height1..20') # 허용 행 개수 명시
    if any(not isinstance(row, str) for row in grid): # 문자열 행만 허용
        raise ValueError('string grid rows') # 모호한 지도 표현 거절
    width = len(grid[0]) # 모든 행이 공유할 열 개수
    if not 1 <= width <= 20 or any(len(row) != width for row in grid): # 빈 행·비직사각형 지도 거절
        raise ValueError('rectangular width1..20') # 지도 형식 오류 분리
    if set(''.join(grid)) - {'.', '#', '?'}: # 빈칸·점유·미관측 이외의 셀 값 거절
        raise ValueError('unknown map symbol') # 임의 문자를 빈칸으로 취급하지 않기
    for value, lower, upper in ((resolution, 0.05, 10.0), (body_radius, 0.0, 10.0), (margin, 0.0, 10.0)): # 미터 단위 매개변수 범위
        if type(value) not in (int, float) or not math.isfinite(value) or not lower <= value <= upper: # NaN·무한대·음수 반경 차단
            raise ValueError('finite metric parameters') # 수치 입력 오류 반환
def validate_cell(cell, height, width): # 시작·목표를 배열에 접근하기 전에 확인
    if not isinstance(cell, tuple) or len(cell) != 2 or any(type(value) is not int for value in cell): # 정수 행·열 두 개만 허용
        raise ValueError('cell is integer(row,column)') # 실수·음성 인덱스의 암묵 변환 방지
    if not 0 <= cell[0] < height or not 0 <= cell[1] < width: # 지도 밖 시작·목표 거절
        raise ValueError('cell outside map') # 음수 인덱스가 반대편 셀을 가리키지 않기
def cell_center(cell, resolution): # 행0은 아래쪽이며 지도 원점은 왼쪽 아래
    row, col = cell # 저장 인덱스를 두 축으로 분리
    return (col + 0.5) * resolution, (row + 0.5) * resolution # 셀 중심의x·y 미터 좌표
def blocked_cells(grid, resolution, body_radius, margin): # 원형 차체를 점 중심으로 바꿀 이진 장애물 확장
    validate_map(grid, resolution, body_radius, margin) # 기하 계산 전에 지도와 단위 확인
    height, width = len(grid), len(grid[0]) # 지도 셀 개수
    radius = body_radius + margin + EPS_M # 차체·안전 여유·수치 접촉 여유 합산
    occupied = [(row, col) for row in range(height) for col in range(width) if grid[row][col] != '.'] # 미관측 셀도 점유 셀로 간주
    blocked = [[False] * width for _ in range(height)] # 중심을 둘 수 없는 위치의 결과
    for row in range(height): # 각 후보 중심의 충돌 검사
        for col in range(width): # 각 열의 중심 확인
            x, y = cell_center((row, col), resolution) # 후보 로봇 중심의 실제 좌표
            if min(x, y, width * resolution - x, height * resolution - y) <= radius: # 원형 차체가 지도 밖 또는 경계에 닿는 경우
                blocked[row][col] = True # 바깥을 돌아가는 가짜 경로 차단
                continue # 장애물 검사 없이 금지 확정
            for obstacle_row, obstacle_col in occupied: # 원래 점유 사각형을 하나씩 확인
                dx = max(abs(col - obstacle_col) * resolution - resolution / 2, 0.0) # 후보 중심에서 사각형까지의x 최소 거리
                dy = max(abs(row - obstacle_row) * resolution - resolution / 2, 0.0) # 사각형까지의y 최소 거리
                if dx * dx + dy * dy <= radius * radius: # 원과 사각형의 접촉도 충돌로 판정
                    blocked[row][col] = True # 차체가 들어갈 수 없는 중심 표시
                    break # 한 장애물 충돌이면 충분
    return blocked # 팽창한 이진 점유 지도 반환
def astar(blocked, start, goal): # 확장된 지도에서만 점 중심 경로 계획
    height, width = len(blocked), len(blocked[0]) # 그래프의 유효 범위
    validate_cell(start, height, width) # 시작 셀의 범위 확인
    validate_cell(goal, height, width) # 목표 셀의 범위 확인
    if blocked[start[0]][start[1]] or blocked[goal[0]][goal[1]]: # 차체가 놓일 수 없는 양 끝점
        return None # 시작과 목표가 같아도 충돌이면 실패
    def heuristic(cell): # 단위 간선의 남은 거리 하한
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1]) # 4연결의 Manhattan 최소 이동 수
    distances, parent = {start: 0}, {start: None} # 최단 이동 수와 경로 복원 정보
    candidates = [(heuristic(start), 0, start)] # f·g·행열 순서로 결정적인 최소 힙
    while candidates: # 도달 후보가 있는 동안 탐색
        _, distance, cell = heapq.heappop(candidates) # 예상 전체 길이가 작은 후보 선택
        if distance != distances[cell]: # 더 짧은 경로로 대체된 오래된 힙 항목
            continue # 같은 상태의 불필요한 재확장 생략
        if cell == goal: # 일관적 하한 아래 목표의 최단 길이 확정
            path, cursor = [], goal # 부모 연결을 거꾸로 따라갈 준비
            while cursor is not None: # 시작의 부모 표식까지 복원
                path.append(cursor) # 현재 셀 추가
                cursor = parent[cursor] # 한 단계 이전 셀
            path.reverse() # 시작부터 목표의 순서로 변경
            return path # 셀 중심 사이를 직선으로 이을 경로
        for dr, dc in DIRECTIONS: # 벽을 가로지르지 않는 네 이웃
            next_cell = cell[0] + dr, cell[1] + dc # 다음 중심의 행·열
            row, col = next_cell # 범위와 점유를 확인할 좌표
            if not 0 <= row < height or not 0 <= col < width or blocked[row][col]: # 지도 밖과 팽창 장애물 제외
                continue # 금지된 중심으로는 진행하지 않기
            next_distance = distance + 1 # 동일 길이의 한 셀 이동
            if next_distance < distances.get(next_cell, height * width + 1): # 더 짧은 경로만 상태 갱신
                distances[next_cell] = next_distance # 현재까지 최단 이동 수
                parent[next_cell] = cell # 실제 경로의 직전 셀 기록
                heapq.heappush(candidates, (next_distance + heuristic(next_cell), next_distance, next_cell)) # 갱신한 예상 비용으로 후보 추가
    return None # 연결된 안전 중심 경로가 없음
def plan(grid, resolution, body_radius, margin, start, goal): # 외부 입력에서 사용할 계획 진입점
    return astar(blocked_cells(grid, resolution, body_radius, margin), start, goal) # 차체 기하를 먼저 반영한 뒤 그래프 탐색
def oracle_blocked(grid, resolution, body_radius, margin): # 중심 차이식 대신 사각형 좌표 clamp로 독립 충돌 기준
    radius = body_radius + margin + EPS_M # 같은 접촉 거절 계약
    height, width = len(grid), len(grid[0]) # 독립 기준의 지도 크기
    result = [] # 행별 금지 중심 목록
    for row in range(height): # 각 행의 기준 생성
        flags = [] # 현재 행의 금지 여부
        for col in range(width): # 각 후보 중심 확인
            x, y = col * resolution + resolution / 2, row * resolution + resolution / 2 # 왼쪽 아래 셀 모서리에서 중심 계산
            collision = x <= radius or y <= radius or x + radius >= width * resolution or y + radius >= height * resolution # 차체의 네 바깥 끝이 경계를 넘거나 닿는지 검사
            for obstacle_row in range(height): # 모든 원래 장애물 사각형
                for obstacle_col in range(width): # 미관측과 점유 셀을 같은 기하로 처리
                    if grid[obstacle_row][obstacle_col] == '.': # 빈 사각형은 장애물이 아님
                        continue # 빈칸의 충돌 기준 생략
                    left, bottom = obstacle_col * resolution, obstacle_row * resolution # 점유 사각형의 실제 모서리
                    nearest_x = min(max(x, left), left + resolution) # 사각형에 가장 가까운x 좌표
                    nearest_y = min(max(y, bottom), bottom + resolution) # 사각형에 가장 가까운y 좌표
                    collision = collision or math.hypot(x - nearest_x, y - nearest_y) <= radius # clamp 점과의 실제 거리로 원 충돌 판정
            flags.append(collision) # 독립 중심 판정 저장
        result.append(flags) # 현재 행의 기준 완성
    return result # A*용 팽창 지도와 대조할 결과
def bfs_distance(blocked, start, goal): # 휴리스틱·힙·부모 사전이 없는 독립 최단 길이 기준
    height, width = len(blocked), len(blocked[0]) # 격자의 유효 크기
    if blocked[start[0]][start[1]] or blocked[goal[0]][goal[1]]: # 놓을 수 없는 시작·목표는 도달 불가
        return None # 동일한 점유 계약 유지
    queue, seen = deque([(start[0], start[1], 0)]), {start} # 거리가 증가하는 순서의 BFS
    while queue: # 아직 방문할 중심이 있는 동안 반복
        row, col, distance = queue.popleft() # 가장 이른 거리의 중심 꺼내기
        if (row, col) == goal: # 처음 도달한 목표의 최단 길이
            return distance # A*와 비교할 이동 수
        for dr, dc in ((-1, 0), (0, -1), (1, 0), (0, 1)): # 별도로 적은 네 방향 열거
            nr, nc = row + dr, col + dc # 다음 중심
            if 0 <= nr < height and 0 <= nc < width and not blocked[nr][nc] and (nr, nc) not in seen: # 경계·장애물·중복 방문 제거
                seen.add((nr, nc)) # 처음 도달한 거리 확정
                queue.append((nr, nc, distance + 1)) # 다음 거리로 확장
    return None # 연결된 중심이 더는 없음
def path_geometry_safe(grid, resolution, body_radius, margin, path): # 중심 사이 전체 선분의 별도 원·사각형 기하 검사
    if not path: # 검증할 실제 경로가 없는 경우
        return False # 빈 경로를 안전 경로라고 계산하지 않기
    height, width = len(grid), len(grid[0]) # 실제 지도 외곽 크기
    radius = body_radius + margin + EPS_M # 차체와 안전 여유의 원 반경
    centers = [cell_center(cell, resolution) for cell in path] # 전체 경로를 미터 좌표로 변환
    segments = [(centers[0], centers[0])] + list(zip(centers, centers[1:])) # 한 점 경로와 모든 직선 이동을 함께 포함
    for first, last in segments: # 원형 차체가 쓸고 지나가는 각 구간
        if first[0] != last[0] and first[1] != last[1]: # 대각선·임의 각도 선분은 이 모델에서 금지
            return False # 허용하지 않은 모서리 지름길 거절
        x0, x1 = sorted((first[0], last[0])) # 선분의x 구간
        y0, y1 = sorted((first[1], last[1])) # 선분의y 구간
        if min(x0, y0, width * resolution - x1, height * resolution - y1) <= radius: # 선분 전체의 차체가 지도 바깥에 닿는 경우
            return False # 지도 외부를 자유공간으로 가정하지 않기
        for row in range(height): # 원래 장애물 면적과 선분을 직접 대조
            for col in range(width): # 미관측 셀도 점유 면적으로 처리
                if grid[row][col] == '.': # 빈 셀은 충돌 대상 아님
                    continue # 빈 면적 생략
                left, bottom = col * resolution, row * resolution # 점유 셀의 모서리
                dx = max(left - x1, x0 - (left + resolution), 0.0) # 두x 구간 사이의 최소 간격
                dy = max(bottom - y1, y0 - (bottom + resolution), 0.0) # 두y 구간 사이의 최소 간격
                if math.hypot(dx, dy) <= radius: # 축 정렬 선분과 사각형의 거리가 원 반경 이하
                    return False # 중심만 통과하고 차체가 벽을 치는 경로 거절
    return True # 이 정적 기하 계약에서 모든 구간 통과
def compare_case(grid, resolution, radius, margin, start, goal): # 계획·지도 확장·선분 안전성을 교차 검사
    global planner_cases, found_paths # 실제 사례 집계 변경
    blocked = blocked_cells(grid, resolution, radius, margin) # 실제 계획에 사용할 금지 중심
    reference = oracle_blocked(grid, resolution, radius, margin) # 독립 clamp 기하 기준
    require(blocked == reference, 'inflation geometry') # 같은 잘못된 지도를 A*와BFS가 공유하지 않기
    path = plan(grid, resolution, radius, margin, start, goal) # 실제A* 계획 실행
    expected_steps = bfs_distance(reference, start, goal) # 별도BFS 최단 길이
    actual_steps = None if path is None else len(path) - 1 # 경로 없음과0길이를 구분
    require(actual_steps == expected_steps, 'A* versus independent BFS') # 도달 여부와 최단 이동 수 함께 비교
    planner_cases += 1 # 실제 계획 사례 수 증가
    if path is not None: # 경로가 존재할 때만 형태와 기하 검사
        require(path[0] == start and path[-1] == goal, 'path endpoints') # 시작·목표 누락 방지
        require(len(set(path)) == len(path), 'positive cost path has no loop') # 반복 셀을 포함한 불필요한 순환 거절
        for a, b in zip(path, path[1:]): # 모든 인접 이동 확인
            require(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1, 'four connected step') # 대각선과 셀 점프 금지
        require(path_geometry_safe(grid, resolution, radius, margin, path), 'swept circle clearance') # 원형 차체의 전체 이동 구간 대조
        found_paths += 1 # 실제 도달 경로 집계
    return path # 직접 예제의 출력에도 같은 경로 사용
def wall_map(open_rows): # 중앙 벽의 문 높이만 바꾸는 실내 지도
    rows = [] # 아래쪽 행부터 저장할 목록
    for row in range(9): # 세로9셀
        line = ['.'] * 9 # 가로9셀의 빈 공간
        if row not in open_rows: # 문이 아닌 중앙 위치
            line[4] = '#' # 한 셀 두께의 벽
        rows.append(''.join(line)) # 행0부터y가 증가하는 저장 순서
    return rows # 중앙 벽과 열린 문의 정적 지도
def main(): # 실내 원형 차체의 계획 예제와 독립 검사 실행
    global invalid_rejections # 입력 거절의 실제 집계
    parser = argparse.ArgumentParser() # 검사 전용 명령행 선택
    parser.add_argument('--negative-point-model', action='store_true') # 유한 반경을 무시하는 잘못된 모델 대조
    args = parser.parse_args() # 정상 또는 음성 대조 모드
    narrow, wide = wall_map({4}), wall_map({3, 4, 5}) # 한 셀 문과 세 셀 문
    start, goal, resolution = (4, 1), (4, 7), 0.5 # 민간 실내로봇의 셀 위치와m/cell
    try: # 검사 실패를 실제 종료 코드로 전달
        if args.negative_point_model: # 차체를 점으로 바꾸면 놓치는 경계 검증
            wrong_path = astar(blocked_cells(narrow, resolution, 0, 0), start, goal) # 잘못된0반경 모델의 경로
            correct_steps = bfs_distance(oracle_blocked(narrow, resolution, 0.20, 0.05), start, goal) # 실제 차체·여유 반경의 독립 기준
            wrong_steps = None if wrong_path is None else len(wrong_path) - 1 # 잘못된 모델의 경로 길이
            print(f'TRACE negative point_steps={wrong_steps} finite_body_steps={correct_steps}') # 모델 차이를 실제 값으로 기록
            require(wrong_steps == correct_steps, 'point model ignores finite body clearance') # 의도한 모델 오류에서 반드시 실패
        path = compare_case(narrow, resolution, 0.20, 0, start, goal) # 0.5m 문을 반경0.20m 원형 차체로 통과
        require(path is not None and len(path) - 1 == 6, 'narrow door small body') # 직접 계산한 직선6이동 기준
        print(f'TRACE narrow radius_m=0.20 margin_m=0.00 steps={len(path)-1} metres={(len(path)-1)*resolution:.3f}') # 실제 거리 단위 출력
        closed = compare_case(narrow, resolution, 0.20, 0.05, start, goal) # 반경과 여유 합0.25m가 양 벽에 닿는 경우
        require(closed is None, 'touching door is blocked') # 접촉도 충돌인 계약 확인
        print('TRACE narrow radius_m=0.20 margin_m=0.05 path=NONE') # 여유 확장으로 닫힌 통로 표시
        path = compare_case(wide, resolution, 0.35, 0, start, goal) # 1.5m 문은 더 큰 차체도 중심선으로 통과
        require(path is not None and len(path) - 1 == 6, 'wider door clearance') # 넓힌 문에서 다시 경로 존재
        print(f'TRACE wide radius_m=0.35 margin_m=0.00 steps={len(path)-1} metres={(len(path)-1)*resolution:.3f}') # 같은 셀 길이와 다른 차체 조건 출력
        boundaries = [ # 직접 정한 작은 지도·차체의 경계 사례
            (['.'], 0, (0, 0), (0, 0), 0), # 빈 한 셀의 시작과 목표가 같으면0이동
            (['.'], 0.25, (0, 0), (0, 0), None), # 차체가 한 셀 지도의 외곽에 닿으면 금지
            (['#'], 0, (0, 0), (0, 0), None), # 점유 시작은 동일 목표라도 거절
            (['?'], 0, (0, 0), (0, 0), None), # 미관측 시작도 점유로 처리
            (['.#', '#.'], 0, (0, 0), (1, 1), None), # 대각선 두 빈칸 사이의 모서리 통과 금지
            (['.#.', '.#.', '.#.'], 0, (1, 0), (1, 2), None), # 지도 바깥으로 벽을 우회하지 않기
            (['...', '...', '...'], 0, (0, 0), (2, 2), 4), # 빈 지도 모서리 사이의 Manhattan 거리
            (['...', '...', '...'], 0.25, (0, 1), (2, 1), None), # 외곽 접촉을 시작부터 차단
            (['...', '...', '...'], 0.1, (1, 1), (1, 1), 0), # 놓을 수 있는 원형 차체의 동일 시작목표
        ] # 9개 경계 사례 끝
        for grid, radius, first, last, expected in boundaries: # 직접 정한 경계 사례
            result = compare_case(grid, 0.5, radius, 0, first, last) # 독립 기하·BFS도 함께 검사
            require((None if result is None else len(result) - 1) == expected, 'hand checked boundary') # 손으로 정한 결과와 비교
        query_pairs = (((0, 0), (2, 2)), ((1, 1), (1, 1)), ((0, 1), (2, 1))) # 모서리·중앙·세로 통과의 세 질의
        for mask in range(1 << 9): # 3×3 지도의 모든512개 점유 패턴
            grid = [''.join('#' if (mask >> (3 * row + col)) & 1 else '.' for col in range(3)) for row in range(3)] # 행0이 아래인 작은 정적 지도 생성
            for radius in (0.0, 0.24, 0.25): # 점·반셀 직전·벽 접촉의 세 차체 반경
                for first, last in query_pairs: # 각 반경에서 독립 시작·목표 검사
                    compare_case(grid, 0.5, radius, 0, first, last) # 512×3×3=4608개 계획 비교
        invalid = [ # 정상 무경로와 구분할 잘못된13개 입력
            ([], 0.5, 0, 0, (0, 0), (0, 0)), # 빈 지도
            (['..', '.'], 0.5, 0, 0, (0, 0), (0, 0)), # 길이가 다른 행
            (['X'], 0.5, 0, 0, (0, 0), (0, 0)), # 정의되지 않은 셀 문자
            (['.'], 0.5, 0, 0, (-1, 0), (0, 0)), # 음수 시작 인덱스
            (['.'], 0.5, 0, 0, (0, 0), (1, 0)), # 지도 밖 목표
            (['.'], 0.5, 0, 0, (0.0, 0), (0, 0)), # 실수 셀 번호
            (['.'], 0, 0, 0, (0, 0), (0, 0)), # 0인 해상도
            (['.'], math.nan, 0, 0, (0, 0), (0, 0)), # NaN 해상도
            (['.'], 0.5, -0.1, 0, (0, 0), (0, 0)), # 음수 차체 반경
            (['.'], 0.5, math.inf, 0, (0, 0), (0, 0)), # 무한대 차체 반경
            (['.'], 0.5, 0, -0.1, (0, 0), (0, 0)), # 음수 안전 여유
            (['.'], 0.5, 0, math.inf, (0, 0), (0, 0)), # 무한대 안전 여유
            (['.'] * 21, 0.5, 0, 0, (0, 0), (0, 0)), # 허용 행 수 초과
        ] # 입력 계약 위반 목록 끝
        for parameters in invalid: # 잘못된 입력이 정상 무경로와 섞이지 않는지 확인
            rejected = False # 이번 요청의 명시적 거절 여부
            try: # 안전 진입점의 입력 계약 검사
                plan(*parameters) # 원래 매개변수로 실제 함수 호출
            except ValueError: # 문서화한 입력 오류만 기대
                rejected = True # 정상적인 입력 거절 기록
            require(rejected, 'reject invalid request') # 음수 인덱스·NaN 등의 조용한 수락 방지
            invalid_rejections += 1 # 실제 오류 요청 검사 수
        print(f'PASS grid-planning checks={checks} planner_cases={planner_cases} exhaustive_maps=512 oracle_cases=4608 found_paths={found_paths} invalid_rejections={invalid_rejections}') # 실제 로컬 검사 집계
        return 0 # 모든 정적 계획 비교가 맞은 결과
    except AssertionError as error: # 모델·경로·오라클 불일치 분리
        print(f'FAIL grid-planning {error}', file=sys.stderr) # 첫 실패 이유 기록
        return 1 # 기능 비교 실패를 프로세스 종료 코드로 전달
if __name__ == '__main__': # 스크립트로 실행할 때만 고정 검사를 시작
    raise SystemExit(main()) # 실제 검사 종료 코드 반환
