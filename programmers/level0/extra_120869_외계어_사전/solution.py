def solution(spell, dic):
    target = sorted(spell)
    return 1 if any(sorted(word) == target for word in dic) else 2

# 전체 코드 줄별 설명
# def solution(spell, dic):  # def는 함수 정의. 사용할 문자 리스트와 단어 사전 입력.
#     target = sorted(spell)  # sorted는 정렬. 모든 문자를 한 번씩 쓴 기준 목록 생성.
#     return 1 if any(sorted(word) == target for word in dic) else 2  # any는 하나라도 참인지 검사. 각 단어의 문자와 개수가 기준과 같은지 비교.

# 풀이 요약
# 정렬한 문자 목록이 같으면 각 글자를 정확히 한 번씩 모두 사용한 단어입니다.
# 