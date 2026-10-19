def solution(num_list):
    odd = ''.join(str(x) for x in num_list if x % 2 == 1)
    even = ''.join(str(x) for x in num_list if x % 2 == 0)
    return int(odd) + int(even)

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 한 자리 정수 리스트 입력.
#     odd = ''.join(str(x) for x in num_list if x % 2 == 1)  # %는 나머지, if는 홀수 필터, str은 문자열 변환, join은 순서대로 연결.
#     even = ''.join(str(x) for x in num_list if x % 2 == 0)  # 짝수만 골라 문자열로 변환하고 연결.
#     return int(odd) + int(even)  # int로 각각 정수로 바꾼 후 숫자 덧셈.

# 풀이 요약
# 홀수와 짝수를 각자 원래 순서대로 연결한 뒤 두 정수의 합을 구합니다.
# 