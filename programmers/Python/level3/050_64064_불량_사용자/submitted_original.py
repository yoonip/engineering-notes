def solution(user_id, banned_id):
    states = {0}
    for pattern in banned_id:
        candidates = []
        for i, user in enumerate(user_id):
            if len(user) == len(pattern) and all(p == '*' or p == u for p, u in zip(pattern, user)):
                candidates.append(1 << i)
        next_states = set()
        for mask in states:
            for bit in candidates:
                if not mask & bit:
                    next_states.add(mask | bit)
        states = next_states
    return len(states)

# 전체 코드 줄별 설명
# def solution(user_id, banned_id):  # def는 함수 정의. 전체 아이디 목록과 별표 패턴 목록을 받음.
#     states = {0}  # {0}은 원소 0 하나를 가진 집합. 선택한 사용자를 정수의 비트로 표시하는 비트마스크.
#     for pattern in banned_id:  # for로 제재 패턴을 하나씩 처리.
#         candidates = []  # []는 리스트. 현재 패턴에 맞는 사용자 비트를 모음.
#         for i, user in enumerate(user_id):  # enumerate는 인덱스와 값을 함께 제공.
#             if len(user) == len(pattern) and all(p == '*' or p == u for p, u in zip(pattern, user)):  # len은 길이, and는 모두 참, all은 모든 조건 검사, zip은 글자끼리 묶음. *가 아닌 문자는 같아야 함.
#                 candidates.append(1 << i)  # append는 추가. <<는 비트 이동으로 i번 사용자만 표시한 값 생성.
#         next_states = set()  # set()은 빈 집합. 같은 사용자 조합을 자동으로 중복 제거.
#         for mask in states:  # 앞 패턴들까지 가능한 사용자 조합을 순회.
#             for bit in candidates:  # 현재 패턴에 맞는 사용자를 한 명 선택.
#                 if not mask & bit:  # &는 비트 AND, not은 부정. 이미 선택한 사용자면 중복 사용 금지.
#                     next_states.add(mask | bit)  # |는 비트 OR. 사용자 추가 후 add로 집합에 저장.
#         states = next_states  # 현재 패턴까지 처리한 결과로 교체.
#     return len(states)  # 순서가 달라도 같은 조합은 같은 마스크. 서로 다른 최종 조합 수 반환.

# 풀이 요약
# 패턴마다 대응 가능한 사용자를 찾고, 기존 선택 조합에 아직 쓰지 않은 사용자 한 명을 추가한다. 비트마스크 집합이 순서 중복을 제거한다.
# 예: 같은 *rodo 패턴 둘에 frodo·crodo를 배정하는 순서는 두 가지지만 최종 마스크는 같아서 한 번만 센다.
# 사용자 N≤8, 패턴 B≤8, 아이디 길이 L≤8. 시간 O(B·N·(L+2^N)), 공간 O(2^N).
# 