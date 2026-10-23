def solution(k, room_number):
    next_room = {}
    answer = []
    for wanted in room_number:
        room = wanted
        trail = []
        while room in next_room:
            trail.append(room)
            room = next_room[room]
        answer.append(room)
        next_room[room] = room + 1
        for previous in trail:
            next_room[previous] = room + 1
    return answer

# 전체 코드 줄별 설명
# def solution(k, room_number):  # def는 함수 정의. 전체 방 수 k와 고객별 희망 방 번호를 입력받음.
#     next_room = {}  # {}는 빈 딕셔너리. 배정된 방 번호를 다음 검색 후보 번호에 연결.
#     answer = []  # []는 빈 리스트. 실제 배정 방 번호를 순서대로 저장.
#     for wanted in room_number:  # for로 고객의 요청 순서를 그대로 순회.
#         room = wanted  # 이번 고객의 희망 방에서 검색 시작.
#         trail = []  # 빈 방을 찾는 동안 거친 배정 완료 방 번호 저장.
#         while room in next_room:  # in은 딕셔너리 키 존재 여부 검사. 이미 배정된 방이면 반복.
#             trail.append(room)  # append는 리스트 끝에 추가. 나중에 경로를 압축할 방을 기록.
#             room = next_room[room]  # []로 딕셔너리 값 조회. 다음 후보로 건너뜀.
#         answer.append(room)  # 키가 없는 방은 비어 있으므로 이번 고객에게 배정.
#         next_room[room] = room + 1  # 이번 방도 사용 중으로 등록. 다음 검색은 바로 뒤에서 시작.
#         for previous in trail:  # 이번 검색에서 지나온 모든 방 순회.
#             next_room[previous] = room + 1  # 같은 경로를 반복하지 않도록 새 후보로 한 번에 연결하는 경로 압축.
#     return answer  # return으로 실제 배정 번호 목록 반환. 모든 고객이 배정 가능한 입력이므로 k 초과 검사 불필요.

# 풀이 요약
# 배정 완료 방을 다음 검색 후보와 연결하는 딕셔너리 기반 서로소 집합 방식입니다. 지나온 경로를 압축해 긴 연속 점유 구간을 건너뜁니다.
# 예: [1,3,4,1,3,1]은 [1,3,4,2,5,6]. 방이 10^12개여도 실제 요청에 사용된 방만 저장합니다.
# 요청 수 Q에 대해 경로 압축의 총 시간 O(Q*log Q), 공간 O(Q). 반복문을 사용해 긴 경로의 재귀 오류를 피합니다.
# 