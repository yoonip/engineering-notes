def solution(phone_number):
    return "*" * (len(phone_number) - 4) + phone_number[-4:]


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(phone_number):  # def로 함수를 정의합니다. 전화번호 문자열을 매개변수로 받습니다.
#     return "*" * (len(phone_number) - 4) + phone_number[-4:]  # 별표 문자열과 뒤 네 자리를 연결해 반환합니다.

# len(phone_number): 전화번호의 전체 글자 수입니다.
# "*" * 정수: 별표를 해당 횟수만큼 반복합니다. 예: "*" * 3은 "***"입니다.
# phone_number[-4:]: 뒤에서 네 번째 글자부터 끝까지 읽는 슬라이싱입니다.
# +: 두 문자열을 이어 붙입니다.
# 길이가 4이면 별표가 0개이므로 원래 번호가 그대로 반환됩니다.