def solution(before, after):
    return int(sorted(before) == sorted(after))

# 전체 코드 줄별 설명
# def solution(before, after):  # def는 함수 정의. 순서를 바꾸기 전과 목표 문자열 입력.
#     return int(sorted(before) == sorted(after))  # sorted는 각 문자열의 문자를 정렬한 리스트 반환. ==로 문자와 개수 일치 비교, int로 1·0 반환.

# 풀이 요약
# 문자 순서를 바꿔 만들 수 있으려면 각 문자의 개수가 같아야 합니다. 정렬하면 이를 비교할 수 있습니다.
# 