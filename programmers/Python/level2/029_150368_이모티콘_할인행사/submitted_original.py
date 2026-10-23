from itertools import product

def solution(users, emoticons):
    best = (0, 0)
    for rates in product((10, 20, 30, 40), repeat=len(emoticons)):
        subscribers = revenue = 0
        for minimum, limit in users:
            cost = sum(price * (100 - rate) // 100 for price, rate in zip(emoticons, rates) if rate >= minimum)
            if cost >= limit:
                subscribers += 1
            else:
                revenue += cost
        best = max(best, (subscribers, revenue))
    return list(best)

# 전체 코드 줄별 설명
# from itertools import product  # itertools의 product는 각 위치의 모든 선택 조합(데카르트 곱)을 만드는 함수. import로 가져옴.
# 
# def solution(users, emoticons):  # def는 함수 정의, () 안은 구매 기준과 이모티콘 가격 입력.
#     best = (0, 0)  # () 튜플에 최대 가입자 수·매출 저장. =는 대입.
#     for rates in product((10, 20, 30, 40), repeat=len(emoticons)):  # product의 repeat로 이모티콘 수만큼 할인율을 선택. len은 길이.
#         subscribers = revenue = 0  # 연쇄 대입으로 이번 조합의 가입자 수·매출 초기화.
#         for minimum, limit in users:  # for~in으로 사용자별 최소 할인율·가입 기준액 언패킹.
#             cost = sum(price * (100 - rate) // 100 for price, rate in zip(emoticons, rates) if rate >= minimum)  # zip은 같은 위치끼리 짝짓기, if는 구매 조건, //는 정수 몫, sum은 할인 가격 합.
#             if cost >= limit:  # >=는 이상. 구매액이 가입 기준 이상이면 구매 취소 후 가입.
#                 subscribers += 1  # +=는 더해 저장. 가입자 수 증가.
#             else:  # else는 앞 조건이 거짓인 경우.
#                 revenue += cost  # 가입하지 않은 사용자의 구매액만 매출에 추가.
#         best = max(best, (subscribers, revenue))  # max는 최댓값. 튜플은 앞 원소부터 비교해 가입자를 먼저, 동률이면 매출을 최대화.
#     return list(best)  # list로 튜플을 리스트로 바꿔 return으로 반환.

# 풀이 요약
# 할인율 4가지의 모든 조합을 평가해 사용자별 가입 또는 구매 결과를 합산합니다. (가입자,매출)의 사전식 최댓값을 선택합니다.
# 예: 첫 예제는 30%,40% 할인으로 [1,5400]. 사용자 N명·이모티콘 M개일 때 시간 O(4^M*N*M), 추가 공간 O(M).
