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
        # 출차 기록이 없으면 23:59에 나간 것으로 본다.
        totals[car] = totals.get(car, 0) + 1439 - time
    base_time, base_fee, unit_time, unit_fee = fees
    answer = []
    for car in sorted(totals):
        # 기본 시간을 넘은 부분에만 추가 요금을 부과한다.
        extra = max(0, totals[car] - base_time)
        answer.append(base_fee + (extra + unit_time - 1) // unit_time * unit_fee)
    return answer
