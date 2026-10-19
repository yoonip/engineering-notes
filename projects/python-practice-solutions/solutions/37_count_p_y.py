# 문자열 내 p와 y의 개수
# 분류: 대소문자 정규화 / 개수 집계
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12916
# 선택 이유: 소문자로 통일한 뒤 p와 y를 각각 센다. 두 번의 순회도 전체 길이에 비례한다.
# 비용: 문자열 길이 L: 시간 O(L), 추가 공간 O(L). lower가 새 문자열을 만든다.

def solution(s):
    s = s.lower()
    return s.count("p") == s.count("y")
