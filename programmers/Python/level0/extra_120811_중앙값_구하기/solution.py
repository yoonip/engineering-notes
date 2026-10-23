def solution(array):
    return sorted(array)[len(array) // 2]

# 전체 코드 줄별 설명
# def solution(array):  # def는 함수 정의. 길이가 홀수인 정수 리스트 입력.
#     return sorted(array)[len(array) // 2]  # sorted는 오름차순 정렬, len은 개수, //2는 가운데 인덱스. []로 중앙 원소 조회.

# 풀이 요약
# 정렬 후 0부터 세는 가운데 인덱스의 값을 가져옵니다.
# 