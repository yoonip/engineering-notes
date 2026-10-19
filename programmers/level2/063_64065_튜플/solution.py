# 문제: 튜플
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/64065
# 풀이: 숫자를 정규식으로 추출해 Counter로 센다. 앞선 튜플 원소일수록 더 자주 등장하는 성질로 순서를 복원한다.
# 복잡도: 문자열 길이 L·고유 원소 U개: 시간 O(L+U log U), 추가 공간 O(L).

from collections import Counter
from re import findall

def solution(s):
    counts = Counter(findall(r'\d+', s))
    return [int(value) for value, count in counts.most_common()]
