def solution(common):
    if common[1] - common[0] == common[2] - common[1]:
        return common[-1] + common[1] - common[0]
    return common[-1] * (common[1] // common[0])

# 전체 코드 줄별 설명
# def solution(common):  # def는 함수 정의. 등차수열 또는 등비수열 입력.
#     if common[1] - common[0] == common[2] - common[1]:  # []는 인덱스 접근, ==는 같음 비교. 첫 두 차이가 같은지 확인.
#         return common[-1] + common[1] - common[0]  # -1은 마지막 원소. 등차수열의 공차를 마지막 값에 더함.
#     return common[-1] * (common[1] // common[0])  # *는 곱셈, //는 정수 나눗셈. 등비수열의 정수 공비를 마지막 값에 곱함.

# 풀이 요약
# 앞 세 항의 차이가 같으면 등차수열이고, 아니면 등비수열입니다.
# 