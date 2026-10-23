from math import gcd
from functools import reduce

def solution(arrayA, arrayB):
    a = reduce(gcd, arrayA)
    b = reduce(gcd, arrayB)
    if any(value % a == 0 for value in arrayB):
        a = 0
    if any(value % b == 0 for value in arrayA):
        b = 0
    return max(a, b)

# 전체 코드 줄별 설명
# from math import gcd  # math 모듈에서 gcd를 import. gcd(a,b)는 두 정수의 최대공약수 반환.
# from functools import reduce  # functools의 reduce는 이항 함수를 목록에 누적 적용하는 함수.
# 
# def solution(arrayA, arrayB):  # def는 함수 정의, () 안은 두 사람의 카드 숫자 목록.
#     a = reduce(gcd, arrayA)  # gcd를 누적 적용해 A 전체의 최대공약수 계산.
#     b = reduce(gcd, arrayB)  # B 전체의 최대공약수 계산. =는 대입.
#     if any(value % a == 0 for value in arrayB):  # any는 하나라도 참인지 검사. %는 나머지, ==는 같음. B 카드 중 a로 나누어지는 수 검사.
#         a = 0  # 반대쪽 카드 하나라도 나누면 A의 후보를 제외.
#     if any(value % b == 0 for value in arrayA):  # 생성식 for로 A의 카드도 b로 나누어지는지 검사.
#         b = 0  # B의 후보도 같은 방식으로 제외.
#     return max(a, b)  # max는 최댓값. return으로 유효 후보 중 큰 수 또는 0 반환.

# 풀이 요약
# 한쪽 전체를 나누는 최대 후보는 최대공약수입니다. 그것이 반대쪽 카드 하나를 나누면 그 약수들도 그 카드를 나누므로 모두 불가능합니다.
# 예: A=[14,35,119]의 최대공약수 7은 B의 어떤 수도 나누지 않아 답 7. 카드 N개·최댓값 V일 때 시간 O(N log V), 추가 공간 O(1).
