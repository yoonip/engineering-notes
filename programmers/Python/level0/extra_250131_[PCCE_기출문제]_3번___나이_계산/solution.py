year = int(input())
age_type = input()
if age_type == "Korea":
    answer = 2030 - year + 1
elif age_type == "Year":
    answer = 2030 - year
print(answer)

# 전체 코드 줄별 설명
# year = int(input())  # input은 입력, int는 정수 변환. 출생 연도 입력.
# age_type = input()  # 나이 종류를 문자열로 입력.
# if age_type == "Korea":  # if는 조건, ==는 같음 비교. 한국식 나이인지 확인.
#     answer = 2030 - year + 1  # 현재 연도에서 출생 연도를 빼고 1을 더함.
# elif age_type == "Year":  # elif는 다음 조건 검사. 연 나이인지 확인.
#     answer = 2030 - year  # 연 나이는 연도 차이만 계산.
# print(answer)  # print로 계산한 나이 출력.

# 풀이 요약
# 한국식 나이는 연도 차이+1, 연 나이는 연도 차이입니다. 기준 연도는 문제에서 정한 2030입니다.
# 