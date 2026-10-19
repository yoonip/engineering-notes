def solution(phone_number):
    return "*" * (len(phone_number) - 4) + phone_number[-4:]

# 전체 코드 줄별 설명
# def solution(phone_number):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 전화번호 문자열을 매개변수로 받습니다.
#     return "*" * (len(phone_number) - 4) + phone_number[-4:]  # return은 결과를 돌려주고 함수 종료. len은 길이. [시작:끝]은 끝을 제외하는 슬라이스. 별표 문자열과 뒤 네 자리를 연결해 반환합니다.

# 풀이 요약
# 마지막 네 글자는 [-4:]로 보존하고 나머지 길이만큼 별을 만든다. 두 문자열을 연결하면 번호 길이를 유지하면서 뒤 네 자리만 보인다.
# 번호 길이 N: 시간·공간 O(N).
