n = int(input())
print(f"{n} is even" if n % 2 == 0 else f"{n} is odd")

# 전체 코드 줄별 설명
# n = int(input())  # input은 문자열 입력, int는 정수 변환.
# print(f"{n} is even" if n % 2 == 0 else f"{n} is odd")  # %는 나머지, ==는 같음 비교. 조건 표현식으로 짝수·홀수 문장을 골라 출력.

# 풀이 요약
# 2로 나눈 나머지가 0이면 짝수, 1이면 홀수입니다.
# 