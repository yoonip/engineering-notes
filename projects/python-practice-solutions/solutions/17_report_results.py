# 신고 결과 받기
# 분류: 집합 / 해시
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/92334
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

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


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(id_list, report, k):  # def로 함수를 정의합니다. 이용자 리스트, 신고 기록, 정지 기준을 매개변수로 받습니다.
#     unique_reports = set(report)  # set은 중복을 허용하지 않는 집합입니다. 똑같은 신고 문자열은 하나만 남깁니다.
#     reported_count = {user: 0 for user in id_list}  # 딕셔너리 컴프리헨션입니다. 각 ID를 키로, 신고당한 횟수 0을 값으로 저장합니다.
#     mail_count = {user: 0 for user in id_list}  # 각 ID에 연결된 메일 개수를 0으로 시작합니다. 위 딕셔너리와 별개입니다.
#
#     for record in unique_reports:  # 중복을 제거한 집합에서 신고 문자열을 하나씩 꺼냅니다. 집합의 순서는 보장되지 않지만 합산 결과는 같습니다.
#         reporter, target = record.split()  # split()은 공백으로 나눕니다. 두 값을 신고자와 신고 대상 변수에 각각 넣는 언패킹입니다.
#         reported_count[target] += 1  # 딕셔너리[키]의 값을 읽고 1을 더해 다시 저장합니다. 신고당한 사람의 횟수를 늘립니다.
#
#     for record in unique_reports:  # 신고 횟수를 모두 센 뒤 같은 기록들을 다시 확인합니다.
#         reporter, target = record.split()  # 예: "muzi frodo" → reporter="muzi", target="frodo"입니다.
#         if reported_count[target] >= k:  # >=는 크거나 같다는 비교입니다. 정확히 k번인 경우도 정지입니다.
#             mail_count[reporter] += 1  # 정지된 상대를 신고한 사람의 메일 개수를 늘립니다. += 1은 기존 값에 1을 더합니다.
#
#     return [mail_count[user] for user in id_list]  # 리스트 컴프리헨션으로 입력 ID 순서대로 메일 수를 모아 반환합니다.
#
