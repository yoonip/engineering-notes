def solution(array, height):
    return sum(value > height for value in array)

# 전체 코드 줄별 설명
# def solution(array, height):  # def는 함수 정의. 친구들 키 리스트와 기준 키 입력.
#     return sum(value > height for value in array)  # >는 초과 비교. 생성기 표현식으로 더 큰 키인지 검사하고 sum으로 참의 개수 합산.

# 풀이 요약
# 같은 키는 제외하고 기준 키보다 큰 사람만 셉니다.
# 