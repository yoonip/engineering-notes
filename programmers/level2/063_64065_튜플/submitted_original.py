from collections import Counter
from re import findall

def solution(s):
    counts = Counter(findall(r'\d+', s))
    return [int(value) for value, count in counts.most_common()]

# 전체 코드 줄별 설명
# from collections import Counter  # collections의 Counter를 import. 숫자 문자열별 등장 횟수를 집계하는 자료구조.
# from re import findall  # re는 정규식 모듈. findall은 패턴에 맞는 모든 문자열 조각 반환.
# 
# def solution(s):  # def는 함수 정의, s는 중첩 집합 표현 문자열 입력.
#     counts = Counter(findall(r'\d+', s))  # r은 원시 문자열, 정규식 \d+는 연속된 숫자 한 개 이상. 숫자들을 추출해 횟수 집계.
#     return [int(value) for value, count in counts.most_common()]  # most_common은 횟수 내림차순 (원소,횟수) 목록. 리스트 내포로 언패킹하고 int로 정수 변환해 반환.

# 풀이 요약
# 튜플 첫 원소는 모든 집합에, 둘째는 첫 집합을 제외한 곳에 등장합니다. 등장 횟수가 많은 순서가 튜플 순서입니다.
# 예: 2·1·3·4가 각각 4·3·2·1번 등장하면 [2,1,3,4]. 문자열 길이 L·원소 U개일 때 시간 O(L+U log U), 공간 O(L).
