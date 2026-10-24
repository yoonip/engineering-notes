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
    cover = array('i', [0]) * size
    count_even, count_odd = array('I', [0]) * size, array('I', [0]) * size
    sum_even, sum_odd = array('q', [0]) * size, array('q', [0]) * size
    for leaf in range(leaves):
        low, high = coordinates[leaf], coordinates[leaf + 1] - 1
        first, last = (low + 1) // 2, high // 2
        even = max(0, last - first + 1)
        count_even[base + leaf], sum_even[base + leaf] = even, (first + last) * even // 2
        first, last = low // 2, (high - 1) // 2
        odd = max(0, last - first + 1)
        count_odd[base + leaf], sum_odd[base + leaf] = odd, (first + last) * odd // 2
    for node in range(base - 1, 0, -1):
        a, b = node * 2, node * 2 + 1
        count_even[node], count_odd[node] = count_even[a] + count_even[b], count_odd[a] + count_odd[b]
        sum_even[node], sum_odd[node] = sum_even[a] + sum_even[b], sum_odd[a] + sum_odd[b]

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
            count_even[node] = count_odd[node] = sum_even[node] = sum_odd[node] = 0
        elif node < base:
            a, b = node * 2, node * 2 + 1
            count_even[node], count_odd[node] = count_even[a] + count_even[b], count_odd[a] + count_odd[b]
            sum_even[node], sum_odd[node] = sum_even[a] + sum_even[b], sum_odd[a] + sum_odd[b]
        else:
            leaf = node - base
            low, high = coordinates[leaf], coordinates[leaf + 1] - 1
            first_t, last_t = (low + 1) // 2, high // 2
            even = max(0, last_t - first_t + 1)
            count_even[node], sum_even[node] = even, (first_t + last_t) * even // 2
            first_t, last_t = low // 2, (high - 1) // 2
            odd = max(0, last_t - first_t + 1)
            count_odd[node], sum_odd[node] = odd, (first_t + last_t) * odd // 2

    def prefix(bound):
        if bound < low_v:
            return 0, 0, 0, 0
        if bound >= high_v:
            return count_even[1], count_odd[1], sum_even[1], sum_odd[1]
        ce = co = se = so = 0
        node, left, right = 1, 0, base
        while node < base:
            if cover[node]:
                return ce, co, se, so
            middle = (left + right) // 2
            cut = coordinates[middle] if middle < leaves else high_v + 1
            if bound < cut:
                node *= 2; right = middle
            else:
                a = node * 2
                ce += count_even[a]; co += count_odd[a]
                se += sum_even[a]; so += sum_odd[a]
                node = a + 1; left = middle
        if not cover[node]:
            low, high = coordinates[left], min(bound, coordinates[left + 1] - 1)
            first, last = (low + 1) // 2, high // 2
            even = max(0, last - first + 1)
            ce += even; se += (first + last) * even // 2
            first, last = low // 2, (high - 1) // 2
            odd = max(0, last - first + 1)
            co += odd; so += (first + last) * odd // 2
        return ce, co, se, so

    def count_slab(left_u, right_u):
        if left_u > right_u or count_even[1] + count_odd[1] == 0:
            return 0
        boundaries = sorted((low_v, high_v + 1, -left_u, left_u + 1, right_u - 2 * m, 2 * n - right_u + 1))
        result = 0
        for index in range(5):
            low, high = max(low_v, boundaries[index]), min(high_v, boundaries[index + 1] - 1)
            if low > high:
                continue
            lower_a = -1 if low < -left_u else 1 if low > left_u else 0
            lower_b = 0 if lower_a else left_u
            upper_a = 1 if low < right_u - 2 * m else -1 if low > 2 * n - right_u else 0
            upper_b = 2 * m if upper_a == 1 else 2 * n if upper_a == -1 else right_u
            slope, difference = upper_a - lower_a, upper_b - lower_b
            if slope > 0:
                low = max(low, -(difference // slope))
            elif slope < 0:
                high = min(high, difference // -slope)
            elif difference < 0:
                continue
            if low > high:
                continue
            ce, co, se, so = prefix(high)
            ae, ao, be, bo = prefix(low - 1)
            constant_even = upper_b // 2 - (lower_b + 1) // 2 + 1
            constant_odd = (upper_b + upper_a - 1) // 2 - (lower_b + lower_a) // 2 + 1
            result += slope * (se + so - be - bo) + constant_even * (ce - ae) + constant_odd * (co - ao)
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
# from array import array  # 덮임 수·홀짝 개수·합을 고정 폭 숫자 배열에 저장해 메모리 절약
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
#     cover = array('i', [0]) * size  # 각 트리 구간 전체를 덮는 실패 사각형 수
#     count_even, count_odd = array('I', [0]) * size, array('I', [0]) * size  # 미덮임 V의 홀짝별 개수; 각각 10억+1 이하
#     sum_even, sum_odd = array('q', [0]) * size, array('q', [0]) * size  # V=2t+p에서 미덮임 t의 홀짝별 64비트 합
#     for leaf in range(leaves):  # 각 압축 리프의 모든 정수 V를 초기 후보로 등록
#         low, high = coordinates[leaf], coordinates[leaf + 1] - 1  # 리프가 담는 포함 정수 구간
#         first, last = (low + 1) // 2, high // 2  # 짝수 V=2t에 대응하는 t의 최소·최대 정수
#         even = max(0, last - first + 1)  # 이 리프의 짝수 V 개수
#         count_even[base + leaf], sum_even[base + leaf] = even, (first + last) * even // 2  # 짝수 V의 개수와 t 등차수열 합 저장
#         first, last = low // 2, (high - 1) // 2  # 홀수 V=2t+1에 대응하는 t의 최소·최대 정수
#         odd = max(0, last - first + 1)  # 이 리프의 홀수 V 개수
#         count_odd[base + leaf], sum_odd[base + leaf] = odd, (first + last) * odd // 2  # 홀수 V의 개수와 t 등차수열 합 저장
#     for node in range(base - 1, 0, -1):  # 리프 통계를 아래에서 위로 합쳐 초기 트리 구성
#         a, b = node * 2, node * 2 + 1  # 현재 구간의 왼쪽·오른쪽 자식
#         count_even[node], count_odd[node] = count_even[a] + count_even[b], count_odd[a] + count_odd[b]  # 두 자식의 홀짝별 정수 개수 합치기
#         sum_even[node], sum_odd[node] = sum_even[a] + sum_even[b], sum_odd[a] + sum_odd[b]  # 두 자식의 홀짝별 t 합 합치기

#     def update(node, left, right, first, last, change):  # 압축 V 반열린 구간의 실패 덮임 수 증감
#         if first <= left and right <= last:  # 현재 트리 구간이 변경 범위에 완전히 포함되면
#             cover[node] += change  # 이 구간 전체의 실패 덮임 수만 변경
#         else:  # 변경 범위가 현재 구간의 일부에만 걸치는 경우
#             middle = (left + right) // 2  # 압축 리프 구간을 나눌 가운데 위치
#             if first < middle:  # 변경 범위가 왼쪽 자식과 겹치면
#                 update(node * 2, left, middle, first, last, change)  # 왼쪽 부분의 실패 덮임 갱신
#             if last > middle:  # 변경 범위가 오른쪽 자식과 겹치면
#                 update(node * 2 + 1, middle, right, first, last, change)  # 오른쪽 부분의 실패 덮임 갱신
#         if cover[node]:  # 현재 구간 전체를 덮는 실패 기록이 하나라도 있으면
#             count_even[node] = count_odd[node] = sum_even[node] = sum_odd[node] = 0  # 이 구간의 모든 V를 후보에서 제외
#         elif node < base:  # 덮이지 않은 내부 구간이면 자식의 남은 부분만 포함
#             a, b = node * 2, node * 2 + 1  # 통계를 다시 합칠 양쪽 자식
#             count_even[node], count_odd[node] = count_even[a] + count_even[b], count_odd[a] + count_odd[b]  # 미덮임 홀짝별 개수 갱신
#             sum_even[node], sum_odd[node] = sum_even[a] + sum_even[b], sum_odd[a] + sum_odd[b]  # 미덮임 홀짝별 t 합 갱신
#         else:  # 덮임이 사라진 실제 리프는 원래 정수 구간으로 복구
#             leaf = node - base  # 완전 이진 트리의 리프 번호를 압축 구간 번호로 변환
#             low, high = coordinates[leaf], coordinates[leaf + 1] - 1  # 리프가 원래 담던 포함 정수 V 구간
#             first_t, last_t = (low + 1) // 2, high // 2  # 짝수 V에 대응하는 t 범위 복원
#             even = max(0, last_t - first_t + 1)  # 복구할 짝수 V 개수
#             count_even[node], sum_even[node] = even, (first_t + last_t) * even // 2  # 짝수 개수와 t 합 복구
#             first_t, last_t = low // 2, (high - 1) // 2  # 홀수 V에 대응하는 t 범위 복원
#             odd = max(0, last_t - first_t + 1)  # 복구할 홀수 V 개수
#             count_odd[node], sum_odd[node] = odd, (first_t + last_t) * odd // 2  # 홀수 개수와 t 합 복구

#     def prefix(bound):  # V가 bound 이하인 미덮임 후보의 홀짝 개수와 t 합 조회
#         if bound < low_v:  # 전체 후보 V보다 앞에서 끝나는 접두 구간이면
#             return 0, 0, 0, 0  # 들어가는 정수 V가 없음
#         if bound >= high_v:  # 전체 후보 V를 포함하는 접두 구간이면
#             return count_even[1], count_odd[1], sum_even[1], sum_odd[1]  # 루트에 저장된 통계를 바로 사용
#         ce = co = se = so = 0  # 완전히 포함한 앞쪽 구간들의 홀짝 개수와 t 합
#         node, left, right = 1, 0, base  # 전체 덮임 트리 루트부터 경계 위치 찾기
#         while node < base:  # 접두 구간의 마지막 리프까지 한 경로만 내려가기
#             if cover[node]:  # 현재 구간 전체가 실패 영역에 덮여 있으면
#                 return ce, co, se, so  # 이 아래에는 더할 후보가 없으므로 앞서 모은 통계 반환
#             middle = (left + right) // 2  # 현재 구간의 가운데 압축 리프 경계
#             cut = coordinates[middle] if middle < leaves else high_v + 1  # 빈 리프가 붙은 오른쪽 끝은 전체 V 끝 다음으로 처리
#             if bound < cut:  # 접두 구간 끝이 왼쪽 자식 안에 있으면
#                 node *= 2; right = middle  # 왼쪽 자식에서 계속 경계 탐색
#             else:  # 왼쪽 자식 전체가 접두 구간에 포함되면
#                 a = node * 2  # 통계를 통째로 더할 왼쪽 구간
#                 ce += count_even[a]; co += count_odd[a]  # 왼쪽 미덮임 홀짝 개수 누적
#                 se += sum_even[a]; so += sum_odd[a]  # 왼쪽 미덮임 t 합 누적
#                 node = a + 1; left = middle  # 오른쪽 자식에서 남은 접두 경계 탐색
#         if not cover[node]:  # 마지막 리프가 덮이지 않았으면 그 안의 일부 구간도 포함
#             low, high = coordinates[left], min(bound, coordinates[left + 1] - 1)  # 마지막 리프와 접두 구간이 겹치는 포함 정수 범위
#             first, last = (low + 1) // 2, high // 2  # 마지막 부분 구간의 짝수 V에 대응하는 t 범위
#             even = max(0, last - first + 1)  # 추가할 짝수 V 개수
#             ce += even; se += (first + last) * even // 2  # 짝수 개수와 t 합을 등차수열로 추가
#             first, last = low // 2, (high - 1) // 2  # 마지막 부분 구간의 홀수 V에 대응하는 t 범위
#             odd = max(0, last - first + 1)  # 추가할 홀수 V 개수
#             co += odd; so += (first + last) * odd // 2  # 홀수 개수와 t 합을 등차수열로 추가
#         return ce, co, se, so  # 덮이지 않은 V 접두 구간의 네 통계 반환

#     def count_slab(left_u, right_u):  # 실패 덮임 상태가 같은 정수 U 슬랩의 원래 격자점 수 계산
#         if left_u > right_u or count_even[1] + count_odd[1] == 0:  # 빈 슬랩이나 남은 V가 없는 상태는 제외
#             return 0  # 이 슬랩에서 가능한 위치가 없음
#         boundaries = sorted((low_v, high_v + 1, -left_u, left_u + 1, right_u - 2 * m, 2 * n - right_u + 1))  # U 하한 max(L,−V,V)와 상한 min(R,2n−V,2m+V)의 식이 바뀌는 V 경계
#         result = 0  # 이번 슬랩의 가능한 원래 정수 격자점 수
#         for index in range(5):  # 상·하한이 각각 일차식인 V 조각을 차례로 확인
#             low, high = max(low_v, boundaries[index]), min(high_v, boundaries[index + 1] - 1)  # 후보 V 범위 안에 들어오는 현재 조각
#             if low > high:  # 중복 경계나 후보 범위 밖의 조각이면
#                 continue  # 가능한 V가 없으므로 건너뛰기
#             lower_a = -1 if low < -left_u else 1 if low > left_u else 0  # U 하한이 −V, V, L 중 어느 식인지 선택
#             lower_b = 0 if lower_a else left_u  # U 하한 일차식의 상수항
#             upper_a = 1 if low < right_u - 2 * m else -1 if low > 2 * n - right_u else 0  # U 상한이 2m+V, 2n−V, R 중 어느 식인지 선택
#             upper_b = 2 * m if upper_a == 1 else 2 * n if upper_a == -1 else right_u  # U 상한 일차식의 상수항
#             slope, difference = upper_a - lower_a, upper_b - lower_b  # U 상한−하한의 기울기와 상수항
#             if slope > 0:  # V가 충분히 커야 U 상한이 하한 이상인 경우
#                 low = max(low, -(difference // slope))  # ceil(−difference/slope) 이상인 정수 V만 남기기
#             elif slope < 0:  # V가 충분히 작아야 U 구간이 비지 않는 경우
#                 high = min(high, difference // -slope)  # floor(difference/−slope) 이하인 정수 V만 남기기
#             elif difference < 0:  # 평행한 상한이 하한보다 작은 경우
#                 continue  # 어느 V에서도 가능한 U가 없음
#             if low > high:  # 원래 격자 경계로 자른 뒤 후보 V가 남지 않으면
#                 continue  # 이 조각은 답에 더하지 않음
#             ce, co, se, so = prefix(high)  # 조각 끝까지의 미덮임 홀짝 통계 조회
#             ae, ao, be, bo = prefix(low - 1)  # 조각 시작 전까지의 통계를 빼서 현재 V 범위만 남길 준비
#             constant_even = upper_b // 2 - (lower_b + 1) // 2 + 1  # V=2t일 때 가능한 U 수의 일차식 상수항
#             constant_odd = (upper_b + upper_a - 1) // 2 - (lower_b + lower_a) // 2 + 1  # V=2t+1일 때 가능한 U 수의 일차식 상수항
#             result += slope * (se + so - be - bo) + constant_even * (ce - ae) + constant_odd * (co - ao)  # 허용 U 개수가 t의 일차식이므로 구간 모멘트로 한 번에 합산
#         return result  # 실패 영역 밖이면서 원래 격자 안인 이번 U 슬랩의 위치 수

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
# U=X+Y, V=X−Y로 바꾸면 맨해튼 거리 이내 조건이 축에 평행한 사각형으로 바뀜
# 성공 사각형은 교집합으로 줄이고 실패 사각형 합집합은 U 경계 스윕과 V 덮임 트리로 제외
# 원래 격자의 |V|≤U≤min(2N−V,2M+V)와 U,V의 같은 홀짝 조건을 따로 반영
# 실패 덮임이 같은 U 슬랩에서 상·하한 식이 바뀌는 V 조각을 나누면, 각 V의 허용 U 개수는 t=(V−홀짝)/2의 일차식
# 트리에 미덮임 V의 홀짝별 개수와 t 합을 저장하고 두 접두 조회의 차이로 조각의 위치 수 합산
# 리프 일부를 조회하면 정수 등차수열로 직접 계산; 음수 좌표에도 파이썬 //의 내림 성질을 그대로 사용
# 테스트 Q개에서 시간 O(Q log Q), 보조 공간 O(Q); 큰 트리 통계는 array 모듈의 32·64비트 배열로 저장
