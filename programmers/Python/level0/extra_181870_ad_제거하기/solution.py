def solution(strArr):
    return [text for text in strArr if 'ad' not in text]

# 전체 코드 줄별 설명
# def solution(strArr):  # def는 함수 정의. 문자열 리스트 입력.
#     return [text for text in strArr if 'ad' not in text]  # 리스트 내포의 for는 순회, if는 필터, not in은 부분 문자열이 없음 검사.

# 풀이 요약
# ad가 포함되지 않은 문자열만 순서를 유지해 남깁니다.
# 