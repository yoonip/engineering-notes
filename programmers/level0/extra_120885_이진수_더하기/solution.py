def solution(bin1, bin2):
    return bin(int(bin1, 2) + int(bin2, 2))[2:]

# 전체 코드 줄별 설명
# def solution(bin1, bin2):  # def는 함수 정의. 두 이진수 문자열 입력.
#     return bin(int(bin1, 2) + int(bin2, 2))[2:]  # int(문자열,2)는 이진수 해석. bin은 합계를 0b 접두사가 있는 이진 문자열로 변환, [2:]로 접두사 제거.

# 풀이 요약
# 두 이진수를 정수로 바꿔 더한 뒤 이진 문자열로 다시 바꿉니다.
# 