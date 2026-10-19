start = int(input())
before = int(input())
after = int(input())
money = start
month = 1
while money < 70:
    money += before
    month += 1
while money < 100:
    money += after
    month += 1
print(month)

# 전체 코드 줄별 설명
# start = int(input())  # input은 한 줄 입력, int는 정수 변환. 첫 달 저축액 입력.
# before = int(input())  # 70만 원 미만일 때의 월 저축액 입력.
# after = int(input())  # 70만 원 이상일 때의 월 저축액 입력.
# money = start  # 첫 달 저축 후 누적 금액 초기화.
# month = 1  # 첫 달을 이미 포함하므로 개월 수는 1부터 시작.
# while money < 70:  # while은 조건이 참인 동안 반복. <는 미만 비교.
#     money += before  # +=는 더해 저장. 70만 원까지 이전 저축액 사용.
#     month += 1  # 저축할 때마다 한 달 증가.
# while money < 100:  # 목표 100만 원에 도달할 때까지 반복.
#     money += after  # 증액된 월 저축액을 더함.
#     month += 1  # 소요 개월 수 증가.
# print(month)  # print로 목표 달성까지의 개월 수 출력.

# 풀이 요약
# 70 전에는 before, 이후에는 after를 더합니다. 첫 달도 한 달로 세며 예제는 12개월과 2개월입니다.
# 