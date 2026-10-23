
def solution(today, terms, privacies):
    def to_days(date):
        y, m, d = map(int, date.split("."))
        return y * 12 * 28 + m * 28 + d

    term_dict = {}

    for term in terms:
        kind, months = term.split()
        term_dict[kind] = int(months)

    today_days = to_days(today)
    answer = []

    for i, privacy in enumerate(privacies, start=1):
        date, kind = privacy.split()

        expiry_days = to_days(date) + term_dict[kind] * 28

        if today_days >= expiry_days:
            answer.append(i)

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(today, terms, privacies):                  # 오늘 날짜, 약관 정보, 개인정보 목록을 입력받는 함수
#     def to_days(date):                                 # 날짜를 일수로 변환하는 내부 함수
#         y, m, d = map(int, date.split("."))            # "."을 기준으로 날짜를 나누고 각각 정수로 변환
#         return y * 12 * 28 + m * 28 + d                # 1년 12개월, 1개월 28일 기준으로 전체 일수 계산
#
#     term_dict = {}                                    # 약관 종류별 유효기간을 저장할 딕셔너리
#
#     for term in terms:                                # 약관 정보를 하나씩 반복
#         kind, months = term.split()                    # 공백 기준 분리 (예: "A 6" → "A", "6")
#         term_dict[kind] = int(months)                  # 약관 종류를 키로, 유효기간을 정수로 저장
#
#     today_days = to_days(today)                       # 오늘 날짜를 일수로 변환
#     answer = []                                       # 파기할 개인정보 번호를 저장할 리스트
#
#     for i, privacy in enumerate(privacies, start=1):  # 개인정보를 1번부터 번호를 붙여 순회
#         date, kind = privacy.split()                   # 수집 날짜와 약관 종류 분리
#
#         expiry_days = to_days(date) + term_dict[kind] * 28  # 수집일에 유효기간을 더해 만료 기준일 계산
#
#         if today_days >= expiry_days:                 # 오늘이 만료 기준일과 같거나 늦으면
#             answer.append(i)                          # 파기할 개인정보 번호를 추가
#
#     return answer                                     # 파기해야 하는 개인정보 번호 목록 반환
