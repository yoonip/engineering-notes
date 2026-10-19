def solution(coin, cards):
    # len은 카드 개수.
    n = len(cards)
    target = n + 1
    # set은 초기 카드의 포함 여부를 확인할 집합.
    initial = set(cards[:n // 3])
    drawn = set()
    # 동전 0·1·2개로 사용할 수 있는 완성된 카드 쌍의 수.
    available = [0, 0, 0]
    for card in initial:
        # 초기 카드끼리의 쌍을 작은 카드에서만 세어 중복 방지.
        if card < target - card and target - card in initial:
            available[0] += 1
    # 게임은 1라운드부터 시작.
    round_number = 1
    for index in range(n // 3, n, 2):
        # 이번 라운드의 두 카드를 순회.
        for card in cards[index:index + 2]:
            partner = target - card
            # 짝이 초기 카드라면 새 카드 한 장만 구매하면 됨.
            if partner in initial:
                available[1] += 1
            elif partner in drawn:
                # 두 번째 카드가 나올 때만 세므로 중복되지 않음.
                available[2] += 1
            drawn.add(card)
        # 비용 0,1,2 순서로 쌍을 선택하는 그리디.
        for price in range(3):
            if available[price] and coin >= price:
                # 선택한 쌍 하나를 소모.
                available[price] -= 1
                coin -= price
                # 다음 라운드로 진행.
                round_number += 1
                break
        else:
            return round_number
    return round_number
