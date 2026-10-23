def solution(i, j, k):
    digit = str(k)
    return sum(str(value).count(digit) for value in range(i, j + 1))

# 전체 코드 줄별 설명
# def solution(i, j, k):  # def는 함수 정의. 범위 양 끝과 셀 숫자 입력.
#     digit = str(k)  # str은 정수를 숫자 문자열로 변환.
#     return sum(str(value).count(digit) for value in range(i, j + 1))  # range는 양 끝 포함 범위 순회, count는 문자 출현 횟수, sum은 모든 수의 횟수 합산.

# 풀이 요약
# 범위 안 각 정수의 문자열에서 k가 나온 횟수를 더합니다. 같은 수의 중복 자릿수도 셉니다.
# 