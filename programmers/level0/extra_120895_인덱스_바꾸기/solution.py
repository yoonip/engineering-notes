def solution(my_string, num1, num2):
    chars = list(my_string)
    chars[num1], chars[num2] = chars[num2], chars[num1]
    return ''.join(chars)

# 전체 코드 줄별 설명
# def solution(my_string, num1, num2):  # def는 함수 정의. 문자열과 교환할 두 인덱스 입력.
#     chars = list(my_string)  # list는 문자열을 수정 가능한 문자 리스트로 변환.
#     chars[num1], chars[num2] = chars[num2], chars[num1]  # 다중 대입으로 오른쪽 두 값을 먼저 읽어 위치를 맞바꿈.
#     return ''.join(chars)  # join은 문자 리스트를 문자열로 연결. return은 결과 반환.

# 풀이 요약
# 문자열을 리스트로 바꾸어 두 위치를 교환한 뒤 다시 문자열로 만듭니다.
# 