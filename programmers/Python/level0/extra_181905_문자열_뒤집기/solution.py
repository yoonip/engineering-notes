def solution(my_string, s, e):
    return my_string[:s] + my_string[s:e + 1][::-1] + my_string[e + 1:]

# 전체 코드 줄별 설명
# def solution(my_string, s, e):  # def는 함수 정의. 문자열과 뒤집을 양 끝 인덱스 입력.
#     return my_string[:s] + my_string[s:e + 1][::-1] + my_string[e + 1:]  # [:s]는 앞부분, [s:e+1]은 양 끝 포함 구간, [::-1]은 역순, +는 문자열 연결.

# 풀이 요약
# 앞뒤는 유지하고 가운데 구간만 역순으로 바꿔 연결합니다.
# 