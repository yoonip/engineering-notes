# 한 거래의 10%를 재귀적으로 추천인에게 올립니다. 거래를 합쳐서 반올림하면 답이 달라지므로 반드시 거래별로 나눕니다.
# 반복문 대신 재귀로 같은 분배 규칙을 표현합니다.
def solution(enroll,referral,seller,amount):
    parent=dict(zip(enroll,referral));profit=dict.fromkeys(enroll,0)
    def give(person,money):
        if person=='-' or money==0:return
        share=money//10;profit[person]+=money-share
        give(parent[person],share)
    for person,count in zip(seller,amount):give(person,count*100)
    return [profit[name] for name in enroll]
