def solution(x1, x2, x3, x4):
    return (x1 or x2) and (x3 or x4)

# 전체 코드 줄별 설명
# def solution(x1, x2, x3, x4):  # def는 함수 정의. 네 참·거짓 값 입력.
#     return (x1 or x2) and (x3 or x4)  # or는 하나라도 참, and는 모두 참. 괄호로 두 OR 조건을 먼저 계산.

# 풀이 요약
# 논리합 기호 ∨는 or, 논리곱 기호 ∧는 and에 대응합니다.
# 