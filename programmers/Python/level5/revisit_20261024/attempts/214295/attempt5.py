

def solution(n, m, tests):
    low_u, high_u, low_v, high_v = 0, n + m, -m, n
    for x, y, distance, flag in tests:
        if flag:
            u, v = x + y, x - y
            low_u, high_u = max(low_u, u - distance), min(high_u, u + distance)
            low_v, high_v = max(low_v, v - distance), min(high_v, v + distance)
    if low_u > high_u or low_v > high_v:
        return 0
    events, coordinates = [], [low_v, high_v + 1]
    for x, y, distance, flag in tests:
        if flag:
            continue
        u, v = x + y, x - y
        first_u, last_u = max(low_u, u - distance), min(high_u, u + distance)
        first_v, last_v = max(low_v, v - distance), min(high_v, v + distance)
        if first_u <= last_u and first_v <= last_v:
            end_v = last_v + 1
            events.append((first_u, first_v, end_v, 1))
            events.append((last_u + 1, first_v, end_v, -1))
            coordinates.extend((first_v, end_v))
    coordinates = sorted(set(coordinates))
    events.sort()
    coordinate_index = {value: number for number, value in enumerate(coordinates)}
    for index, (u, first, last, change) in enumerate(events):
        events[index] = (u, coordinate_index[first], coordinate_index[last], change)
    del coordinate_index
    leaves, base = len(coordinates) - 1, 1
    while base < leaves:
        base *= 2
    size = base * 2
    cover = [0] * size
    statistics = [0] * size
    count_mask = (1 << 32) - 1
    for leaf in range(leaves):
        low, high = coordinates[leaf], coordinates[leaf + 1] - 1
        even = high // 2 - (low + 1) // 2 + 1
        odd = high - low + 1 - even
        moment = high * high // 4 - (low - 1) * (low - 1) // 4
        statistics[base + leaf] = (moment << 64) + (odd << 32) + even
    for node in range(base - 1, 0, -1):
        statistics[node] = statistics[node * 2] + statistics[node * 2 + 1]
    full_statistics = statistics[base:base + leaves]

    def update(node, left, right, first, last, change):
        if first <= left and right <= last:
            cover[node] += change
        else:
            middle = (left + right) // 2
            if first < middle:
                update(node * 2, left, middle, first, last, change)
            if last > middle:
                update(node * 2 + 1, middle, right, first, last, change)
        if cover[node]:
            statistics[node] = 0
        elif node < base:
            statistics[node] = statistics[node * 2] + statistics[node * 2 + 1]
        else:
            statistics[node] = full_statistics[node - base]

    def prefix(bound):
        if bound < low_v:
            return 0
        if bound >= high_v:
            return statistics[1]
        total = 0
        node, left, right = 1, 0, base
        while node < base:
            if cover[node]:
                return total
            middle = (left + right) // 2
            cut = coordinates[middle] if middle < leaves else high_v + 1
            if bound < cut:
                node *= 2; right = middle
            else:
                a = node * 2
                total += statistics[a]
                node = a + 1; left = middle
        if not cover[node]:
            low = coordinates[left]
            even = bound // 2 - (low + 1) // 2 + 1
            odd = bound - low + 1 - even
            moment = bound * bound // 4 - (low - 1) * (low - 1) // 4
            total += (moment << 64) + (odd << 32) + even
        return total

    def count_slab(left_u, right_u):
        if left_u > right_u or statistics[1] == 0:
            return 0
        first_v = max(low_v, -right_u, left_u - 2 * m)
        last_v = min(high_v, right_u, 2 * n - left_u)
        if first_v > last_v:
            return 0
        if left_u == right_u:
            difference = prefix(last_v) - prefix(first_v - 1)
            shift = 32 if left_u & 1 else 0
            return (difference >> shift) & count_mask
        boundaries = sorted((first_v, last_v + 1, -left_u, left_u + 1, right_u - 2 * m, 2 * n - right_u + 1))
        previous = prefix(first_v - 1)
        result = 0
        for index in range(5):
            low, high = max(first_v, boundaries[index]), min(last_v, boundaries[index + 1] - 1)
            if low > high:
                continue
            lower_a = -1 if low < -left_u else 1 if low > left_u else 0
            lower_b = 0 if lower_a else left_u
            upper_a = 1 if low < right_u - 2 * m else -1 if low > 2 * n - right_u else 0
            upper_b = 2 * m if upper_a == 1 else 2 * n if upper_a == -1 else right_u
            current = prefix(high)
            difference = current - previous
            even = difference & count_mask
            odd = (difference >> 32) & count_mask
            moment = difference >> 64
            constant_even = upper_b // 2 - (lower_b + 1) // 2 + 1
            constant_odd = (upper_b + upper_a - 1) // 2 - (lower_b + lower_a) // 2 + 1
            result += (upper_a - lower_a) * moment + constant_even * even + constant_odd * odd
            previous = current
        return result

    answer, current_u, index = 0, low_u, 0
    while index < len(events):
        next_u = events[index][0]
        answer += count_slab(current_u, next_u - 1)
        while index < len(events) and events[index][0] == next_u:
            _, a, b, change = events[index]
            update(1, 0, base, a, b, change)
            index += 1
        current_u = next_u
    answer += count_slab(current_u, high_u)
    del update
    return answer




# 전체 코드 줄별 설명


# def solution(n, m, tests):  # 모든 주행 기록과 격자 경계를 만족하는 정수 표지판 위치 수 계산
#     low_u, high_u, low_v, high_v = 0, n + m, -m, n  # U=X+Y, V=X−Y에서 원래 격자가 들어가는 바깥 상자
#     for x, y, distance, flag in tests:  # 성공 기록들의 맨해튼 공을 먼저 교집합
#         if flag:  # 성공 기록은 표지판이 거리 이내라는 조건
#             u, v = x + y, x - y  # 기록 출발점의 변환 좌표
#             low_u, high_u = max(low_u, u - distance), min(high_u, u + distance)  # 성공 기록이 허용하는 U 범위로 줄이기
#             low_v, high_v = max(low_v, v - distance), min(high_v, v + distance)  # 성공 기록이 허용하는 V 범위로 줄이기
#     if low_u > high_u or low_v > high_v:  # 성공 기록부터 양립할 수 없는 경우 확인
#         return 0  # 교집합이 비었으면 가능한 좌표가 없음
#     events, coordinates = [], [low_v, high_v + 1]  # 실패 사각형의 U 증감 이벤트와 정수 V 구간 경계
#     for x, y, distance, flag in tests:  # 실패 기록 중 성공 후보 상자와 겹치는 제외 영역 추출
#         if flag:  # 성공 기록은 이미 교집합에 반영된 상태
#             continue  # 실패 덮임 이벤트에는 넣지 않음
#         u, v = x + y, x - y  # 실패 기록의 출발점을 변환한 중심 좌표
#         first_u, last_u = max(low_u, u - distance), min(high_u, u + distance)  # 실패 U 범위를 성공 후보 상자 안으로 자르기
#         first_v, last_v = max(low_v, v - distance), min(high_v, v + distance)  # 실패 V 범위를 성공 후보 상자 안으로 자르기
#         if first_u <= last_u and first_v <= last_v:  # 성공 후보와 겹치는 실패 사각형만 처리
#             end_v = last_v + 1  # 정수 V의 포함 구간을 반열린 구간으로 바꿀 끝 다음 경계
#             events.append((first_u, first_v, end_v, 1))  # 실패 U 시작부터 해당 V 구간의 덮임 추가
#             events.append((last_u + 1, first_v, end_v, -1))  # 실패 U 끝 다음 정수에서 같은 덮임 제거
#             coordinates.extend((first_v, end_v))  # 덮임이 바뀌는 V 경계를 압축 목록에 추가
#     coordinates = sorted(set(coordinates))  # 서로 다른 V 경계를 오름차순으로 압축
#     events.sort()  # U가 작은 순서로 실패 사각형 경계 처리
#     coordinate_index = {value: number for number, value in enumerate(coordinates)}  # 실제 V 경계를 압축 번호로 한 번에 바꿀 사전 준비
#     for index, (u, first, last, change) in enumerate(events):  # 스윕 전에 모든 이벤트의 V 경계 번호를 확정
#         events[index] = (u, coordinate_index[first], coordinate_index[last], change)  # 기존 이벤트 자리에 실제 V 좌표 대신 압축 구간 번호 저장
#     del coordinate_index  # 큰 덮임 트리를 만들기 전에 변환 사전 메모리 해제
#     leaves, base = len(coordinates) - 1, 1  # 실제 V 구간 수와 완전 이진 트리의 리프 밑변 크기
#     while base < leaves:  # 실제 구간 수를 담을 최소 2의 거듭제곱 찾기
#         base *= 2  # 완전 이진 트리 밑변을 두 배로 늘리기
#     size = base * 2  # 루트부터 모든 리프까지 저장할 배열 길이
#     cover = [0] * size  # 각 구간 전체를 덮는 실패 사각형 수; 반복 접근이 많은 값은 리스트로 저장
#     statistics = [0] * size  # t 합·홀수 개수·짝수 개수를 하나의 파이썬 정수에 묶어 저장
#     count_mask = (1 << 32) - 1  # 묶인 정수에서 홀짝 개수 필드를 꺼낼 32비트 마스크
#     for leaf in range(leaves):  # 각 압축 리프의 초기 정수 구간 통계 계산
#         low, high = coordinates[leaf], coordinates[leaf + 1] - 1  # 리프가 담는 포함 정수 V 범위
#         even = high // 2 - (low + 1) // 2 + 1  # 이 구간의 짝수 V 개수
#         odd = high - low + 1 - even  # 전체 정수 개수에서 짝수를 뺀 홀수 개수
#         moment = high * high // 4 - (low - 1) * (low - 1) // 4  # F(V)=V²//4의 차이로 모든 floor(V/2)의 합 계산
#         statistics[base + leaf] = (moment << 64) + (odd << 32) + even  # 부호 있는 t 합 위에 두 32비트 개수 필드를 겹치지 않게 결합
#     for node in range(base - 1, 0, -1):  # 리프에서 위로 올라가 초기 미덮임 통계 합산
#         statistics[node] = statistics[node * 2] + statistics[node * 2 + 1]  # 서로소 자식 구간은 홀짝 개수 합도 2^32 미만이라 한 정수 덧셈으로 합치기
#     full_statistics = statistics[base:base + leaves]  # 리프 덮임이 사라질 때 그대로 복구할 초기 통계 캐시

#     def update(node, left, right, first, last, change):  # 압축 V 반열린 구간의 실패 덮임 수 증감
#         if first <= left and right <= last:  # 현재 구간이 변경 범위에 완전히 포함되면
#             cover[node] += change  # 이 구간 전체의 덮임 수만 변경
#         else:  # 변경 범위가 현재 구간의 일부에만 걸치는 경우
#             middle = (left + right) // 2  # 자식 구간을 나누는 가운데 리프 위치
#             if first < middle:  # 변경 범위가 왼쪽 자식과 겹치면
#                 update(node * 2, left, middle, first, last, change)  # 왼쪽 구간의 실패 덮임 수 갱신
#             if last > middle:  # 변경 범위가 오른쪽 자식과 겹치면
#                 update(node * 2 + 1, middle, right, first, last, change)  # 오른쪽 구간의 실패 덮임 수 갱신
#         if cover[node]:  # 실패 기록이 현재 구간 전체를 덮고 있으면
#             statistics[node] = 0  # 현재 구간의 후보 개수와 t 합을 함께 0으로 제외
#         elif node < base:  # 덮이지 않은 내부 구간이면
#             statistics[node] = statistics[node * 2] + statistics[node * 2 + 1]  # 양쪽 자식의 세 통계를 한 정수 덧셈으로 합치기
#         else:  # 리프의 덮임이 모두 사라지면
#             statistics[node] = full_statistics[node - base]  # 저장해 둔 리프의 세 통계를 한 번에 복구

#     def prefix(bound):  # V가 bound 이하인 미덮임 후보의 세 통계를 묶은 정수 반환
#         if bound < low_v:  # 전체 후보 V보다 앞에서 끝나면
#             return 0  # 접두 구간에 들어가는 V가 없음
#         if bound >= high_v:  # 전체 후보 V를 포함하면
#             return statistics[1]  # 루트의 묶인 통계를 그대로 반환
#         total = 0  # 완전히 포함한 앞쪽 구간들의 묶인 통계 합
#         node, left, right = 1, 0, base  # 전체 트리 루트부터 마지막 리프 위치 탐색
#         while node < base:  # 접두 구간의 마지막 리프까지 한 경로만 내려가기
#             if cover[node]:  # 현재 구간 전체가 실패 영역에 덮여 있으면
#                 return total  # 이 아래에는 더할 후보가 없으므로 누적 통계 반환
#             middle = (left + right) // 2  # 현재 구간의 가운데 압축 위치
#             cut = coordinates[middle] if middle < leaves else high_v + 1  # 빈 끝 리프의 경계는 전체 V 끝 다음으로 처리
#             if bound < cut:  # 접두 구간 끝이 왼쪽 자식 안에 있으면
#                 node *= 2; right = middle  # 왼쪽 자식에서 경계 탐색 계속
#             else:  # 왼쪽 자식 전체가 접두 구간에 포함되면
#                 a = node * 2  # 통째로 더할 왼쪽 구간
#                 total += statistics[a]  # 서로소 앞 구간의 세 통계를 한 번에 누적
#                 node = a + 1; left = middle  # 오른쪽 자식에서 남은 경계 탐색
#         if not cover[node]:  # 마지막 리프가 덮이지 않았으면 그 안쪽 부분도 포함
#             low = coordinates[left]  # 현재 리프의 첫 정수 V; 마지막 정수는 탐색한 bound
#             even = bound // 2 - (low + 1) // 2 + 1  # 부분 리프의 짝수 V 개수
#             odd = bound - low + 1 - even  # 부분 리프의 홀수 V 개수
#             moment = bound * bound // 4 - (low - 1) * (low - 1) // 4  # 부분 리프의 floor(V/2) 합을 F의 차이로 계산
#             total += (moment << 64) + (odd << 32) + even  # 부분 리프의 세 통계를 묶어 접두 구간에 더하기
#         return total  # 접두 구간의 미덮임 세 통계를 묶은 정수 반환

#     def count_slab(left_u, right_u):  # 덮임 상태가 같은 정수 U 슬랩의 원래 격자점 수 계산
#         if left_u > right_u or statistics[1] == 0:  # 빈 슬랩이나 남은 V가 없는 상태는 제외
#             return 0  # 이 슬랩에는 가능한 위치가 없음
#         first_v = max(low_v, -right_u, left_u - 2 * m)  # 원래 격자에서 이 U 슬랩과 만나는 V의 최소 정수
#         last_v = min(high_v, right_u, 2 * n - left_u)  # 원래 격자에서 이 U 슬랩과 만나는 V의 최대 정수
#         if first_v > last_v:  # 원래 격자 경계와 만나는 V가 없으면
#             return 0  # 이 슬랩의 후보 위치는 없음
#         if left_u == right_u:  # U가 정수 한 값으로 고정되면 상·하한을 조각별로 계산할 필요가 없음
#             difference = prefix(last_v) - prefix(first_v - 1)  # 원래 격자와 만나는 V 구간에서 실패 영역 밖의 묶인 통계 조회
#             shift = 32 if left_u & 1 else 0  # 고정 U가 홀수이면 홀수 개수 필드, 짝수이면 짝수 개수 필드 선택
#             return (difference >> shift) & count_mask  # U와 V의 홀짝이 같은 미덮임 V 하나마다 원래 정수 격자점 하나씩 대응
#         boundaries = sorted((first_v, last_v + 1, -left_u, left_u + 1, right_u - 2 * m, 2 * n - right_u + 1))  # 가능한 V 구간에서 U 상·하한 식이 바뀌는 경계 정렬
#         previous = prefix(first_v - 1)  # 연속 V 조각들의 첫 시작 전 통계를 한 번만 조회
#         result = 0  # 이번 슬랩의 가능한 원래 정수 격자점 수
#         for index in range(5):  # U 상·하한이 각각 일차식인 V 조각 확인
#             low, high = max(first_v, boundaries[index]), min(last_v, boundaries[index + 1] - 1)  # 원래 격자와 만나는 현재 V 조각
#             if low > high:  # 중복 경계나 가능한 V 범위 밖의 조각이면
#                 continue  # 통계를 조회하지 않고 다음 조각으로 이동
#             lower_a = -1 if low < -left_u else 1 if low > left_u else 0  # U 하한이 −V, V, L 중 어느 일차식인지 선택
#             lower_b = 0 if lower_a else left_u  # 선택한 U 하한의 상수항
#             upper_a = 1 if low < right_u - 2 * m else -1 if low > 2 * n - right_u else 0  # U 상한이 2m+V, 2n−V, R 중 어느 일차식인지 선택
#             upper_b = 2 * m if upper_a == 1 else 2 * n if upper_a == -1 else right_u  # 선택한 U 상한의 상수항
#             current = prefix(high)  # 현재 조각의 끝까지 묶인 접두 통계 한 번 조회
#             difference = current - previous  # 포함 관계인 접두 구간 차이이므로 개수 필드의 빌림 없이 현재 조각 통계만 남기기
#             even = difference & count_mask  # 하위 32비트에서 현재 조각의 짝수 V 개수 추출
#             odd = (difference >> 32) & count_mask  # 다음 32비트에서 홀수 V 개수 추출
#             moment = difference >> 64  # 산술 오른쪽 시프트로 음수도 가능한 t 합을 정확히 복원
#             constant_even = upper_b // 2 - (lower_b + 1) // 2 + 1  # 짝수 V=2t에서 허용 U 수의 상수항
#             constant_odd = (upper_b + upper_a - 1) // 2 - (lower_b + lower_a) // 2 + 1  # 홀수 V=2t+1에서 허용 U 수의 상수항
#             result += (upper_a - lower_a) * moment + constant_even * even + constant_odd * odd  # 공통 t 기울기와 홀짝별 상수항으로 조각의 위치 수 합산
#             previous = current  # 다음 연속 조각의 시작 전 통계로 방금 조회한 끝 통계 재사용
#         return result  # 이번 U 슬랩의 정수 표지판 위치 수 반환

#     answer, current_u, index = 0, low_u, 0  # 누적 위치 수와 아직 세지 않은 첫 U, 다음 이벤트 위치
#     while index < len(events):  # 실패 덮임이 바뀌는 U 경계를 오름차순으로 처리
#         next_u = events[index][0]  # 현재 덮임 상태가 끝나는 다음 U 경계
#         answer += count_slab(current_u, next_u - 1)  # 다음 경계 전까지 덮임이 같은 정수 U 구간 합산
#         while index < len(events) and events[index][0] == next_u:  # 같은 U에서 일어난 실패 영역 추가·제거를 모두 처리
#             _, a, b, change = events[index]  # 이번에 바뀌는 압축 V 반열린 구간과 덮임 증감량
#             update(1, 0, base, a, b, change)  # 실패 사각형의 V 덮임 수를 트리에 반영
#             index += 1  # 다음 경계 이벤트로 이동
#         current_u = next_u  # 새 덮임 상태에서 아직 세지 않은 첫 U 기록
#     answer += count_slab(current_u, high_u)  # 마지막 이벤트 뒤에 남은 정수 U 구간 합산
#     del update  # 재귀 함수의 자기 참조를 끊어 큰 트리 배열이 반환 뒤 바로 정리되게 하기
#     return answer  # 모든 기록에 맞는 정수 표지판 위치의 개수 반환




# 풀이 요약
# U=X+Y, V=X−Y로 바꾸면 맨해튼 거리 조건이 축에 평행한 사각형; 성공 영역은 교집합, 실패 영역은 U 스윕의 V 덮임으로 처리
# 정수 U 슬랩 [L,R]가 원래 격자와 만나는 V는 [max(V최소,−R,L−2M), min(V최대,R,2N−L)]의 한 연속 구간
# U 상·하한 식이 바뀌는 경계로 나누면 허용 U 개수는 t=floor(V/2)의 일차식; U와 V의 같은 홀짝 조건은 홀짝별 상수항으로 반영
# 미덮임 t 합·홀수 개수·짝수 개수를 (합<<64)+(홀수<<32)+짝수 한 정수에 저장해 자식 합과 접두 누적을 정수 덧셈 하나로 처리
# 각 홀짝 개수는 10억+1 이하라 32비트 필드 사이에 캐리가 없고, 포함 관계인 접두 구간 차이에도 빌림이 없음; 음수 t 합은 산술 >>64로 복원
# F(V)=V²//4의 차이로 부분 리프의 t 합을 구하고 리프 복구는 초기 통계 캐시 사용; 연속 V 조각의 앞 접두 통계는 직전 끝 통계 재사용
# U 슬랩이 정수 한 행이면 가능한 V 구간에서 U와 같은 홀짝의 개수만 두 접두 조회의 차이로 계산해 일반 조각 분할과 t 합 복원을 생략
# V 경계의 압축 번호를 사전으로 모든 이벤트에 미리 붙여 스윕 중 이분 탐색을 없애고, 변환 사전은 트리 할당 전에 해제
# 테스트 Q개에서 시간 O(Q log Q), 보조 공간 O(Q)
