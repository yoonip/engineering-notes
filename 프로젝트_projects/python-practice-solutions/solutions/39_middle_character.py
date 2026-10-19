# 가운데 글자 가져오기
# 분류: 인덱스 / 슬라이싱
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12903
# 선택 이유: 가운데 인덱스를 구하고 길이의 홀짝에 따라 한 글자 또는 두 글자를 고른다.
# 비용: 가져오는 글자 수가 최대 2개라 시간 O(1), 추가 공간 O(1).

def solution(s):
    mid = len(s) // 2
    if len(s) % 2 == 0:
        return s[mid - 1:mid + 1]
    return s[mid]
