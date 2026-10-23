def solution(my_string, overwrite_string, s):
    return my_string[:s] + overwrite_string + my_string[s + len(overwrite_string):]

# 전체 코드 줄별 설명
# def solution(my_string, overwrite_string, s):  # def는 함수 정의. 원본·덮을 문자열·시작 인덱스를 입력받음.
#     return my_string[:s] + overwrite_string + my_string[s + len(overwrite_string):]  # [:s]는 시작 전 부분, len은 길이, [끝:]는 덮는 구간 뒤의 부분. +로 앞·대체·뒤를 연결.

# 풀이 요약
# 교체 범위 바깥의 앞뒤 부분은 슬라이싱으로 보존하고 가운데를 새 문자열로 바꿉니다.
# 