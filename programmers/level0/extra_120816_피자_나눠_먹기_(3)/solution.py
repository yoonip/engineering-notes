def solution(slice, n):
    return (n + slice - 1) // slice

# 전체 코드 줄별 설명
# def solution(slice, n):  # def는 함수 정의. 한 판의 조각 수와 사람 수 입력.
#     return (n + slice - 1) // slice  # //는 정수 나눗셈. 양수 나눗셈을 올림하는 공식 (분자+분모-1)//분모 사용.

# 풀이 요약
# 사람 수를 한 판의 조각 수로 나눈 값을 올림해야 모두 한 조각 이상 먹습니다.
# 