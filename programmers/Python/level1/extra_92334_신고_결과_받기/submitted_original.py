def solution(id_list, report, k):
    unique_reports = set(report)
    reported_count = {user: 0 for user in id_list}
    mail_count = {user: 0 for user in id_list}

    for record in unique_reports:
        reporter, target = record.split()
        reported_count[target] += 1

    for record in unique_reports:
        reporter, target = record.split()
        if reported_count[target] >= k:
            mail_count[reporter] += 1

    return [mail_count[user] for user in id_list]


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(id_list, report, k):  # def로 함수를 정의합니다. 이용자 목록, 신고 기록, 정지 기준을 받습니다.
#     unique_reports = set(report)  # set은 중복을 허용하지 않는 집합입니다. 같은 신고 문자열을 하나만 남깁니다.
#     reported_count = {user: 0 for user in id_list}  # 딕셔너리 컴프리헨션입니다. ID를 키로, 신고당한 횟수 0을 값으로 저장합니다.
#     mail_count = {user: 0 for user in id_list}  # 각 이용자가 받을 메일 개수를 0으로 시작합니다.
#
#     for record in unique_reports:  # 중복을 제거한 신고 문자열을 하나씩 꺼냅니다.
#         reporter, target = record.split()  # split()으로 공백을 기준으로 나누고 신고자와 신고 대상에 각각 대입합니다.
#         reported_count[target] += 1  # 딕셔너리[키]의 값을 1 증가시킵니다. 신고 대상의 횟수를 늘립니다.
#
#     for record in unique_reports:  # 모든 신고 횟수를 계산한 뒤 기록을 다시 확인합니다.
#         reporter, target = record.split()  # 예: "muzi frodo"이면 reporter="muzi", target="frodo"입니다.
#         if reported_count[target] >= k:  # >=는 크거나 같다는 비교입니다. 정확히 k번 신고되어도 정지됩니다.
#             mail_count[reporter] += 1  # 해당 상대를 신고한 사람의 메일 개수를 1 늘립니다.
#
#     return [mail_count[user] for user in id_list]  # 리스트 컴프리헨션으로 입력 ID 순서대로 메일 수를 모아 반환합니다.