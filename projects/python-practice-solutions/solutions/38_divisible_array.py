# 나누어 떨어지는 숫자 배열
# 분류: 조건 필터 / 정렬
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12910
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(arr, divisor):
    answer = []
    for num in arr:
        if num % divisor == 0:
            answer.append(num)
    if not answer:
        return [-1]
    return sorted(answer)


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(arr, divisor):       # 숫자 배열 arr와 나눌 수 divisor를 입력받습니다.
#     answer = []                  # 조건에 맞는 숫자를 담을 빈 리스트를 만듭니다.
#     for num in arr:              # arr의 숫자를 하나씩 num에 넣어 반복합니다.
#         if num % divisor == 0:   # %는 나머지입니다. 나머지가 0이면 나누어떨어집니다.
#             answer.append(num)   # append()로 해당 숫자를 리스트 끝에 추가합니다.
#     if not answer:               # answer가 빈 리스트이면 실행합니다.
#         return [-1]              # 숫자가 없으면 -1을 담은 리스트를 반환합니다.
#     return sorted(answer)        # sorted()로 오름차순 정렬한 리스트를 반환합니다.
