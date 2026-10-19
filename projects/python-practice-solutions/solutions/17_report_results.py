# 신고 결과 받기
# 분류: 집합 / 해시
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/92334
# 선택 이유: 같은 신고를 set으로 제거한 뒤 피신고 횟수와 발송 횟수를 각각 집계한다.
# 비용: 사용자 N명, 신고 R개: 평균 시간 O(N+R), 추가 공간 O(N+R).

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
