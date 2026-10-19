def solution(commands):
    groups = list(range(2500))
    values = [''] * 2500
    answer = []

    def position(r, c):
        return (int(r) - 1) * 50 + int(c) - 1

    for command in commands:
        parts = command.split()
        operation = parts[0]
        if operation == 'UPDATE' and len(parts) == 4:
            cell = position(parts[1], parts[2])
            values[groups[cell]] = parts[3]
        elif operation == 'UPDATE':
            old, new = parts[1], parts[2]
            for i in range(2500):
                if values[i] == old:
                    values[i] = new
        elif operation == 'MERGE':
            first = groups[position(parts[1], parts[2])]
            second = groups[position(parts[3], parts[4])]
            if first == second:
                continue
            value = values[first] or values[second]
            for cell in range(2500):
                if groups[cell] == second:
                    groups[cell] = first
            values[first] = value
            values[second] = ''
        elif operation == 'UNMERGE':
            cell = position(parts[1], parts[2])
            group = groups[cell]
            value = values[group]
            members = [i for i in range(2500) if groups[i] == group]
            for member in members:
                groups[member] = member
                values[member] = ''
            values[cell] = value
        else:
            cell = position(parts[1], parts[2])
            answer.append(values[groups[cell]] or 'EMPTY')
    return answer

# 전체 코드 줄별 설명
# def solution(commands):  # def는 함수 정의. commands는 순서대로 실행할 표 명령 문자열 목록.
#     groups = list(range(2500))  # range는 0~2499, list는 목록 생성. 각 셀이 속한 병합 그룹 번호를 직접 저장.
#     values = [''] * 2500  # [] 리스트를 *로 반복. 그룹 대표 번호에만 값 저장, 빈 문자열은 빈 셀.
#     answer = []  # PRINT 결과를 모을 빈 리스트.
# 
#     def position(r, c):  # 행·열 문자열을 1차원 셀 번호로 변환하는 중첩 함수.
#         return (int(r) - 1) * 50 + int(c) - 1  # int는 문자열→정수. 1 기반 행·열을 0 기반 위치로 변환해 return.
# 
#     for command in commands:  # for~in으로 명령 순회.
#         parts = command.split()  # split()은 공백으로 단어를 나눠 리스트 반환.
#         operation = parts[0]  # [0]은 첫 단어인 명령 이름.
#         if operation == 'UPDATE' and len(parts) == 4:  # if는 조건문, ==는 같음, and는 모두 참. 네 단어면 특정 셀 갱신.
#             cell = position(parts[1], parts[2])  # 함수 호출 ()로 셀 번호 계산.
#             values[groups[cell]] = parts[3]  # 병합 그룹 대표의 값을 변경해 모든 소속 셀에 반영.
#         elif operation == 'UPDATE':  # elif는 앞 조건이 거짓일 때 검사. 세 단어면 값 전체 치환.
#             old, new = parts[1], parts[2]  # 두 값을 언패킹.
#             for i in range(2500):  # 모든 그룹 값 저장 공간 순회.
#                 if values[i] == old:  # 기존 값과 일치하는지 검사.
#                     values[i] = new  # 새 값으로 변경.
#         elif operation == 'MERGE':  # 두 셀의 그룹 병합.
#             first = groups[position(parts[1], parts[2])]  # 첫 셀이 속한 그룹 번호.
#             second = groups[position(parts[3], parts[4])]  # 둘째 셀이 속한 그룹 번호.
#             if first == second:  # 이미 같은 그룹이면 아무 작업도 하지 않음.
#                 continue  # continue는 다음 명령으로 진행.
#             value = values[first] or values[second]  # or는 첫 참인 값을 선택. 첫 값이 비어 있지 않으면 우선, 비었으면 둘째 값.
#             for cell in range(2500):  # 둘째 그룹의 모든 셀을 찾음.
#                 if groups[cell] == second:  # 해당 셀이 둘째 그룹 소속인지 확인.
#                     groups[cell] = first  # 그룹 번호를 첫 그룹으로 바꿔 병합.
#             values[first] = value  # 병합 후 사용할 값 저장.
#             values[second] = ''  # 더는 대표가 아닌 이전 그룹 값 삭제.
#         elif operation == 'UNMERGE':  # 선택 셀이 속한 그룹 전체 해제.
#             cell = position(parts[1], parts[2])  # 선택한 실제 셀 번호.
#             group = groups[cell]  # 해제할 그룹 번호.
#             value = values[group]  # 해제 후 선택 셀에만 남길 값 보관.
#             members = [i for i in range(2500) if groups[i] == group]  # 리스트 내포로 해제 대상 셀을 먼저 수집.
#             for member in members:  # 병합된 모든 셀 순회.
#                 groups[member] = member  # 각 셀을 독립 그룹으로 되돌림.
#                 values[member] = ''  # 값을 빈 초기 상태로 되돌림.
#             values[cell] = value  # 선택한 셀 하나에만 이전 값을 복원.
#         else:  # 나머지 명령은 PRINT.
#             cell = position(parts[1], parts[2])  # 출력할 셀 번호 계산.
#             answer.append(values[groups[cell]] or 'EMPTY')  # append는 결과 하나 추가. 빈 문자열은 거짓이므로 or 뒤의 EMPTY 출력.
#     return answer  # 모든 PRINT 결과를 원래 순서대로 반환.

# 풀이 요약
# 2500칸뿐이므로 각 셀에 그룹 번호를 직접 저장하고 병합·해제 때 전체를 순회합니다. 값은 그룹 대표 한 곳에만 둡니다.
# MERGE는 첫 셀 값이 있으면 우선합니다. UNMERGE는 모든 소속 셀을 초기화한 후 지정 셀 하나만 값을 남깁니다. 명령 Q개에 대해 시간 O(2500Q), 공간 O(2500+출력 수).
# 예: a와 b가 있는 두 셀을 첫 셀 우선으로 병합하면 모두 a. 둘째 셀에서 해제하면 첫 셀은 EMPTY, 둘째 셀만 a입니다.
