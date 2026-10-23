def solution(coin, cards):
    n = len(cards)
    target = n + 1
    initial = set(cards[:n // 3])
    drawn = set()
    available = [0, 0, 0]
    for card in initial:
        if card < target - card and target - card in initial:
            available[0] += 1
    round_number = 1
    for index in range(n // 3, n, 2):
        for card in cards[index:index + 2]:
            partner = target - card
            if partner in initial:
                available[1] += 1
            elif partner in drawn:
                available[2] += 1
            drawn.add(card)
        for price in range(3):
            if available[price] and coin >= price:
                available[price] -= 1
                coin -= price
                round_number += 1
                break
        else:
            return round_number
    return round_number

# 전체 코드 줄별 설명
# def solution(coin, cards):  # def는 함수 정의. coin은 동전 수, cards는 뽑는 순서의 카드 목록.
#     n = len(cards)  # len은 카드 개수.
#     target = n + 1  # 한 라운드에 낼 두 카드의 목표 합.
#     initial = set(cards[:n // 3])  # [:끝]은 앞부분 슬라이스, //는 정수 나눗셈. set은 초기 카드의 포함 여부를 확인할 집합.
#     drawn = set()  # set()은 빈 집합. 이미 나온 유료 카드를 기록.
#     available = [0, 0, 0]  # []는 리스트. 동전 0·1·2개로 사용할 수 있는 완성된 카드 쌍의 수.
#     for card in initial:  # for~in으로 초기 카드를 순회.
#         if card < target - card and target - card in initial:  # and는 모두 참, in은 포함 검사. 초기 카드끼리의 쌍을 작은 카드에서만 세어 중복 방지.
#             available[0] += 1  # +=는 더해 저장. 처음 가진 두 카드의 쌍은 무료.
#     round_number = 1  # 게임은 1라운드부터 시작.
#     for index in range(n // 3, n, 2):  # range(시작,끝,간격)으로 남은 카드를 두 장씩 읽음.
#         for card in cards[index:index + 2]:  # [시작:끝]은 끝 제외. 이번 라운드의 두 카드를 순회.
#             partner = target - card  # 이 카드와 짝을 이루는 유일한 카드 값.
#             if partner in initial:  # 짝이 초기 카드라면 새 카드 한 장만 구매하면 됨.
#                 available[1] += 1  # 동전 1개짜리 쌍 추가.
#             elif partner in drawn:  # elif는 앞 조건이 거짓일 때 검사. 짝도 나중에 뽑힌 카드라면 두 장 구매 필요.
#                 available[2] += 1  # 동전 2개짜리 쌍 추가. 두 번째 카드가 나올 때만 세므로 중복되지 않음.
#             drawn.add(card)  # add는 집합 원소 추가. 구매 결정은 쌍을 실제로 사용할 때 비용으로 계산.
#         for price in range(3):  # 비용 0,1,2 순서로 쌍을 선택하는 그리디.
#             if available[price] and coin >= price:  # 0이 아닌 쌍 수와 충분한 동전을 and로 함께 검사.
#                 available[price] -= 1  # -=는 빼서 저장. 선택한 쌍 하나를 소모.
#                 coin -= price  # 필요한 동전 차감.
#                 round_number += 1  # 다음 라운드로 진행.
#                 break  # break는 가격 탐색 종료. 한 라운드에는 한 쌍만 사용.
#         else:  # for-else는 break 없이 반복을 끝냈을 때 실행. 사용할 수 있는 쌍이 없다는 뜻.
#             return round_number  # 현재 라운드에서 게임 종료.
#     return round_number  # 카드가 모두 떨어져 종료한 라운드 번호 반환.

# 풀이 요약
# 각 카드의 짝은 n+1-card로 유일하므로 서로 다른 쌍은 카드를 공유하지 않습니다. 완성된 쌍을 구매 비용 0·1·2로 분류해 매 라운드 가장 싼 쌍부터 씁니다.
# 이미 뽑힌 카드의 구매 비용은 실제 쌍을 쓸 때 계산해도 됩니다. 최종 선택한 카드들을 처음 뽑을 때 샀다고 생각하면 같은 총비용 안의 유효한 전략입니다. 시간·공간 O(N).
# 예: 초기 두 카드의 쌍을 먼저 사용하면 동전을 아껴 나중에 나온 카드로 추가 라운드를 진행할 수 있습니다. 카드를 모두 써도 다음 종료 라운드 번호까지 셉니다.
