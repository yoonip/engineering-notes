def solution(str1, str2):
    return ''.join(a + b for a, b in zip(str1, str2))

# 전체 코드 줄별 설명
# def solution(str1, str2):  # def는 함수 정의. 길이가 같은 두 문자열 입력.
#     return ''.join(a + b for a, b in zip(str1, str2))  # zip은 같은 위치 문자를 묶음, for는 생성기 표현식, +는 문자 연결, join은 모두 이어 붙임.

# 풀이 요약
# 같은 위치의 문자 두 개를 먼저 붙인 뒤 그 쌍들을 순서대로 연결합니다.
# 