def solution(myStr):
    separated = myStr.replace('a', ' ').replace('b', ' ').replace('c', ' ')
    return separated.split() or ['EMPTY']

# 전체 코드 줄별 설명
# def solution(myStr):  # def는 함수 정의. a·b·c로 나눌 문자열 입력.
#     separated = myStr.replace('a', ' ').replace('b', ' ').replace('c', ' ')  # replace는 문자열 치환. 세 구분자를 모두 공백으로 바꿔 통일.
#     return separated.split() or ['EMPTY']  # split()은 연속 공백과 빈 조각을 무시하고 분리. or는 결과가 비어 있으면 EMPTY 리스트 선택.

# 풀이 요약
# 구분자를 공백 하나로 통일하면 split으로 빈 조각 없이 나눌 수 있습니다.
# 