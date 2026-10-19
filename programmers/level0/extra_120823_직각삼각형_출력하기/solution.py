n = int(input())
for width in range(1, n + 1):
    print('*' * width)

# 전체 코드 줄별 설명
# n = int(input())  # input은 한 줄 입력, int는 정수 변환. 삼각형 높이 저장.
# for width in range(1, n + 1):  # for는 반복, range는 1부터 n까지 순회. 각 행의 별 개수를 증가시킴.
#     print('*' * width)  # 문자열 * 정수는 반복. print는 별을 출력하고 줄바꿈.

# 풀이 요약
# 첫 행부터 별을 1개,2개 순서로 늘려 n개까지 출력합니다.
# 