def solution(a, b, g, s, w, t):
    left, right = 0, 4 * 10 ** 14
    while left < right:
        middle = (left + right) // 2
        total_gold = total_silver = total = 0
        for gold, silver, weight, travel in zip(g, s, w, t):
            capacity = ((middle + travel) // (2 * travel)) * weight
            total_gold += min(gold, capacity)
            total_silver += min(silver, capacity)
            total += min(gold + silver, capacity)
            if total_gold >= a and total_silver >= b and total >= a + b:
                break
        if total_gold >= a and total_silver >= b and total >= a + b:
            right = middle
        else:
            left = middle + 1
    return left

# 전체 코드 줄별 설명
# def solution(a, b, g, s, w, t):  # def는 함수 정의. 필요한 금·은과 도시별 보유량·적재량·편도 시간 입력.
#     left, right = 0, 4 * 10 ** 14  # 언패킹으로 이진 탐색 범위 초기화. **는 거듭제곱. 최악의 총 20억 kg·용량 1·편도 10만도 포함하는 상한.
#     while left < right:  # while은 조건이 참인 동안 반복. 가능한 최소 시간을 찾음.
#         middle = (left + right) // 2  # //는 정수 나눗셈. 현재 시간 범위의 중간값.
#         total_gold = total_silver = total = 0  # 연쇄 대입으로 금·은·합계의 최대 운반량 초기화.
#         for gold, silver, weight, travel in zip(g, s, w, t):  # zip은 같은 위치의 원소를 묶음. for로 도시별 네 정보를 언패킹.
#             capacity = ((middle + travel) // (2 * travel)) * weight  # 도착은 t,3t,5t... 시각. 마지막에는 돌아오지 않아도 되므로 이 식으로 운반 횟수×적재량 계산.
#             total_gold += min(gold, capacity)  # min은 작은 값, +=는 더해 저장. 금만 실었을 때의 최대 운반량.
#             total_silver += min(silver, capacity)  # 은만 실었을 때의 최대 운반량.
#             total += min(gold + silver, capacity)  # 금·은이 같은 적재 용량을 나눠 쓰므로 총량 조건도 별도로 계산.
#             if total_gold >= a and total_silver >= b and total >= a + b:  # if는 조건문, >=는 이상, and는 모두 참. 이미 세 조건을 충족하면 나머지 도시는 필요 없음.
#                 break  # break는 도시 탐색 반복 종료.
#         if total_gold >= a and total_silver >= b and total >= a + b:  # 금·은 개별량과 합계량이 모두 충분해야 실제 배분 가능.
#             right = middle  # 가능한 시간이므로 더 짧은 시간에서 최소값 탐색.
#         else:  # else는 아직 운반이 불가능한 경우.
#             left = middle + 1  # 불가능한 중간 시간을 제외한 오른쪽 범위로 이동.
#     return left  # return으로 가능한 최소 시간 반환.

# 풀이 요약
# 주어진 시간 안에 운반 가능한 최대 금·은·총량을 계산합니다. 개별량이 각각 충분해도 같은 트럭 용량을 중복 사용하지 않도록 합계 조건이 필요합니다.
# 시간이 늘면 운반 가능량이 줄지 않으므로 이진 탐색으로 최소 시간을 찾습니다. 마지막 운반은 편도만 필요합니다. 도시 수 N·시간 상한 T에 대해 시간 O(N log T), 추가 공간 O(1).
# 예: 편도 10·적재량 7인 트럭은 10,30,50에 각각 배달합니다. 금·은 합계 20을 운반하려면 세 번 필요해 답은 50입니다.
# 