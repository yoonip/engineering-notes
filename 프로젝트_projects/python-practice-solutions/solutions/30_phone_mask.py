# 핸드폰 번호 가리기
# 분류: 문자열 슬라이싱
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12948
# 선택 이유: 마지막 네 글자는 그대로 두고 앞부분 길이만큼 *를 만든다.
# 비용: 문자열 길이 L: 시간 O(L), 반환 문자열을 포함한 공간 O(L).

def solution(phone_number):
    return "*" * (len(phone_number) - 4) + phone_number[-4:]
