def solution(my_string):
    return sorted(my_string[i:] for i in range(len(my_string)))

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 접미사를 구할 문자열 입력.
#     return sorted(my_string[i:] for i in range(len(my_string)))  # len은 길이, range는 인덱스 순회, [i:]는 i부터 끝까지. sorted는 접미사들을 사전순 정렬.

# 풀이 요약
# 모든 시작 인덱스의 접미사를 만들어 사전순으로 정렬합니다.
# 