def solution(my_str, n):
    return [my_str[i:i + n] for i in range(0, len(my_str), n)]

# 전체 코드 줄별 설명
# def solution(my_str, n):  # def는 함수 정의. 문자열과 조각 길이 입력.
#     return [my_str[i:i + n] for i in range(0, len(my_str), n)]  # range의 간격 n으로 시작 위치 순회. 슬라이싱으로 n글자씩 추출하는 리스트 내포. 마지막 짧은 조각도 유지.

# 풀이 요약
# 시작 위치를 n칸씩 옮기며 길이 n의 부분 문자열을 자릅니다.
# 