def solution(my_string):
    return sorted(int(char) for char in my_string if char.isdigit())

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 숫자와 소문자가 섞인 문자열 입력.
#     return sorted(int(char) for char in my_string if char.isdigit())  # isdigit으로 숫자 문자만 선택, int로 정수 변환, sorted로 오름차순 정렬한 리스트 반환.

# 풀이 요약
# 문자열에서 한 자리 숫자를 골라 정수로 바꾼 뒤 정렬합니다.
# 