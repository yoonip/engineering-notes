a, b = map(int, input().split())
print(f"{a} + {b} = {a + b}")

# 전체 코드 줄별 설명
# a, b = map(int, input().split())  # input은 입력, split은 공백 분리, map(int, ...)는 각 항목 정수 변환. 두 변수에 나누어 저장.
# print(f"{a} + {b} = {a + b}")  # f 문자열의 {}에는 변수나 계산식 삽입. print로 숫자·연산 기호·합계 출력.

# 풀이 요약
# 덧셈은 실제로 계산하고, 식의 기호와 공백은 문자열로 출력합니다.
# 