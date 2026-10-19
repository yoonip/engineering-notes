def solution(my_string, index_list):
    return ''.join(my_string[i] for i in index_list)

# 전체 코드 줄별 설명
# def solution(my_string, index_list):  # def는 함수 정의. 원본 문자열과 글자 위치 리스트 입력.
#     return ''.join(my_string[i] for i in index_list)  # []는 인덱스 접근. 생성기 표현식으로 지정 글자를 순서대로 꺼내 join으로 연결.

# 풀이 요약
# 인덱스가 가리키는 문자를 주어진 순서 그대로 연결합니다.
# 