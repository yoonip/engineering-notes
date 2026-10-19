def solution(arr):
    return sum(arr) / len(arr)

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. arr는 정수 리스트를 받는 매개변수입니다.
#     return sum(arr) / len(arr)  # return은 결과를 돌려주고 함수 종료. len은 길이. sum은 원소 합. sum()으로 합을 구하고 len()으로 개수를 구해 나눈 뒤 반환합니다.

# 풀이 요약
# 모든 원소의 합을 원소 수로 나눈다. 평균은 소수일 수 있으므로 정수 몫 //가 아니라 일반 나눗셈 /를 사용한다.
# 원소 N개: 시간 O(N), 보조 공간 O(1).
