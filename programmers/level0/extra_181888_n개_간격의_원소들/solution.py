def solution(num_list, n):
    return num_list[::n]

# 전체 코드 줄별 설명
# def solution(num_list, n):  # def는 함수 정의. 리스트와 추출 간격 입력.
#     return num_list[::n]  # [시작:끝:간격] 슬라이싱. 시작·끝을 생략해 처음부터 끝까지 n칸 간격 추출.

# 풀이 요약
# 인덱스 0, n, 2n 위치의 원소를 가져옵니다.
# 