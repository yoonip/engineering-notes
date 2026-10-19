def solution(book_time):
    changes = [0] * 1450
    for start, end in book_time:
        sh, sm = map(int, start.split(':'))
        eh, em = map(int, end.split(':'))
        changes[sh * 60 + sm] += 1
        changes[eh * 60 + em + 10] -= 1
    active = answer = 0
    for change in changes:
        active += change
        answer = max(answer, active)
    return answer

# 전체 코드 줄별 설명
# def solution(book_time):  # def는 함수 정의, book_time은 입실·퇴실 시각 목록 입력.
#     changes = [0] * 1450  # []는 리스트, *는 반복 생성. 자정 이후 청소 10분까지 시간별 증감 저장.
#     for start, end in book_time:  # for~in으로 예약의 두 문자열을 각각 언패킹.
#         sh, sm = map(int, start.split(':'))  # split은 ':' 기준 분리, map(int,...)는 각 조각을 정수로 변환.
#         eh, em = map(int, end.split(':'))  # 퇴실 시각의 시·분도 정수로 변환.
#         changes[sh * 60 + sm] += 1  # []는 원소 접근, +=는 더해 저장. 입실 분부터 방 하나 사용.
#         changes[eh * 60 + em + 10] -= 1  # -=는 빼서 저장. 퇴실+10분부터 방 사용 해제.
#     active = answer = 0  # 연쇄 대입으로 현재 사용량과 최대 사용량 초기화.
#     for change in changes:  # 시간 순으로 방 수 증감을 순회.
#         active += change  # 누적 합으로 해당 분의 사용 중인 방 수 계산.
#         answer = max(answer, active)  # max는 최댓값. 동시에 필요한 방의 최대 수 갱신.
#     return answer  # return으로 필요한 최소 객실 수 반환.

# 풀이 요약
# 입실에 +1, 청소 종료에 -1을 기록하고 시간별 누적 합의 최댓값을 구합니다.
# 예: 10:10 퇴실한 방은 10:20부터 다시 사용 가능해 방 1개면 됩니다. 예약 N개일 때 시간 O(N+1450), 공간 O(1450).
