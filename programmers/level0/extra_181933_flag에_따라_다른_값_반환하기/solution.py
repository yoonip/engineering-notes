def solution(a, b, flag):
    return a + b if flag else a - b

# 전체 코드 줄별 설명
# def solution(a, b, flag):  # def는 함수 정의. 두 정수와 불리언 True·False 입력.
#     return a + b if flag else a - b  # 조건 표현식은 조건이 참이면 앞 값, 거짓이면 뒤 값 선택. return으로 반환.

# 풀이 요약
# flag가 참이면 더하고 거짓이면 뺍니다.
# 