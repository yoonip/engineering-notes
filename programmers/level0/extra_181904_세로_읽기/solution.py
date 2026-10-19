def solution(my_string, m, c):
    return my_string[c - 1::m]

# 전체 코드 줄별 설명
# def solution(my_string, m, c):  # def는 함수 정의. 문자열·한 줄 글자 수·열 번호 입력.
#     return my_string[c - 1::m]  # [시작:끝:간격]은 슬라이싱. 1부터 시작하는 열 c를 인덱스 c-1로 바꾸고 m칸 간격으로 추출.

# 풀이 요약
# 같은 열의 글자는 문자열에서 m칸 간격으로 나타납니다.
# 