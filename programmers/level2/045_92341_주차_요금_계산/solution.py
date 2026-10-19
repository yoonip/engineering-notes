# 문제: 주차 요금 계산
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/92341
# 풀이: 해시로 차량별 입차 시각과 누적 주차 시간을 관리한다. 미출차는 23:59로 마감하고 차량 번호순으로 요금을 계산한다.
# 복잡도: 기록 R개·차량 C대: 시간 O(R+C log C), 추가 공간 O(C).

def solution(fees, records):
    entered, totals = {}, {}
    for record in records:
        time, car, action = record.split()
        hour, minute = map(int, time.split(':'))
        now = hour * 60 + minute
        if action == 'IN':
            entered[car] = now
        else:
            totals[car] = totals.get(car, 0) + now - entered.pop(car)
    for car, time in entered.items():
        totals[car] = totals.get(car, 0) + 1439 - time
    base_time, base_fee, unit_time, unit_fee = fees
    answer = []
    for car in sorted(totals):
        extra = max(0, totals[car] - base_time)
        answer.append(base_fee + (extra + unit_time - 1) // unit_time * unit_fee)
    return answer
