# commands는 순서대로 실행할 표 명령 문자열 목록.
def solution(commands):
    # 각 셀이 속한 병합 그룹 번호를 직접 저장.
    groups = list(range(2500))
    # 그룹 대표 번호에만 값 저장, 빈 문자열은 빈 셀.
    values = [''] * 2500
    # PRINT 결과를 모을 빈 리스트.
    answer = []

    # 행·열 문자열을 1차원 셀 번호로 변환하는 중첩 함수.
    def position(r, c):
        # 1 기반 행·열을 0 기반 위치로 변환해 return.
        return (int(r) - 1) * 50 + int(c) - 1

    # for~in으로 명령 순회.
    for command in commands:
        # split()은 공백으로 단어를 나눠 리스트 반환.
        parts = command.split()
        # [0]은 첫 단어인 명령 이름.
        operation = parts[0]
        # 네 단어면 특정 셀 갱신.
        if operation == 'UPDATE' and len(parts) == 4:
            # 출력할 셀 번호 계산.
            cell = position(parts[1], parts[2])
            # 병합 그룹 대표의 값을 변경해 모든 소속 셀에 반영.
            values[groups[cell]] = parts[3]
        # 세 단어면 값 전체 치환.
        elif operation == 'UPDATE':
            # 두 값을 언패킹.
            old, new = parts[1], parts[2]
            # 모든 그룹 값 저장 공간 순회.
            for i in range(2500):
                # 기존 값과 일치하는지 검사.
                if values[i] == old:
                    # 새 값으로 변경.
                    values[i] = new
        # 두 셀의 그룹 병합.
        elif operation == 'MERGE':
            # 첫 셀이 속한 그룹 번호.
            first = groups[position(parts[1], parts[2])]
            # 둘째 셀이 속한 그룹 번호.
            second = groups[position(parts[3], parts[4])]
            # 이미 같은 그룹이면 아무 작업도 하지 않음.
            if first == second:
                # continue는 다음 명령으로 진행.
                continue
            # 첫 값이 비어 있지 않으면 우선, 비었으면 둘째 값.
            value = values[first] or values[second]
            # 둘째 그룹의 모든 셀을 찾음.
            for cell in range(2500):
                # 해당 셀이 둘째 그룹 소속인지 확인.
                if groups[cell] == second:
                    # 그룹 번호를 첫 그룹으로 바꿔 병합.
                    groups[cell] = first
            # 병합 후 사용할 값 저장.
            values[first] = value
            # 더는 대표가 아닌 이전 그룹 값 삭제.
            values[second] = ''
        # 선택 셀이 속한 그룹 전체 해제.
        elif operation == 'UNMERGE':
            # 출력할 셀 번호 계산.
            cell = position(parts[1], parts[2])
            # 해제할 그룹 번호.
            group = groups[cell]
            # 해제 후 선택 셀에만 남길 값 보관.
            value = values[group]
            # 리스트 내포로 해제 대상 셀을 먼저 수집.
            members = [i for i in range(2500) if groups[i] == group]
            # 병합된 모든 셀 순회.
            for member in members:
                # 각 셀을 독립 그룹으로 되돌림.
                groups[member] = member
                # 값을 빈 초기 상태로 되돌림.
                values[member] = ''
            # 선택한 셀 하나에만 이전 값을 복원.
            values[cell] = value
        else:
            # 출력할 셀 번호 계산.
            cell = position(parts[1], parts[2])
            # 빈 문자열은 거짓이므로 or 뒤의 EMPTY 출력.
            answer.append(values[groups[cell]] or 'EMPTY')
    # 모든 PRINT 결과를 원래 순서대로 반환.
    return answer
