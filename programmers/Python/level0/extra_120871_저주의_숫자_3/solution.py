def solution(n):
    value = 0
    for _ in range(n):
        value += 1
        while value % 3 == 0 or '3' in str(value):
            value += 1
    return value

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 3x 마을 숫자로 바꿀 순번 입력.
#     value = 0  # 실제로 사용할 숫자 초기화.
#     for _ in range(n):  # range는 n번 반복, _는 사용하지 않는 반복 변수.
#         value += 1  # +=는 더해 저장. 다음 숫자로 이동.
#         while value % 3 == 0 or '3' in str(value):  # while은 반복, %는 나머지, or는 하나라도 참. 3의 배수이거나 숫자 3 포함이면 제외.
#             value += 1  # 금지 숫자를 건너뛰어 다음 후보 검사.
#     return value  # 금지 조건을 피한 n번째 숫자 반환.

# 풀이 요약
# 숫자를 하나씩 증가시키면서 3의 배수와 3을 포함한 수를 모두 건너뜁니다.
# 