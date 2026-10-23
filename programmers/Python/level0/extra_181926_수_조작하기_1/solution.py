def solution(n, control):
    changes = {'w': 1, 's': -1, 'd': 10, 'a': -10}
    return n + sum(changes[char] for char in control)

# 전체 코드 줄별 설명
# def solution(n, control):  # def는 함수 정의. 시작 정수와 조작 문자열 입력.
#     changes = {'w': 1, 's': -1, 'd': 10, 'a': -10}  # {키:값}은 딕셔너리. 각 문자에 해당하는 증감량 저장.
#     return n + sum(changes[char] for char in control)  # []로 문자에 해당하는 값 조회. 생성기 표현식의 증감량들을 sum으로 합산하고 초기값에 더함.

# 풀이 요약
# 모든 조작은 덧셈이므로 문자별 증감량을 합쳐 한 번에 더할 수 있습니다.
# 