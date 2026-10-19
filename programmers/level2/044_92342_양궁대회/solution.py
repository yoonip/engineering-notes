def solution(n, info):
    best_key = (0, [])
    answer = [-1]
    for mask in range(1 << 10):
        shots = [0] * 11
        remaining = n
        for index in range(10):
            if mask & (1 << index):
                shots[index] = info[index] + 1
                remaining -= shots[index]
        if remaining < 0:
            continue
        shots[10] = remaining
        difference = 0
        for index in range(10):
            if shots[index] > info[index]:
                difference += 10 - index
            elif info[index] > 0:
                difference -= 10 - index
        key = (difference, shots[::-1])
        if difference > 0 and key > best_key:
            best_key, answer = key, shots
    return answer

# 전체 코드 줄별 설명
# def solution(n, info):  # def는 함수 정의. n은 화살 수, info는 어피치의 점수별 화살 수.
#     best_key = (0, [])  # () 튜플은 차이·낮은 점수 우선 비교값. []는 빈 리스트.
#     answer = [-1]  # 이길 수 없는 경우의 기본 반환값.
#     for mask in range(1 << 10):  # <<는 왼쪽 비트 이동. 2^10가지 점수 획득 여부를 정수 비트로 표현.
#         shots = [0] * 11  # *로 0을 반복한 리스트. 라이언의 10점~0점 화살 수 초기화.
#         remaining = n  # =는 대입. 아직 쏘지 않은 화살 수.
#         for index in range(10):  # range(10)은 0~9. 10점부터 1점까지 검사.
#             if mask & (1 << index):  # &는 비트 AND. 해당 점수를 이기는 선택인지 검사.
#                 shots[index] = info[index] + 1  # []는 인덱싱. 어피치보다 한 발 더 쏴 해당 점수를 획득.
#                 remaining -= shots[index]  # -=는 빼서 저장. 사용 화살 차감.
#         if remaining < 0:  # <는 작음. 화살 수를 넘은 선택 제외.
#             continue  # continue는 다음 선택 조합으로 이동.
#         shots[10] = remaining  # 남은 화살은 동률 규칙에 유리한 0점에 모두 배정.
#         difference = 0  # 점수 차이 초기화.
#         for index in range(10):  # 실제 점수가 있는 열 개 과녁 순회.
#             if shots[index] > info[index]:  # >는 큼. 라이언이 이긴 과녁인지 검사.
#                 difference += 10 - index  # +=는 더해 저장. 라이언 점수 추가.
#             elif info[index] > 0:  # elif는 앞 조건이 거짓일 때 검사. 어피치가 맞힌 과녁이면 어피치 득점.
#                 difference -= 10 - index  # 어피치 점수를 차이에서 차감.
#         key = (difference, shots[::-1])  # [::-1]은 역순 슬라이스. 낮은 점수 화살 수부터 비교할 키 생성.
#         if difference > 0 and key > best_key:  # and는 둘 다 참. 튜플·리스트는 앞 원소부터 사전식 비교.
#             best_key, answer = key, shots  # 더 큰 점수 차이 또는 유리한 동률 배치로 갱신.
#     return answer  # return으로 최적 화살 배치 또는 [-1] 반환.

# 풀이 요약
# 각 점수에서 이기려면 어피치보다 한 발 더 쏘고, 포기하면 0발로 둡니다. 모든 점수 선택을 검사하고 남은 화살은 0점에 둡니다.
# 예: 첫 예제의 최적 배치는 [0,2,2,0,1,0,0,0,0,0,0]. 동률은 낮은 점수부터 비교. 시간 O(2^10*11), 공간 O(11).
