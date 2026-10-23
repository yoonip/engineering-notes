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

# 전체 코드 줄별 설명
# def solution(fees, records):  # def는 함수 정의. fees는 요금표, records는 입출차 기록 목록.
#     entered, totals = {}, {}  # {}는 빈 딕셔너리. 차량별 입차 시각·누적 주차 시간 저장.
#     for record in records:  # for~in으로 시간 순 기록 순회.
#         time, car, action = record.split()  # split()은 공백으로 분리. 시각·차량·내역을 언패킹.
#         hour, minute = map(int, time.split(':'))  # ':'로 나눈 문자열에 map(int,...)를 적용해 정수 변환.
#         now = hour * 60 + minute  # *는 곱셈. 시각을 자정 이후 분으로 변환.
#         if action == 'IN':  # if는 분기, ==는 같음. 입차 기록 검사.
#             entered[car] = now  # [키]로 차량의 입차 시각 저장.
#         else:  # else는 출차인 경우.
#             totals[car] = totals.get(car, 0) + now - entered.pop(car)  # get은 없으면 기본값 0. pop(키)은 입차 시각을 꺼내 삭제. 이번 주차 시간 누적.
#     for car, time in entered.items():  # items()는 (키,값) 제공. 출차 기록이 없는 차량 순회.
#         totals[car] = totals.get(car, 0) + 1439 - time  # 23:59인 1439분에 출차한 것으로 주차 시간 추가.
#     base_time, base_fee, unit_time, unit_fee = fees  # 요금표 네 값을 각각 언패킹.
#     answer = []  # []는 빈 결과 리스트.
#     for car in sorted(totals):  # sorted는 정렬된 새 목록. 길이 4의 차량번호 문자열을 오름차순 순회.
#         extra = max(0, totals[car] - base_time)  # max는 최댓값. 기본 시간을 넘는 부분만 0 이상으로 계산.
#         answer.append(base_fee + (extra + unit_time - 1) // unit_time * unit_fee)  # //는 정수 몫. 단위 시간 올림 나눗셈으로 추가 요금 계산, append로 저장.
#     return answer  # return으로 차량번호 순 요금 목록 반환.

# 풀이 요약
# 입출차를 짝지어 차량별 총 시간을 모으고, 미출차는 23:59로 마감합니다. 기본 초과 시간에만 단위 요금을 올림 적용합니다.
# 예: 총 334분이면 5000+ceil(154/10)×600=14600. 기록 R개·차량 C대일 때 시간 O(R+C log C), 공간 O(C).
