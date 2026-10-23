def solution(letter):
    codes = '.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..'.split()
    morse = {code: chr(97 + i) for i, code in enumerate(codes)}
    return ''.join(morse[code] for code in letter.split())

# 전체 코드 줄별 설명
# def solution(letter):  # def는 함수 정의. 공백으로 나눈 모스부호 문자열 입력.
#     codes = '.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..'.split()  # split은 공백으로 분리. a부터 z까지의 모스부호 표 저장.
#     morse = {code: chr(97 + i) for i, code in enumerate(codes)}  # 딕셔너리 내포. enumerate는 번호와 부호 제공, chr은 문자 코드를 문자로 변환. 97은 a의 코드.
#     return ''.join(morse[code] for code in letter.split())  # 공백으로 부호를 나눈 뒤 []로 알파벳을 조회하고 join으로 연결.

# 풀이 요약
# 문제에서 제공한 모스부호 표를 딕셔너리로 만들어 각 부호를 문자로 바꿉니다.
# 