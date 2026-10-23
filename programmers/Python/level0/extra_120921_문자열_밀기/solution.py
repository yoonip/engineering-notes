def solution(A, B):
    for count in range(len(A)):
        if A == B:
            return count
        A = A[-1] + A[:-1]
    return -1

# 전체 코드 줄별 설명
# def solution(A, B):  # def는 함수 정의. 회전할 문자열과 목표 문자열 입력.
#     for count in range(len(A)):  # len은 길이, range는 0부터 길이-1까지 정수 생성. 가능한 최소 회전 횟수부터 검사.
#         if A == B:  # if는 조건, ==는 문자열 같음 비교.
#             return count  # 처음 일치한 횟수가 최소이므로 즉시 반환.
#         A = A[-1] + A[:-1]  # -1은 마지막 문자, [:-1]은 마지막 전까지의 슬라이싱. 마지막 문자를 맨 앞으로 옮김.
#     return -1  # 한 바퀴 안에 일치하지 않으면 만들 수 없으므로 -1 반환.

# 풀이 요약
# 오른쪽으로 한 칸씩 회전해 목표 문자열과 처음 같아지는 횟수를 찾습니다.
# 