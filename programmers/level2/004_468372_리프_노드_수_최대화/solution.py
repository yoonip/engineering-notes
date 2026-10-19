def solution(dist_limit, split_limit):
    def binary_cost(count, depth):
        total = 0
        for _ in range(depth):
            total += count
            count = (count + 1) // 2
        return total

    answer = 1
    width = 1
    depth = 0
    while width <= split_limit:
        answer = max(answer, min(width, dist_limit + 1))
        power = 1
        while width * power * 3 <= split_limit:
            power *= 3
        if depth == 0:
            answer = max(answer, 1 + 2 * min(dist_limit, (power - 1) // 2))
        elif power > 1:
            low, high = 1, width // 2
            while low < high:
                mid = (low + high) // 2
                needed = binary_cost(mid, depth) + mid * (power - 1)
                if needed >= dist_limit:
                    high = mid
                else:
                    low = mid + 1
            for count in (low - 1, low):
                if count == 0:
                    continue
                used = binary_cost(count, depth)
                if used <= dist_limit:
                    ternary = min(dist_limit - used, count * (power - 1))
                    answer = max(answer, 1 + used + 2 * ternary)
        width *= 2
        depth += 1
    return answer

# 전체 코드 줄별 설명 (아래는 모두 실행되지 않는 주석입니다.)
# def solution(dist_limit, split_limit):  # def는 함수 정의. 두 제한값을 입력 매개변수로 받음.
#     def binary_cost(count, depth):  # 이진 분기 부분의 비용을 구하는 중첩 함수 정의.
#         total = 0  # 누적 비용을 정수 0으로 초기화. =는 대입.
#         for _ in range(depth):  # range(depth)만큼 반복. _는 사용하지 않는 반복 변수.
#             total += count  # +=는 더해서 다시 저장. 해당 층의 필요한 노드 수 합산.
#             count = (count + 1) // 2  # ()는 계산 묶음, //는 몫 내림. 필요한 부모 수를 절반 올림으로 계산.
#         return total  # 누적 비용을 호출한 곳에 반환.
#
#     answer = 1  # 분기 없는 트리의 리프 1개를 초기 정답으로 설정.
#     width = 1  # 이진 분기 층까지의 폭을 1로 시작.
#     depth = 0  # 이진 분기 층 수를 0으로 시작.
#     while width <= split_limit:  # while은 조건 반복, <=는 이하. 폭이 분기 제한 안인 경우만 검사.
#         answer = max(answer, min(width, dist_limit + 1))  # min은 작은 값, max는 큰 값 선택. 이진 분기만 쓸 때의 최댓값 반영.
#         power = 1  # 뒤에 붙일 3의 거듭제곱을 1로 시작.
#         while width * power * 3 <= split_limit:  # *는 곱셈. 3배 넓혀도 제한 안이면 반복.
#             power *= 3  # *= 3은 3을 곱해 저장. 가능한 최대 3의 거듭제곱 구함.
#         if depth == 0:  # if는 조건문, ==는 같음. 이진 분기 앞부분이 없는 경우.
#             answer = max(answer, 1 + 2 * min(dist_limit, (power - 1) // 2))  # 삼진 분기 한 번은 리프를 2 늘림. //는 정수 나눗셈, min으로 비용 제한 적용.
#         elif power > 1:  # elif는 앞 조건이 거짓일 때의 추가 조건. 삼진 분기를 붙일 수 있는 경우.
#             low, high = 1, width // 2  # 쉼표 언패킹으로 이진 탐색 경계 두 변수 설정. // 2는 절반 내림.
#             while low < high:  # low<high인 동안 최소 경계를 이진 탐색.
#                 mid = (low + high) // 2  # 괄호로 먼저 더한 뒤 //2로 중간 정수 계산.
#                 needed = binary_cost(mid, depth) + mid * (power - 1)  # 함수 호출 ()로 이진 비용을 구하고 삼진 분기를 모두 채우는 비용을 더함.
#                 if needed >= dist_limit:  # >=는 이상. 비용이 제한 이상인 경계인지 검사.
#                     high = mid  # 경계가 중간 이하에 있으므로 상한을 mid로 줄임.
#                 else:  # else는 앞 if 조건이 거짓일 때 실행.
#                     low = mid + 1  # 검사한 중간값 이하를 제외하고 하한을 mid+1로 올림.
#             for count in (low - 1, low):  # (low-1,low)는 튜플. 경계 직전과 경계 두 경우를 순회.
#                 if count == 0:  # 선택 수가 0인지 확인.
#                     continue  # continue는 이번 경우를 건너뜀.
#                 used = binary_cost(count, depth)  # 해당 개수와 깊이에 필요한 이진 부분 비용 계산.
#                 if used <= dist_limit:  # 이진 비용이 제한 이하일 때만 후보 구성.
#                     ternary = min(dist_limit - used, count * (power - 1))  # 남은 비용과 삼진 부분 용량 중 작은 값을 선택.
#                     answer = max(answer, 1 + used + 2 * ternary)  # 이진 비용만큼 1씩, 삼진 비용만큼 2씩 리프가 늘어난 값을 정답에 반영.
#         width *= 2  # 폭을 2배로 갱신. *=는 곱해서 저장.
#         depth += 1  # 깊이를 1 늘림. +=는 더해서 저장.
#     return answer  # 최대 리프 수를 반환.

# 풀이 요약
# 이진 분기 앞부분과 삼진 분기 뒷부분으로 구성한 후보를 비교합니다.
# 이진 깊이를 순회하고, 비용 제한을 넘는 경계의 양쪽을 이진 탐색으로 확인합니다.
# 이진 분기는 리프를 1개, 삼진 분기는 2개 늘립니다. 예: 분기 없이 1개, 삼진 분기 한 번이면 3개입니다.
