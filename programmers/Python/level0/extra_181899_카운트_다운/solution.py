def solution(start_num, end_num):
    return list(range(start_num, end_num - 1, -1))

# 전체 코드 줄별 설명
# def solution(start_num, end_num):  # def는 함수 정의. 시작값과 끝값 입력.
#     return list(range(start_num, end_num - 1, -1))  # range의 간격 -1은 감소 수열. 끝은 제외하므로 end_num-1 사용, list로 변환.

# 풀이 요약
# 간격을 -1로 지정해 양 끝을 포함하는 감소 수열을 만듭니다.
# 