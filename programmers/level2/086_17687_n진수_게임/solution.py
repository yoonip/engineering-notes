def solution(n, t, m, p):
    digits = '0123456789ABCDEF'
    stream = []
    number = 0
    while len(stream) < t * m:
        value = number
        converted = '0' if value == 0 else ''
        while value:
            value, remainder = divmod(value, n)
            converted = digits[remainder] + converted
        stream.extend(converted)
        number += 1
    return ''.join(stream[p - 1:t * m:m])

# 전체 코드 줄별 설명
# def solution(n, t, m, p):  # def는 함수 정의. 진법·말할 개수·참가자 수·튜브 순서 입력.
#     digits = '0123456789ABCDEF'  # 진법의 각 자릿수를 대문자까지 표현할 문자열.
#     stream = []  # []는 빈 리스트. 게임에서 말하는 모든 자릿수 저장.
#     number = 0  # =는 대입. 다음에 진수 변환할 정수 초기화.
#     while len(stream) < t * m:  # len은 길이, *는 곱셈. 필요한 t라운드 분량까지 생성.
#         value = number  # 나눗셈 중에도 원래 정수를 보존하도록 작업용 변수 복사.
#         converted = '0' if value == 0 else ''  # 조건 표현식. 0은 별도 표현, 다른 수는 빈 문자열에서 시작.
#         while value:  # while은 반복. 몫이 0이 될 때까지 자릿수 추출.
#             value, remainder = divmod(value, n)  # divmod는 몫·나머지 반환. 두 값 언패킹.
#             converted = digits[remainder] + converted  # []는 문자 접근, +는 연결. 낮은 자리부터 얻으므로 앞에 붙임.
#         stream.extend(converted)  # extend는 문자열의 문자들을 리스트 끝에 각각 추가.
#         number += 1  # +=는 더해 저장. 다음 정수로 이동.
#     return ''.join(stream[p - 1:t * m:m])  # [시작:끝:간격]으로 p번째부터 m칸 간격의 t개 문자를 선택해 join으로 연결·반환.

# 풀이 요약
# 0부터 정수를 n진수 자릿수로 이어 붙이고, 튜브 순서에 해당하는 문자만 참가자 수 간격으로 고릅니다.
# 예: 2진수·2명·1번 순서의 네 문자는 '0111'. 필요한 문자 수 L=t*m에 대해 시간·공간 O(L).
