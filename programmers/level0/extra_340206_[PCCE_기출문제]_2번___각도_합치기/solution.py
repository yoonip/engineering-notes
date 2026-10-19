angle1 = int(input())
angle2 = int(input())
sum_angle = (angle1 + angle2) %360
print(sum_angle)

# 전체 코드 줄별 설명
# angle1 = int(input())  # int는 정수 변환. input은 한 줄의 문자열 입력. =는 값 저장. 첫 각도를 정수로 입력받음.
# angle2 = int(input())  # int는 정수 변환. input은 한 줄의 문자열 입력. =는 값 저장. 둘째 각도를 정수로 입력받음.
# sum_angle = (angle1 + angle2) %360  # %는 나머지. =는 값 저장. 각도의 합을 한 바퀴 360도로 나눈 나머지로 바꿈.
# print(sum_angle)  # print는 값을 표준 출력에 표시. 0도 이상 360도 미만인 결과 출력.

# 풀이 요약
# 두 각도를 더한 뒤 360으로 나눈 나머지를 구한다. 완전한 한 바퀴를 제거하면 같은 방향을 나타내는 0~359도의 각도가 남는다. 예를 들어 280+100은 380이고 결과는 20이다.
# 문제의 정수 범위에서 시간·보조 공간 O(1).
