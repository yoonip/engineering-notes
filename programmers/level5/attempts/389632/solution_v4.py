from functools import lru_cache

def solution(s, query):
    n = len(s)
    width = 18
    planes = [0] * width
    all_bits = (1 << n) - 1
    byte_count = (n + 7) // 8
    letter_bytes = [bytearray(byte_count) for _ in range(26)]
    letters = []
    for index, char in enumerate(s):
        letter = ord(char) - 97
        letters.append(letter)
        letter_bytes[letter][index >> 3] |= 1 << (index & 7)
    alphabet = [int.from_bytes(data, 'little') for data in letter_bytes]
    union_tables = []
    for start in range(0, 26, 6):
        table = [0]
        size = min(6, 26 - start)
        for code in range(1, 1 << size):
            lowest = code & -code
            table.append(table[code - lowest] | alphabet[start + lowest.bit_length() - 1])
        union_tables.append(table)
    @lru_cache(maxsize=256)
    def select_letters(word):
        code = 0
        for char in word:
            code |= 1 << (ord(char) - 97)
        return (union_tables[0][code & 63] | union_tables[1][(code >> 6) & 63] | union_tables[2][(code >> 12) & 63] | union_tables[3][(code >> 18) & 63] | union_tables[4][code >> 24])
    def locate(index):
        return (
            ((planes[0] >> index) & 1)
            | (((planes[1] >> index) & 1) << 1)
            | (((planes[2] >> index) & 1) << 2)
            | (((planes[3] >> index) & 1) << 3)
            | (((planes[4] >> index) & 1) << 4)
            | (((planes[5] >> index) & 1) << 5)
            | (((planes[6] >> index) & 1) << 6)
            | (((planes[7] >> index) & 1) << 7)
            | (((planes[8] >> index) & 1) << 8)
            | (((planes[9] >> index) & 1) << 9)
            | (((planes[10] >> index) & 1) << 10)
            | (((planes[11] >> index) & 1) << 11)
            | (((planes[12] >> index) & 1) << 12)
            | (((planes[13] >> index) & 1) << 13)
            | (((planes[14] >> index) & 1) << 14)
            | (((planes[15] >> index) & 1) << 15)
            | (((planes[16] >> index) & 1) << 16)
            | (((planes[17] >> index) & 1) << 17)
        )
    def group_mask(group):
        return (all_bits
            & (planes[0] if group & 1 else ~planes[0])
            & (planes[1] if group & 2 else ~planes[1])
            & (planes[2] if group & 4 else ~planes[2])
            & (planes[3] if group & 8 else ~planes[3])
            & (planes[4] if group & 16 else ~planes[4])
            & (planes[5] if group & 32 else ~planes[5])
            & (planes[6] if group & 64 else ~planes[6])
            & (planes[7] if group & 128 else ~planes[7])
            & (planes[8] if group & 256 else ~planes[8])
            & (planes[9] if group & 512 else ~planes[9])
            & (planes[10] if group & 1024 else ~planes[10])
            & (planes[11] if group & 2048 else ~planes[11])
            & (planes[12] if group & 4096 else ~planes[12])
            & (planes[13] if group & 8192 else ~planes[13])
            & (planes[14] if group & 16384 else ~planes[14])
            & (planes[15] if group & 32768 else ~planes[15])
            & (planes[16] if group & 65536 else ~planes[16])
            & (planes[17] if group & 131072 else ~planes[17])
        )
    flips = [()]
    for value in range(1, 1 << width):
        lowest = value & -value
        flips.append(flips[value - lowest] + (lowest.bit_length() - 1,))
    destination = 0
    bit_values = [1 << bit for bit in range(width)]
    result = []
    for command in query:
        parts = command.split()
        kind = parts[0]
        if kind == '1':
            a, b = locate(int(parts[1]) - 1), locate(int(parts[2]) - 1)
            result.append('YES' if a == b else 'NO')
        elif kind == '2' or kind == '4':
            source = locate(int(parts[1]) - 1)
            if kind == '2':
                destination += 1
                target = destination
                mask = group_mask(source) & select_letters(parts[2])
            else:
                target = locate(int(parts[2]) - 1)
                if source == target:
                    continue
                source, target = max(source, target), min(source, target)
                mask = group_mask(source)
            if mask:
                for bit in flips[source ^ target]:
                    planes[bit] ^= mask
        elif kind == '3':
            left, right = int(parts[1]) - 1, int(parts[2])
            destination += 1
            mask = (((1 << (right - left)) - 1) << left) & select_letters(parts[3])
            if mask:
                inverse = ~mask
                planes[:] = [plane | mask if destination & bit else plane & inverse for plane, bit in zip(planes, bit_values)]
        else:
            encoded = [plane.to_bytes(byte_count, 'little') for plane in planes]
            groups = {}
            for index, letter in enumerate(letters):
                byte, shift = index >> 3, index & 7
                group = 0
                for bit, data in enumerate(encoded):
                    group |= ((data[byte] >> shift) & 1) << bit
                counts = groups.setdefault(group, {})
                counts[letter] = counts.get(letter, 0) + 1
            for group in sorted(groups):
                counts = groups[group]
                result.append(' '.join(value for letter in sorted(counts) for value in (chr(letter + 97), str(counts[letter]))))
    return result

# 전체 코드 줄별 설명
# from functools import lru_cache  # from A import B는 모듈에서 가져오기. lru_cache는 최근 함수 결과를 제한된 개수만 저장하는 장식자.
# 
# def solution(s, query):  # def는 함수 정의. 초기 문자열과 쿼리 목록을 입력받음.
#     n = len(s)  # len은 길이. 전체 문자 개수.
#     width = 18  # 쿼리 최대 20만 개의 생성 번호는 18비트로 표현 가능. 명시적 비트 처리로 반복문 비용 절약.
#     planes = [0] * width  # []는 리스트. planes[b]의 i번째 비트는 i번 문자의 소속 번호에서 b번째 비트.
#     all_bits = (1 << n) - 1  # <<는 비트 이동. n개 문자를 모두 선택하는 1 비트 마스크 생성.
#     byte_count = (n + 7) // 8  # //는 정수 나눗셈. 문자별 1비트를 저장할 바이트 수.
#     letter_bytes = [bytearray(byte_count) for _ in range(26)]  # bytearray는 0~255 정수 배열. 알파벳별 문자 위치 비트 초기화.
#     letters = []  # 각 원래 문자의 알파벳 번호를 담을 리스트.
#     for index, char in enumerate(s):  # enumerate는 인덱스와 문자를 함께 제공.
#         letter = ord(char) - 97  # ord는 문자 코드. a~z를 0~25로 변환.
#         letters.append(letter)  # append는 끝에 추가. 최종 알파벳 집계에 사용할 문자 번호 저장.
#         letter_bytes[letter][index >> 3] |= 1 << (index & 7)  # >>3은 8로 나눈 몫, &7은 나머지. 해당 위치 비트를 |=로 켬.
#     alphabet = [int.from_bytes(data, 'little') for data in letter_bytes]  # 바이트 배열을 정수 비트 집합으로 변환. little은 앞 바이트가 낮은 자릿수임을 뜻함.
#     union_tables = []  # 알파벳 6개 묶음마다 모든 부분집합의 위치 합집합을 미리 저장.
#     for start in range(0, 26, 6):  # 0·6·12·18·24번째 알파벳부터 묶음을 시작.
#         table = [0]  # 빈 알파벳 부분집합은 위치 마스크 0.
#         size = min(6, 26 - start)  # min은 작은 값. 마지막 묶음은 알파벳 두 개만 포함.
#         for code in range(1, 1 << size):  # 묶음 안의 모든 알파벳 선택 조합을 순회.
#             lowest = code & -code  # 가장 낮은 선택 비트 추출.
#             table.append(table[code - lowest] | alphabet[start + lowest.bit_length() - 1])  # 이전 조합에 한 알파벳의 위치를 OR로 합쳐 마스크 계산.
#         union_tables.append(table)  # 묶음별 사전 계산 표를 저장.
#     @lru_cache(maxsize=256)  # 장식자로 자주 반복되는 word의 위치 마스크를 최대 256개 기억.
#     def select_letters(word):  # word에 포함된 알파벳의 원래 위치 전체를 선택.
#         code = 0  # 알파벳 포함 여부를 26비트 정수에 저장.
#         for char in word:  # 각 알파벳을 순회. 중복은 OR로 자연스럽게 제거.
#             code |= 1 << (ord(char) - 97)  # ord는 문자 코드. 해당 알파벳 선택 비트를 켬.
#         return (union_tables[0][code & 63] | union_tables[1][(code >> 6) & 63] | union_tables[2][(code >> 12) & 63] | union_tables[3][(code >> 18) & 63] | union_tables[4][code >> 24])  # 6비트 묶음별 사전 계산 마스크 다섯 개만 OR로 합침.
#     def locate(index):  # 원래 문자 인덱스의 소속 번호를 비트 평면에서 복원.
#         return (  # 여러 자릿수의 OR 식을 괄호 안에서 이어 계산.
#             ((planes[0] >> index) & 1)  # 소속 번호의 0번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[1] >> index) & 1) << 1)  # 소속 번호의 1번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[2] >> index) & 1) << 2)  # 소속 번호의 2번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[3] >> index) & 1) << 3)  # 소속 번호의 3번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[4] >> index) & 1) << 4)  # 소속 번호의 4번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[5] >> index) & 1) << 5)  # 소속 번호의 5번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[6] >> index) & 1) << 6)  # 소속 번호의 6번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[7] >> index) & 1) << 7)  # 소속 번호의 7번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[8] >> index) & 1) << 8)  # 소속 번호의 8번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[9] >> index) & 1) << 9)  # 소속 번호의 9번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[10] >> index) & 1) << 10)  # 소속 번호의 10번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[11] >> index) & 1) << 11)  # 소속 번호의 11번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[12] >> index) & 1) << 12)  # 소속 번호의 12번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[13] >> index) & 1) << 13)  # 소속 번호의 13번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[14] >> index) & 1) << 14)  # 소속 번호의 14번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[15] >> index) & 1) << 15)  # 소속 번호의 15번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[16] >> index) & 1) << 16)  # 소속 번호의 16번째 비트를 읽어 해당 자릿수에 반영.
#             | (((planes[17] >> index) & 1) << 17)  # 소속 번호의 17번째 비트를 읽어 해당 자릿수에 반영.
#         )  # 소속 번호 조립 표현식 종료.
#     def group_mask(group):  # 소속 번호의 모든 자릿수가 일치하는 문자 위치를 선택.
#         return (all_bits  # 모든 문자 위치에서 시작하여 소속 번호별 조건으로 필터링.
#             & (planes[0] if group & 1 else ~planes[0])  # 소속 번호의 0번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[1] if group & 2 else ~planes[1])  # 소속 번호의 1번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[2] if group & 4 else ~planes[2])  # 소속 번호의 2번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[3] if group & 8 else ~planes[3])  # 소속 번호의 3번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[4] if group & 16 else ~planes[4])  # 소속 번호의 4번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[5] if group & 32 else ~planes[5])  # 소속 번호의 5번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[6] if group & 64 else ~planes[6])  # 소속 번호의 6번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[7] if group & 128 else ~planes[7])  # 소속 번호의 7번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[8] if group & 256 else ~planes[8])  # 소속 번호의 8번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[9] if group & 512 else ~planes[9])  # 소속 번호의 9번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[10] if group & 1024 else ~planes[10])  # 소속 번호의 10번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[11] if group & 2048 else ~planes[11])  # 소속 번호의 11번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[12] if group & 4096 else ~planes[12])  # 소속 번호의 12번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[13] if group & 8192 else ~planes[13])  # 소속 번호의 13번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[14] if group & 16384 else ~planes[14])  # 소속 번호의 14번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[15] if group & 32768 else ~planes[15])  # 소속 번호의 15번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[16] if group & 65536 else ~planes[16])  # 소속 번호의 16번째 비트 조건에 맞는 위치만 교집합으로 유지.
#             & (planes[17] if group & 131072 else ~planes[17])  # 소속 번호의 17번째 비트 조건에 맞는 위치만 교집합으로 유지.
#         )  # 특정 문자열의 실제 위치 마스크 반환.
#     flips = [()]  # ()는 빈 튜플. 소속 번호 차이별로 바꿀 비트 위치들을 미리 저장.
#     for value in range(1, 1 << width):  # 가능한 소속 번호의 비트 차이를 작은 값부터 순회.
#         lowest = value & -value  # 가장 낮은 1 비트 하나만 추출.
#         flips.append(flips[value - lowest] + (lowest.bit_length() - 1,))  # 기존 비트 위치 튜플에 새 자릿수를 붙여 반복적인 비트 추출을 생략.
#     destination = 0  # 처음 문자열의 생성 순서 번호는 0.
#     bit_values = [1 << bit for bit in range(width)]  # 각 자릿수의 비트 값을 미리 저장하여 반복 계산 제거.
#     result = []  # 1번·5번 쿼리의 출력 목록.
#     for command in query:  # 모든 쿼리를 주어진 순서대로 처리.
#         parts = command.split()  # split은 공백으로 쿼리 문자열을 나눔.
#         kind = parts[0]  # 첫 항목은 쿼리 종류.
#         if kind == '1':  # if는 조건문. 두 문자의 소속 비교.
#             a, b = locate(int(parts[1]) - 1), locate(int(parts[2]) - 1)  # int는 정수 변환. 1부터 시작하는 번호를 인덱스로 바꾸어 조회.
#             result.append('YES' if a == b else 'NO')  # 조건 표현식으로 같은 문자열이면 YES, 아니면 NO 추가.
#         elif kind == '2' or kind == '4':  # elif는 다음 조건, or는 하나라도 참. 출발 문자열이 하나로 정해지는 이동·병합 쿼리.
#             source = locate(int(parts[1]) - 1)  # 기준 문자의 현재 문자열 소속 조회.
#             if kind == '2':  # 지정 알파벳을 새 문자열로 분리하는 경우.
#                 destination += 1  # +=는 더한 값 저장. 빈 결과여도 생성 순서 번호는 증가.
#                 target = destination  # 새 문자열을 이동 목표로 설정.
#                 mask = group_mask(source) & select_letters(parts[2])  # 현재 문자열 문자와 지정 알파벳 위치의 교집합만 선택.
#             else:  # 두 문자열을 합치는 경우.
#                 target = locate(int(parts[2]) - 1)  # 두 번째 문자의 소속 조회.
#                 if source == target:  # ==는 같음 비교. 이미 같은 문자열이면 병합 불필요.
#                     continue  # continue는 이번 쿼리를 건너뜀.
#                 source, target = max(source, target), min(source, target)  # max·min으로 늦게 생성된 문자열을 오래된 문자열로 이동하도록 지정.
#                 mask = group_mask(source)  # 늦게 생성된 문자열의 모든 문자를 선택.
#             if mask:  # 이동할 문자가 있을 때만 실제 비트 갱신.
#                 for bit in flips[source ^ target]:  # ^는 XOR. 미리 저장한 소속 번호 차이의 비트 위치만 순회.
#                     planes[bit] ^= mask  # 같은 소속의 문자들이므로 달라지는 자릿수만 한 번에 반전.
#         elif kind == '3':  # 번호 범위·알파벳 조건의 문자를 새 문자열로 모음.
#             left, right = int(parts[1]) - 1, int(parts[2])  # [left,right) 형식의 문자 인덱스 범위로 변환.
#             destination += 1  # 새 문자열 생성 순서 번호 증가.
#             mask = (((1 << (right - left)) - 1) << left) & select_letters(parts[3])  # 연속 범위 비트와 알파벳 위치의 교집합 선택.
#             if mask:  # 실제로 옮길 문자가 있는 경우.
#                 inverse = ~mask  # 선택하지 않은 위치를 유지할 반전 마스크.
#                 planes[:] = [plane | mask if destination & bit else plane & inverse for plane, bit in zip(planes, bit_values)]  # 리스트 내포·zip으로 각 비트 평면을 새 소속 번호에 맞게 한 번에 갱신.
#         else:  # 마지막 5번 쿼리. 실제 남은 문자열의 알파벳 구성 출력.
#             encoded = [plane.to_bytes(byte_count, 'little') for plane in planes]  # to_bytes는 정수 비트 집합을 바이트로 변환. 모든 문자 조회를 위해 한 번씩만 변환.
#             groups = {}  # {}는 딕셔너리. 실제 소속 번호별 알파벳 개수를 집계.
#             for index, letter in enumerate(letters):  # 모든 원래 문자의 위치와 알파벳을 순회.
#                 byte, shift = index >> 3, index & 7  # 해당 비트가 들어 있는 바이트 위치와 바이트 안 자릿수.
#                 group = 0  # 현재 문자의 소속 번호 복원 준비.
#                 for bit, data in enumerate(encoded):  # 각 소속 번호 비트의 바이트 배열 순회.
#                     group |= ((data[byte] >> shift) & 1) << bit  # 작은 바이트 정수에서 비트를 읽어 소속 번호 조립.
#                 counts = groups.setdefault(group, {})  # setdefault는 키가 없으면 빈 알파벳 딕셔너리를 생성.
#                 counts[letter] = counts.get(letter, 0) + 1  # get은 없으면 기본값 반환. 해당 알파벳 개수 증가.
#             for group in sorted(groups):  # 생성 순서 번호를 sorted로 오름차순 정렬. 비어 사라진 문자열은 집계에 없음.
#                 counts = groups[group]  # 이번 문자열의 알파벳 개수 조회.
#                 result.append(' '.join(value for letter in sorted(counts) for value in (chr(letter + 97), str(counts[letter]))))  # chr은 코드→문자, str은 숫자→문자열, join은 공백을 넣어 합침.
#     return result  # return으로 전체 조회 결과 목록 반환.

# 풀이 요약
# 문자 소속 번호를 18개의 큰 정수 비트 평면에 저장합니다. AND·OR·XOR로 많은 문자 소속을 내부 연산에서 한꺼번에 변경합니다.
# 알파벳을 6개씩 묶어 선택 마스크를 사전 계산하고, 소속 번호 간 달라지는 비트 위치도 미리 계산하여 Python 반복 비용을 줄였습니다.
# 비교용 첫·두 번째·세 번째 Python 구현을 따로 보존했습니다. 실행 코드 아래에 동일한 코드 전체와 줄별 문법·의도 설명이 있습니다.
# 