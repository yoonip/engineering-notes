a = int(input())
c = int(input())
b_square = c ** 2 - a ** 2
print(b_square)

# 전체 코드 줄별 설명
# a = int(input())  # input은 한 줄 입력, int는 정수 변환. 직각변 길이 저장.
# c = int(input())  # 빗변 길이를 입력받아 정수로 저장.
# b_square = c ** 2 - a ** 2  # **는 거듭제곱. 피타고라스 정리에서 다른 변 제곱은 빗변 제곱 빼기 주어진 변 제곱.
# print(b_square)  # print는 결과를 화면에 출력.

# 풀이 요약
# a²+b²=c²이므로 b²=c²-a²입니다. 제곱 계산 한 줄만 수정합니다.
# 