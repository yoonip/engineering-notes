# 문자열 내 마음대로 정렬하기
# 분류: 튜플 정렬 키
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12915
# 선택 이유: n번째 글자와 문자열 자체를 튜플 키로 지정해 동률까지 한 번의 정렬로 처리한다.
# 비용: 문자열 N개, 최대 길이 L: 최악 시간 O(NL log N), 추가 공간 O(N).

def solution(strings, n):
    return sorted(strings, key=lambda word: (word[n], word))
