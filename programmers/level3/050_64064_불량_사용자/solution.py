# 전체 아이디 목록과 별표 패턴 목록을 받음.
def solution(user_id, banned_id):
    # 선택한 사용자를 정수의 비트로 표시하는 비트마스크.
    states = {0}
    # for로 제재 패턴을 하나씩 처리.
    for pattern in banned_id:
        # 현재 패턴에 맞는 사용자 비트를 모음.
        candidates = []
        # enumerate는 인덱스와 값을 함께 제공.
        for i, user in enumerate(user_id):
            # *가 아닌 문자는 같아야 함.
            if len(user) == len(pattern) and all(p == '*' or p == u for p, u in zip(pattern, user)):
                # <<는 비트 이동으로 i번 사용자만 표시한 값 생성.
                candidates.append(1 << i)
        # 같은 사용자 조합을 자동으로 중복 제거.
        next_states = set()
        # 앞 패턴들까지 가능한 사용자 조합을 순회.
        for mask in states:
            # 현재 패턴에 맞는 사용자를 한 명 선택.
            for bit in candidates:
                # 이미 선택한 사용자면 중복 사용 금지.
                if not mask & bit:
                    # 사용자 추가 후 add로 집합에 저장.
                    next_states.add(mask | bit)
        # 현재 패턴까지 처리한 결과로 교체.
        states = next_states
    # 서로 다른 최종 조합 수 반환.
    return len(states)
