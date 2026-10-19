def solution(elements):
    n = len(elements)
    doubled = elements * 2
    sums = set()
    for start in range(n):
        total = 0
        for end in range(start, start + n):
            total += doubled[end]
            sums.add(total)
    return len(sums)

# 전체 코드 줄별 설명
# def solution(elements):  # def는 함수 정의, elements는 원형 수열 목록 입력.
#     n = len(elements)  # len은 원소 수, =는 대입. 원래 수열 길이 저장.
#     doubled = elements * 2  # 리스트의 *2는 두 번 이어 붙이기. 원을 도는 구간을 직선 구간으로 표현.
#     sums = set()  # set()은 중복 없는 집합. 서로 다른 부분 합 저장.
#     for start in range(n):  # range(n)은 0~n-1. 모든 시작 인덱스 순회.
#         total = 0  # 현재 시작점의 부분 합 초기화.
#         for end in range(start, start + n):  # 끝 미포함 range로 길이 1부터 n까지 끝점을 늘림.
#             total += doubled[end]  # [end]는 원소 접근, +=는 더해 저장. 새 원소를 부분 합에 추가.
#             sums.add(total)  # add는 집합 원소 추가. 같은 합은 한 번만 저장.
#     return len(sums)  # return으로 서로 다른 합의 개수 반환.

# 풀이 요약
# 수열을 두 번 이어 붙이고 각 시작점에서 길이 1~N의 합을 누적해 집합에 넣습니다.
# 예: [7,9,1,1,4]에서 중복을 제거한 합은 18종류. 시간 O(N²), 합 집합의 최악 공간 O(N²).
