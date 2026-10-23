a, b = map(int, input().split())
print(f"a = {a}")
print(f"b = {b}")

# 전체 코드 줄별 설명
# a, b = map(int, input().split())  # input은 한 줄 입력, split은 공백으로 분리, map(int, ...)는 각각 정수로 변환. 두 변수에 나누어 저장.
# print(f"a = {a}")  # f 문자열은 중괄호 안 표현식의 값을 삽입. print로 이름과 값 출력.
# print(f"b = {b}")  # 두 번째 변수도 요구된 형식과 공백에 맞춰 출력.

# 풀이 요약
# 두 정수를 입력받아 각각 a = 값, b = 값 형식으로 출력합니다.
# 