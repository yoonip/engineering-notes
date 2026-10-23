def solution(record):
    names = {}
    events = []
    # 기록 순회.
    for entry in record:
        parts = entry.split()
        # [인덱스]로 동작·ID를 읽어 각각 대입.
        action, user = parts[0], parts[1]
        if action != 'Leave':
            # [키]의 닉네임을 최신 값으로 덮어씀.
            names[user] = parts[2]
        if action != 'Change':
            # 아직 닉네임은 넣지 않음.
            events.append((user, action))
    messages = {'Enter': '님이 들어왔습니다.', 'Leave': '님이 나갔습니다.'}
    return [names[user] + messages[action] for user, action in events]
