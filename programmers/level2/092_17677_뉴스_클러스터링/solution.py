# 문제: 뉴스 클러스터링
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/17677
# 풀이: 인접한 영문자 쌍을 Counter로 센다. 다중집합의 교집합은 최소 횟수, 합집합은 최대 횟수로 계산한다.
# 복잡도: 두 문자열 길이 합 L: 평균 시간 O(L), 추가 공간 O(min(L,26²)).

from collections import Counter

def solution(str1, str2):
    def pairs(text):
        text = text.lower()
        return Counter(text[i:i + 2] for i in range(len(text) - 1) if 'a' <= text[i] <= 'z' and 'a' <= text[i + 1] <= 'z')
    first, second = pairs(str1), pairs(str2)
    intersection = sum((first & second).values())
    union = sum((first | second).values())
    return 65536 if union == 0 else intersection * 65536 // union
