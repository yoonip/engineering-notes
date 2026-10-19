# 문제: 오픈채팅방
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42888
# 풀이: 사용자 ID별 최종 닉네임과 입퇴장 이벤트를 따로 저장한다. 마지막에 닉네임을 붙여 과거 메시지를 반복 수정하지 않는다.
# 복잡도: 기록 총 글자수 L·이벤트 N개·결과 글자수 A: 시간 O(L+A), 추가 공간 O(L+N+A).

def solution(record):
    names = {}
    events = []
    for entry in record:
        parts = entry.split()
        action, user = parts[0], parts[1]
        if action != 'Leave':
            names[user] = parts[2]
        if action != 'Change':
            events.append((user, action))
    messages = {'Enter': '님이 들어왔습니다.', 'Leave': '님이 나갔습니다.'}
    return [names[user] + messages[action] for user, action in events]
