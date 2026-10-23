def solution(n, k):
    return list(range(k, n + 1, k))

# 전체 코드 줄별 설명
# def solution(n, k):  # def는 함수 정의. 상한과 배수 기준 입력.
#     return list(range(k, n + 1, k))  # range(시작,끝,간격)는 끝 제외 정수 수열. k부터 k씩 증가한 수를 list로 변환.

# 풀이 요약
# 양의 k의 배수는 k, 2k, 3k 순서입니다.
# 