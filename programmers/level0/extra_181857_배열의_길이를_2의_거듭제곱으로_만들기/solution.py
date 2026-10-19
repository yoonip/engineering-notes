def solution(arr):
    size = 1
    while size < len(arr):
        size *= 2
    return arr + [0] * (size - len(arr))

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 정수 리스트 입력.
#     size = 1  # 2의 0제곱부터 목표 길이 시작.
#     while size < len(arr):  # while은 조건 반복, len은 길이. 현재 길이 이상인 거듭제곱을 찾음.
#         size *= 2  # *=는 곱해 저장. 1,2,4,8 순서로 목표 길이 증가.
#     return arr + [0] * (size - len(arr))  # 부족한 길이만큼 0 리스트를 만들어 +로 뒤에 연결.

# 풀이 요약
# 현재 길이 이상인 가장 작은 2의 거듭제곱을 찾고 그 차이만큼 0을 추가합니다.
# 