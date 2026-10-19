from itertools import permutations
from math import isqrt

def solution(numbers):
    candidates = set()
    for size in range(1, len(numbers) + 1):
        candidates.update(int(''.join(parts)) for parts in permutations(numbers, size))
    answer = 0
    for value in candidates:
        if value >= 2 and all(value % divisor for divisor in range(2, isqrt(value) + 1)):
            answer += 1
    return answer

# 전체 코드 줄별 설명
# from itertools import permutations  # itertools의 permutations를 import. 주어진 길이의 숫자 조각 순열 생성.
# from math import isqrt  # math의 isqrt는 정수 제곱근의 내림값 반환.
# 
# def solution(numbers):  # def는 함수 정의, numbers는 한 자리 숫자 조각 문자열 입력.
#     candidates = set()  # set은 중복 없는 집합. 조각으로 만든 정수 후보 저장.
#     for size in range(1, len(numbers) + 1):  # len은 길이, range는 끝 미포함. 사용할 조각 개수를 1부터 전체까지 순회.
#         candidates.update(int(''.join(parts)) for parts in permutations(numbers, size))  # join은 문자 연결, int는 정수 변환. update는 여러 후보 추가. 선행 0·중복 순열은 집합에서 통합.
#     answer = 0  # =는 대입. 서로 다른 소수 개수 초기화.
#     for value in candidates:  # 중복 제거한 정수 후보 순회.
#         if value >= 2 and all(value % divisor for divisor in range(2, isqrt(value) + 1)):  # >=는 이상, and는 둘 다 참, %는 나머지. all로 제곱근 이하 약수가 없는지 검사.
#             answer += 1  # +=는 더해 저장. 소수 개수 증가.
#     return answer  # return으로 만들 수 있는 서로 다른 소수 수 반환.

# 풀이 요약
# 모든 길이의 순열로 정수 후보를 만들고 집합으로 중복을 제거합니다. 2 이상이면서 제곱근까지 약수가 없으면 소수입니다.
# 예: '011'은 11·101 두 소수. 생성 순열 수 T·고유 후보 U·최댓값 V일 때 시간 O(T*N+U√V), 공간 O(U+N).
