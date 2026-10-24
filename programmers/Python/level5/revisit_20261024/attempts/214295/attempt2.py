from array import array
from bisect import bisect_left


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
    leaves, base = len(coordinates) - 1, 1
    while base < leaves:
        base *= 2
    size = base * 2
    cover = [0] * size
    count_even, count_odd = array('I', [0]) * size, array('I', [0]) * size
    sum_t = [0] * size
    for leaf in range(leaves):
        low, high = coordinates[leaf], coordinates[leaf + 1] - 1
        even = high // 2 - (low + 1) // 2 + 1
        count_even[base + leaf] = even
        count_odd[base + leaf] = high - low + 1 - even
        sum_t[base + leaf] = high * high // 4 - (low - 1) * (low - 1) // 4
    for node in range(base - 1, 0, -1):
        a, b = node * 2, node * 2 + 1
        count_even[node], count_odd[node] = count_even[a] + count_even[b], count_odd[a] + count_odd[b]
        sum_t[node] = sum_t[a] + sum_t[b]
    full_even = count_even[base:base + leaves]
    full_odd = count_odd[base:base + leaves]
    full_sum = sum_t[base:base + leaves]

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
            count_even[node] = count_odd[node] = sum_t[node] = 0
        elif node < base:
            a, b = node * 2, node * 2 + 1
            count_even[node], count_odd[node] = count_even[a] + count_even[b], count_odd[a] + count_odd[b]
            sum_t[node] = sum_t[a] + sum_t[b]
        else:
            leaf = node - base
            count_even[node], count_odd[node] = full_even[leaf], full_odd[leaf]
            sum_t[node] = full_sum[leaf]

    def prefix(bound):
        if bound < low_v:
            return 0, 0, 0
        if bound >= high_v:
            return count_even[1], count_odd[1], sum_t[1]
        ce = co = total = 0
        node, left, right = 1, 0, base
        while node < base:
            if cover[node]:
                return ce, co, total
            middle = (left + right) // 2
            cut = coordinates[middle] if middle < leaves else high_v + 1
            if bound < cut:
                node *= 2; right = middle
            else:
                a = node * 2
                ce += count_even[a]; co += count_odd[a]; total += sum_t[a]
                node = a + 1; left = middle
        if not cover[node]:
            low = coordinates[left]
            even = bound // 2 - (low + 1) // 2 + 1
            ce += even; co += bound - low + 1 - even
            total += bound * bound // 4 - (low - 1) * (low - 1) // 4
        return ce, co, total

    def count_slab(left_u, right_u):
        if left_u > right_u or count_even[1] + count_odd[1] == 0:
            return 0
        first_v = max(low_v, -right_u, left_u - 2 * m)
        last_v = min(high_v, right_u, 2 * n - left_u)
        if first_v > last_v:
            return 0
        boundaries = sorted((first_v, last_v + 1, -left_u, left_u + 1, right_u - 2 * m, 2 * n - right_u + 1))
        ae, ao, previous_sum = prefix(first_v - 1)
        result = 0
        for index in range(5):
            low, high = max(first_v, boundaries[index]), min(last_v, boundaries[index + 1] - 1)
            if low > high:
                continue
            lower_a = -1 if low < -left_u else 1 if low > left_u else 0
            lower_b = 0 if lower_a else left_u
            upper_a = 1 if low < right_u - 2 * m else -1 if low > 2 * n - right_u else 0
            upper_b = 2 * m if upper_a == 1 else 2 * n if upper_a == -1 else right_u
            ce, co, total = prefix(high)
            constant_even = upper_b // 2 - (lower_b + 1) // 2 + 1
            constant_odd = (upper_b + upper_a - 1) // 2 - (lower_b + lower_a) // 2 + 1
            result += (upper_a - lower_a) * (total - previous_sum) + constant_even * (ce - ae) + constant_odd * (co - ao)
            ae, ao, previous_sum = ce, co, total
        return result

    answer, current_u, index = 0, low_u, 0
    while index < len(events):
        next_u = events[index][0]
        answer += count_slab(current_u, next_u - 1)
        while index < len(events) and events[index][0] == next_u:
            _, first, last, change = events[index]
            a, b = bisect_left(coordinates, first), bisect_left(coordinates, last)
            update(1, 0, base, a, b, change)
            index += 1
        current_u = next_u
    answer += count_slab(current_u, high_u)
    del update
    return answer

# 전체 코드 줄별 설명
# from array import array  # 홀짝 개수 배열을 32비트 정수로 저장해 메모리 절약
# from bisect import bisect_left  # 실패 사각형의 실제 V 경계를 압축 위치로 찾기


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
#     leaves, base = len(coordinates) - 1, 1  # 실제 V 구간 수와 완전 이진 트리의 리프 밑변 크기
#     while base < leaves:  # 실제 구간 수를 담을 최소 2의 거듭제곱 찾기
#         base *= 2  # 완전 이진 트리 밑변을 두 배로 늘리기
#     size = base * 2  # 루트부터 모든 리프까지 저장할 배열 길이
#     cover = [0] * size  # 각 구간 전체를 덮는 실패 사각형 수; 반복 접근이 많은 값은 리스트로 저장
#     count_even, count_odd = array('I', [0]) * size, array('I', [0]) * size  # 미덮임 V의 홀짝 개수는 각각 10억+1 이하라 32비트 배열에 저장
#     sum_t = [0] * size  # V의 홀짝과 무관하게 t=floor(V/2)의 합 하나만 저장
#     for leaf in range(leaves):  # 각 압축 리프의 초기 정수 구간 통계 계산
#         low, high = coordinates[leaf], coordinates[leaf + 1] - 1  # 리프가 담는 포함 정수 V 범위
#         even = high // 2 - (low + 1) // 2 + 1  # 이 구간의 짝수 V 개수 계산
#         count_even[base + leaf] = even  # 리프의 짝수 V 개수 저장
#         count_odd[base + leaf] = high - low + 1 - even  # 전체 정수 개수에서 짝수를 빼 홀수 개수 저장
#         sum_t[base + leaf] = high * high // 4 - (low - 1) * (low - 1) // 4  # F(V)=V²//4의 차이로 모든 floor(V/2)의 합 계산
#     for node in range(base - 1, 0, -1):  # 리프 통계를 아래에서 위로 합쳐 초기 트리 구성
#         a, b = node * 2, node * 2 + 1  # 현재 구간의 왼쪽·오른쪽 자식
#         count_even[node], count_odd[node] = count_even[a] + count_even[b], count_odd[a] + count_odd[b]  # 두 자식의 홀짝별 개수 합치기
#         sum_t[node] = sum_t[a] + sum_t[b]  # 두 자식의 t 합을 홀짝 구분 없이 합치기
#     full_even = count_even[base:base + leaves]  # 리프 덮임이 사라질 때 복구할 원래 짝수 개수 캐시
#     full_odd = count_odd[base:base + leaves]  # 리프 덮임이 사라질 때 복구할 원래 홀수 개수 캐시
#     full_sum = sum_t[base:base + leaves]  # 큰 정수를 다시 계산하지 않고 복구할 리프의 원래 t 합

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
#             count_even[node] = count_odd[node] = sum_t[node] = 0  # 현재 구간의 모든 V를 후보에서 제외
#         elif node < base:  # 덮이지 않은 내부 구간은 자식의 남은 통계를 합산
#             a, b = node * 2, node * 2 + 1  # 다시 합칠 양쪽 자식
#             count_even[node], count_odd[node] = count_even[a] + count_even[b], count_odd[a] + count_odd[b]  # 미덮임 홀짝 개수 갱신
#             sum_t[node] = sum_t[a] + sum_t[b]  # 미덮임 t 합 갱신
#         else:  # 리프의 덮임이 모두 사라지면 초기 통계를 그대로 복구
#             leaf = node - base  # 트리 노드 번호를 압축 리프 번호로 변환
#             count_even[node], count_odd[node] = full_even[leaf], full_odd[leaf]  # 저장해 둔 홀짝 개수로 복구
#             sum_t[node] = full_sum[leaf]  # 저장해 둔 t 합을 그대로 복구

#     def prefix(bound):  # V가 bound 이하인 미덮임 후보의 홀짝 개수와 t 합 조회
#         if bound < low_v:  # 전체 후보 V보다 앞에서 끝나면
#             return 0, 0, 0  # 접두 구간에 들어가는 V가 없음
#         if bound >= high_v:  # 전체 후보 V를 포함하면
#             return count_even[1], count_odd[1], sum_t[1]  # 루트 통계를 그대로 반환
#         ce = co = total = 0  # 완전히 포함한 앞쪽 구간들의 홀짝 개수와 t 합
#         node, left, right = 1, 0, base  # 전체 트리 루트부터 마지막 리프 위치 탐색
#         while node < base:  # 접두 구간의 마지막 리프까지 한 경로만 내려가기
#             if cover[node]:  # 현재 구간 전체가 실패 영역에 덮여 있으면
#                 return ce, co, total  # 이 아래에는 더할 후보가 없으므로 누적 통계 반환
#             middle = (left + right) // 2  # 현재 구간의 가운데 압축 위치
#             cut = coordinates[middle] if middle < leaves else high_v + 1  # 비어 있는 끝 리프들의 경계는 전체 V 끝 다음으로 처리
#             if bound < cut:  # 접두 구간 끝이 왼쪽 자식 안에 있으면
#                 node *= 2; right = middle  # 왼쪽 자식에서 경계 탐색 계속
#             else:  # 왼쪽 자식 전체가 접두 구간에 포함되면
#                 a = node * 2  # 통째로 더할 왼쪽 구간
#                 ce += count_even[a]; co += count_odd[a]; total += sum_t[a]  # 왼쪽 미덮임 홀짝 개수와 t 합 누적
#                 node = a + 1; left = middle  # 오른쪽 자식에서 남은 경계 탐색
#         if not cover[node]:  # 마지막 리프가 덮이지 않았으면 그 안쪽 부분도 포함
#             low = coordinates[left]  # 현재 리프의 첫 정수 V; 마지막 정수는 탐색한 bound
#             even = bound // 2 - (low + 1) // 2 + 1  # 부분 리프의 짝수 V 개수
#             ce += even; co += bound - low + 1 - even  # 부분 리프의 짝수와 홀수 개수 추가
#             total += bound * bound // 4 - (low - 1) * (low - 1) // 4  # 부분 리프의 floor(V/2) 합을 F의 차이로 추가
#         return ce, co, total  # 접두 구간의 미덮임 홀짝 개수와 t 합 반환

#     def count_slab(left_u, right_u):  # 덮임 상태가 같은 정수 U 슬랩의 원래 격자점 수 계산
#         if left_u > right_u or count_even[1] + count_odd[1] == 0:  # 빈 슬랩이나 남은 V가 없는 상태는 제외
#             return 0  # 이 슬랩에는 가능한 위치가 없음
#         first_v = max(low_v, -right_u, left_u - 2 * m)  # 원래 격자에서 이 U 슬랩과 만나는 V의 최소 정수
#         last_v = min(high_v, right_u, 2 * n - left_u)  # 원래 격자에서 이 U 슬랩과 만나는 V의 최대 정수
#         if first_v > last_v:  # 원래 격자 경계와 만나는 V가 없으면
#             return 0  # 이 슬랩의 후보 위치는 없음
#         boundaries = sorted((first_v, last_v + 1, -left_u, left_u + 1, right_u - 2 * m, 2 * n - right_u + 1))  # 가능한 V 구간에서 U 상·하한 식이 바뀌는 경계 정렬
#         ae, ao, previous_sum = prefix(first_v - 1)  # 연속 V 조각들의 첫 시작 전 통계를 한 번만 조회
#         result = 0  # 이번 슬랩의 가능한 원래 정수 격자점 수
#         for index in range(5):  # U 상·하한이 각각 일차식인 V 조각 확인
#             low, high = max(first_v, boundaries[index]), min(last_v, boundaries[index + 1] - 1)  # 원래 격자와 만나는 현재 V 조각
#             if low > high:  # 중복 경계나 가능한 V 범위 밖의 조각이면
#                 continue  # 통계를 조회하지 않고 다음 조각으로 이동
#             lower_a = -1 if low < -left_u else 1 if low > left_u else 0  # U 하한이 −V, V, L 중 어느 일차식인지 선택
#             lower_b = 0 if lower_a else left_u  # 선택한 U 하한의 상수항
#             upper_a = 1 if low < right_u - 2 * m else -1 if low > 2 * n - right_u else 0  # U 상한이 2m+V, 2n−V, R 중 어느 일차식인지 선택
#             upper_b = 2 * m if upper_a == 1 else 2 * n if upper_a == -1 else right_u  # 선택한 U 상한의 상수항
#             ce, co, total = prefix(high)  # 현재 조각의 끝까지 접두 통계를 한 번 조회
#             constant_even = upper_b // 2 - (lower_b + 1) // 2 + 1  # 짝수 V=2t에서 허용 U 수의 상수항
#             constant_odd = (upper_b + upper_a - 1) // 2 - (lower_b + lower_a) // 2 + 1  # 홀수 V=2t+1에서 허용 U 수의 상수항
#             result += (upper_a - lower_a) * (total - previous_sum) + constant_even * (ce - ae) + constant_odd * (co - ao)  # 두 홀짝의 공통 t 기울기와 서로 다른 상수항으로 조각 전체 합산
#             ae, ao, previous_sum = ce, co, total  # 연속된 다음 조각의 시작 전 통계로 방금 조회한 끝 통계 재사용
#         return result  # 이번 U 슬랩의 정수 표지판 위치 수 반환

#     answer, current_u, index = 0, low_u, 0  # 누적 위치 수와 아직 세지 않은 첫 U, 다음 이벤트 위치
#     while index < len(events):  # 실패 덮임이 바뀌는 U 경계를 오름차순으로 처리
#         next_u = events[index][0]  # 현재 덮임 상태가 끝나는 다음 U 경계
#         answer += count_slab(current_u, next_u - 1)  # 다음 경계 전까지 덮임이 같은 정수 U 구간 합산
#         while index < len(events) and events[index][0] == next_u:  # 같은 U에서 일어난 실패 영역 추가·제거를 모두 처리
#             _, first, last, change = events[index]  # 이번에 바뀌는 실제 V 반열린 구간과 덮임 증감량
#             a, b = bisect_left(coordinates, first), bisect_left(coordinates, last)  # 실제 V 경계를 압축 리프 구간으로 변환
#             update(1, 0, base, a, b, change)  # 실패 사각형의 V 덮임 수를 트리에 반영
#             index += 1  # 다음 경계 이벤트로 이동
#         current_u = next_u  # 새 덮임 상태에서 아직 세지 않은 첫 U 기록
#     answer += count_slab(current_u, high_u)  # 마지막 이벤트 뒤에 남은 정수 U 구간 합산
#     del update  # 재귀 함수의 자기 참조를 끊어 큰 트리 배열이 반환 뒤 바로 정리되게 하기
#     return answer  # 모든 기록에 맞는 정수 표지판 위치의 개수 반환

# 풀이 요약
# U=X+Y, V=X−Y로 바꾸면 맨해튼 거리 조건이 축에 평행한 사각형; 성공 영역은 교집합, 실패 영역은 U 스윕의 V 구간 덮임으로 처리
# 정수 U 슬랩 [L,R]가 원래 격자와 만나는 V는 [max(V최소,−R,L−2M), min(V최대,R,2N−L)]의 한 연속 구간
# 그 구간을 U 상·하한 식이 바뀌는 경계로 나누면 허용 U 개수는 t=floor(V/2)의 일차식이며 U와 V의 같은 홀짝 조건이 상수항에 반영됨
# 트리에는 미덮임 V의 짝수 개수·홀수 개수·공통 t 합 세 통계만 저장; 연속 조각의 앞 접두 통계는 직전 조각의 끝 통계를 재사용
# 모든 정수 V에서 F(V)=V²//4는 F(V)−F(V−1)=floor(V/2)를 만족하므로 리프 일부의 t 합을 두 F값의 차이로 계산
# 리프 덮임이 사라질 때는 미리 저장한 원래 통계를 복구; 홀짝 개수는 uint32 배열, 덮임과 공통 합은 리스트에 저장
# 테스트 Q개에서 시간 O(Q log Q), 보조 공간 O(Q)
