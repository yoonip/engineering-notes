def solution(strings, n):
    return sorted(strings, key=lambda word: (word[n], word))

# 전체 코드 줄별 설명
# def solution(strings, n):  # def는 함수 정의. 문자열 리스트와 정렬할 글자 인덱스 입력.
#     return sorted(strings, key=lambda word: (word[n], word))  # sorted는 정렬, lambda는 익명 기준 함수. 튜플의 첫 기준은 n번째 문자, 같으면 전체 단어 사전순.

# 풀이 요약
# 정렬 키를 (지정 문자,전체 문자열)로 만들면 동률일 때의 사전순 조건도 반영됩니다.
# 