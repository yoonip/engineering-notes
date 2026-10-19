# 문제: 파일명 정렬
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/17686
# 풀이: 정규식으로 HEAD와 최대 다섯 자리 NUMBER를 나눈다. 소문자 HEAD·정수 NUMBER를 키로 안정 정렬해 동률의 입력 순서를 유지한다.
# 복잡도: 파일 N개·최대 길이 L: 시간 O(NL log N), 추가 공간 O(NL). 같은 키의 원래 순서를 유지한다.

from re import match

def solution(files):
    def key(filename):
        head, number = match(r'(\D+)(\d{1,5})', filename).groups()
        return (head.lower(), int(number))
    return sorted(files, key=key)
