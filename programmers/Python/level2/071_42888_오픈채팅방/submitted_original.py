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

# 전체 코드 줄별 설명
# def solution(record):  # def는 함수 정의, record는 입장·퇴장·변경 기록 입력.
#     names = {}  # {}는 빈 딕셔너리. 사용자 ID별 최종 닉네임 저장.
#     events = []  # []는 빈 리스트. 출력할 입장·퇴장 이벤트 순서 저장.
#     for entry in record:  # for~in으로 기록 순회.
#         parts = entry.split()  # split()으로 공백 기준 단어 분리.
#         action, user = parts[0], parts[1]  # [인덱스]로 동작·ID를 읽어 각각 대입.
#         if action != 'Leave':  # !=는 다름. 입장·이름 변경에는 새 닉네임이 있음.
#             names[user] = parts[2]  # [키]의 닉네임을 최신 값으로 덮어씀.
#         if action != 'Change':  # if는 조건 분기. 이름 변경 자체는 메시지를 남기지 않음.
#             events.append((user, action))  # append로 ID·동작 튜플을 기록. 아직 닉네임은 넣지 않음.
#     messages = {'Enter': '님이 들어왔습니다.', 'Leave': '님이 나갔습니다.'}  # 동작별 메시지 접미사를 딕셔너리에 연결.
#     return [names[user] + messages[action] for user, action in events]  # 리스트 내포로 이벤트를 언패킹하고 +로 최종 닉네임·메시지를 연결해 반환.

# 풀이 요약
# 먼저 최종 닉네임을 확정하면서 ID와 입퇴장 순서만 기록합니다. 이후 모든 이벤트에 최종 닉네임을 붙입니다.
# 예: uid1234가 Prodo로 재입장하면 이전 입퇴장 기록도 Prodo로 표시. 기록 N개일 때 시간·공간 O(N).
