def solution(id_pw, db):
    username, password = id_pw
    members = dict(db)
    if username not in members:
        return 'fail'
    return 'login' if members[username] == password else 'wrong pw'

# 전체 코드 줄별 설명
# def solution(id_pw, db):  # def는 함수 정의. 문제에서 제공한 가상 아이디·비밀번호와 회원 목록 입력.
#     username, password = id_pw  # 두 항목을 아이디·비밀번호 변수로 나누어 대입.
#     members = dict(db)  # dict는 [키,값] 쌍 리스트를 딕셔너리로 변환. 아이디로 문제 데이터의 비밀번호 조회.
#     if username not in members:  # if는 조건, not in은 키가 없음 검사.
#         return 'fail'  # 아이디가 없을 때의 지정 문자열 반환.
#     return 'login' if members[username] == password else 'wrong pw'  # []로 값 조회, ==로 문자열 비교. 조건 표현식으로 일치·불일치 메시지 반환.

# 풀이 요약
# 코딩 문제의 입력 데이터에서 아이디 존재 여부를 먼저 확인하고 비밀번호를 비교합니다.
# 