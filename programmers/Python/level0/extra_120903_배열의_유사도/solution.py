def solution(s1, s2):
    return len(set(s1) & set(s2))

# 전체 코드 줄별 설명
# def solution(s1, s2):  # def는 함수 정의. 중복 없는 두 문자열 리스트 입력.
#     return len(set(s1) & set(s2))  # set은 중복 없는 집합, &는 교집합, len은 원소 개수. 공통 원소 수 반환.

# 풀이 요약
# 두 집합에 모두 포함된 원소의 개수를 구합니다.
# 