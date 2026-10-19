# 가입자·추천인·판매자·판매량을 입력받음.
def solution(enroll, referral, seller, amount):
    # 이름→번호 표 생성.
    index = {name: i for i, name in enumerate(enroll)}
    # 추천인 번호를 저장.
    parent = [index.get(name, -1) for name in referral]
    # 사람별 이익을 0으로 초기화.
    profit = [0] * len(enroll)
    # for로 판매 기록을 하나씩 처리.
    for name, quantity in zip(seller, amount):
        # []로 판매자의 번호 조회.
        person = index[name]
        # 칫솔당 이익 100원 곱하기.
        money = quantity * 100
        # 센터에 도달하거나 금액이 0이면 종료.
        while person != -1 and money > 0:
            # 10%를 원 단위에서 버림.
            share = money // 10
            # 추천인에게 줄 금액을 뺀 나머지를 본인 이익에 추가.
            profit[person] += money - share
            # 추천인으로 한 단계 올라감.
            person = parent[person]
            # 판매 기록별로 따로 버림해야 함.
            money = share
    # enroll 순서대로 정리된 이익 목록 반환.
    return profit
