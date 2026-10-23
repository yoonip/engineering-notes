def solution(strArr):
    counts = [0] * 31
    for text in strArr:
        counts[len(text)] += 1
    return max(counts)

# 전체 코드 줄별 설명
# def solution(strArr):  # def는 함수 정의. 문자열 리스트 입력.
#     counts = [0] * 31  # []는 리스트, *는 반복. 길이 1~30의 출현 횟수 저장 공간 초기화.
#     for text in strArr:  # for로 각 문자열 순회.
#         counts[len(text)] += 1  # len은 길이, []는 인덱스 접근. 해당 길이 그룹의 문자열 수 증가.
#     return max(counts)  # max는 최댓값. 가장 큰 그룹의 크기 반환.

# 풀이 요약
# 문자열의 내용이 아닌 길이를 기준으로 개수를 세고 최댓값을 구합니다.
# 