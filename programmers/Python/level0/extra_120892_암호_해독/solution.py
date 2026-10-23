def solution(cipher, code):
    return cipher[code - 1::code]

# 전체 코드 줄별 설명
# def solution(cipher, code):  # def는 함수 정의. 암호 문자열과 추출할 순번의 배수 입력.
#     return cipher[code - 1::code]  # [시작::간격]은 슬라이싱. code번째 문자의 인덱스 code-1부터 code칸 간격 추출.

# 풀이 요약
# 문자 순번은 1부터지만 인덱스는 0부터이므로 첫 위치에 1을 뺍니다.
# 