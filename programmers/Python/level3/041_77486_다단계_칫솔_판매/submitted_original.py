def solution(enroll, referral, seller, amount):
    index = {name: i for i, name in enumerate(enroll)}
    parent = [index.get(name, -1) for name in referral]
    profit = [0] * len(enroll)
    for name, quantity in zip(seller, amount):
        person = index[name]
        money = quantity * 100
        while person != -1 and money > 0:
            share = money // 10
            profit[person] += money - share
            person = parent[person]
            money = share
    return profit

# 전체 코드 줄별 설명
# def solution(enroll, referral, seller, amount):  # def는 함수 정의. 가입자·추천인·판매자·판매량을 입력받음.
#     index = {name: i for i, name in enumerate(enroll)}  # {}는 딕셔너리, enumerate는 번호와 값을 함께 제공. 이름→번호 표 생성.
#     parent = [index.get(name, -1) for name in referral]  # 리스트 컴프리헨션. get은 키 조회, 없으면 -1. 추천인 번호를 저장.
#     profit = [0] * len(enroll)  # []는 리스트, *는 반복, len은 길이. 사람별 이익을 0으로 초기화.
#     for name, quantity in zip(seller, amount):  # zip은 같은 위치끼리 묶음. for로 판매 기록을 하나씩 처리.
#         person = index[name]  # []로 판매자의 번호 조회.
#         money = quantity * 100  # 칫솔당 이익 100원 곱하기.
#         while person != -1 and money > 0:  # while은 조건 반복, !=는 다름, and는 모두 참. 센터에 도달하거나 금액이 0이면 종료.
#             share = money // 10  # //는 정수 나눗셈. 10%를 원 단위에서 버림.
#             profit[person] += money - share  # +=는 더해 저장. 추천인에게 줄 금액을 뺀 나머지를 본인 이익에 추가.
#             person = parent[person]  # 추천인으로 한 단계 올라감.
#             money = share  # 다음 사람에게 나눌 금액으로 갱신. 판매 기록별로 따로 버림해야 함.
#     return profit  # enroll 순서대로 정리된 이익 목록 반환.

# 풀이 요약
# 각 판매의 이익을 본인부터 추천인 방향으로 전달한다. 금액이 단계마다 1/10이 되어 몇 단계 뒤 0이 된다.
# 예: 1200원은 본인 1080원, 추천인 108원, 그 위 11원, 센터 1원으로 분배된다.
# 판매 금액 최대 10000원이므로 기록당 최대 5단계. 시간 O(가입자 수 + 판매 기록 수), 공간 O(가입자 수).
# 