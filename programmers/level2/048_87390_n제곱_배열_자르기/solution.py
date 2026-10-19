def solution(n, left, right):
    answer = []
    for index in range(left, right + 1):
        row, column = divmod(index, n)
        answer.append(max(row, column) + 1)
    return answer

# 전체 코드 줄별 설명
# def solution(n, left, right):  # def는 함수 정의. () 안은 한 변 길이·남길 시작·끝 인덱스.
#     answer = []  # []는 빈 리스트. 필요한 구간 값만 저장.
#     for index in range(left, right + 1):  # range는 끝 미포함. +1로 right 인덱스까지 포함.
#         row, column = divmod(index, n)  # divmod는 몫·나머지 반환. 펼친 인덱스를 0부터인 행·열로 언패킹.
#         answer.append(max(row, column) + 1)  # max는 최댓값. 행·열 중 큰 번호+1을 append로 결과 끝에 추가.
#     return answer  # return으로 잘라낸 구간 리스트 반환.

# 풀이 요약
# 0부터인 (행,열)의 값은 max(행,열)+1입니다. 전체 n² 배열을 만들지 않고 필요한 인덱스만 행·열로 바꿉니다.
# 예: n=3의 인덱스 2~5는 [3,2,2,3]. 구간 길이 L일 때 시간·결과 공간 O(L).
