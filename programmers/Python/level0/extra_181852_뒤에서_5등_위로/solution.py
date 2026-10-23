def solution(num_list):
    return sorted(num_list)[5:]

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     return sorted(num_list)[5:]  # sorted는 오름차순 정렬, [5:]는 앞 5개를 제외한 나머지 슬라이싱.

# 풀이 요약
# 가장 작은 다섯 개를 제외하려면 정렬 후 인덱스 5부터 가져옵니다.
# 