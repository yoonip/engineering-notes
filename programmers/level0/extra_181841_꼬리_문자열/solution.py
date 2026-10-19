def solution(str_list, ex):
    return ''.join(text for text in str_list if ex not in text)

# 전체 코드 줄별 설명
# def solution(str_list, ex):  # def는 함수 정의. 문자열 리스트와 제외할 부분 문자열 입력.
#     return ''.join(text for text in str_list if ex not in text)  # not in은 부분 문자열 없음 검사. 생성기 표현식에서 조건에 맞는 문자열만 골라 join으로 연결.

# 풀이 요약
# 제외 문구가 없는 문자열만 원래 순서대로 이어 붙입니다.
# 