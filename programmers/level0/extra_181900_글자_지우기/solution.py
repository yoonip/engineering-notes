def solution(my_string, indices):
    removed = set(indices)
    return ''.join(char for i, char in enumerate(my_string) if i not in removed)

# 전체 코드 줄별 설명
# def solution(my_string, indices):  # def는 함수 정의. 문자열과 지울 인덱스 리스트 입력.
#     removed = set(indices)  # set은 중복 없는 집합. 삭제 인덱스를 빠르게 조회하도록 변환.
#     return ''.join(char for i, char in enumerate(my_string) if i not in removed)  # enumerate는 위치와 문자 제공, not in은 집합에 없음 검사, join은 남긴 문자 연결.

# 풀이 요약
# 지울 위치를 집합으로 만들고 해당 위치를 제외한 문자만 원래 순서대로 연결합니다.
# 