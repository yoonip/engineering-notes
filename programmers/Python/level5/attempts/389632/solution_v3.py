from functools import lru_cache

def solution(s, query):
    n = len(s)
    width = (len(query) + 1).bit_length()
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
    @lru_cache(maxsize=256)
    def select_letters(word):
        mask = 0
        for char in word:
            mask |= alphabet[ord(char) - 97]
        return mask
    def locate(index):
        group = 0
        for bit, plane in enumerate(planes):
            group |= ((plane >> index) & 1) << bit
        return group
    def group_mask(group):
        mask = all_bits
        for bit, plane in enumerate(planes):
            mask &= plane if (group >> bit) & 1 else ~plane
        return mask
    destination = 0
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
            changed = source ^ target
            while changed and mask:
                bit = (changed & -changed).bit_length() - 1
                planes[bit] ^= mask
                changed &= changed - 1
        elif kind == '3':
            left, right = int(parts[1]) - 1, int(parts[2])
            destination += 1
            mask = (((1 << (right - left)) - 1) << left) & select_letters(parts[3])
            if mask:
                inverse = ~mask
                for bit, plane in enumerate(planes):
                    planes[bit] = plane | mask if (destination >> bit) & 1 else plane & inverse
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
#     width = (len(query) + 1).bit_length()  # bit_length는 이진수 자릿수. 모든 생성 문자열 번호를 표현할 비트 수.
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
#     @lru_cache(maxsize=256)  # @는 장식자 적용. 자주 반복되는 알파벳 조합 마스크를 최대 256개 캐시.
#     def select_letters(word):  # 쿼리에 나온 알파벳들의 모든 원래 위치를 비트 집합으로 선택.
#         mask = 0  # 빈 집합은 모든 비트가 0인 정수.
#         for char in word:  # word의 각 알파벳을 순회. 중복 문자는 OR 결과에 영향을 주지 않음.
#             mask |= alphabet[ord(char) - 97]  # |는 비트 OR. 선택한 알파벳 위치들을 합집합으로 모음.
#         return mask  # 선택한 위치 비트 집합 반환.
#     def locate(index):  # 원래 문자 인덱스의 현재 소속 번호를 복원.
#         group = 0  # 복원할 문자열 번호 초기화.
#         for bit, plane in enumerate(planes):  # 소속 번호의 각 비트 평면을 순회.
#             group |= ((plane >> index) & 1) << bit  # 위치 비트를 추출하여 문자열 번호의 해당 자릿수에 반영.
#         return group  # 현재 소속 문자열 번호 반환.
#     def group_mask(group):  # 특정 문자열에 속한 모든 문자를 비트 집합으로 선택.
#         mask = all_bits  # 처음에는 모든 문자를 후보로 둠.
#         for bit, plane in enumerate(planes):  # 소속 번호의 각 비트 조건을 순회.
#             mask &= plane if (group >> bit) & 1 else ~plane  # &는 교집합, ~는 비트 반전. 원하는 소속 번호와 같은 위치만 남김.
#         return mask  # 해당 문자열의 현재 실제 문자 위치만 반환.
#     destination = 0  # 처음 문자열의 생성 순서 번호는 0.
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
#             changed = source ^ target  # ^는 비트 XOR. 소속 번호에서 달라지는 자릿수만 확인.
#             while changed and mask:  # and는 모두 참. 선택 문자가 있고 바꿀 자릿수가 남아 있으면 반복.
#                 bit = (changed & -changed).bit_length() - 1  # 가장 낮은 1 비트를 뽑아 변경할 자릿수 계산.
#                 planes[bit] ^= mask  # 같은 소속의 문자들이므로 달라지는 비트만 XOR로 한 번에 반전.
#                 changed &= changed - 1  # 가장 낮은 1 비트를 꺼서 다음 변경 자릿수로 진행.
#         elif kind == '3':  # 번호 범위·알파벳 조건의 문자를 새 문자열로 모음.
#             left, right = int(parts[1]) - 1, int(parts[2])  # [left,right) 형식의 문자 인덱스 범위로 변환.
#             destination += 1  # 새 문자열 생성 순서 번호 증가.
#             mask = (((1 << (right - left)) - 1) << left) & select_letters(parts[3])  # 연속 범위 비트와 알파벳 위치의 교집합 선택.
#             if mask:  # 실제로 옮길 문자가 있는 경우.
#                 inverse = ~mask  # 선택하지 않은 위치를 유지할 반전 마스크.
#                 for bit, plane in enumerate(planes):  # 소속 번호의 모든 비트 평면을 갱신.
#                     planes[bit] = plane | mask if (destination >> bit) & 1 else plane & inverse  # 새 번호의 비트가 1이면 선택 위치를 켜고, 0이면 끔.
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
# 각 문자의 소속 문자열 번호를 이진수로 나누어 여러 큰 정수에 저장합니다. 큰 정수의 AND·OR·XOR는 많은 문자의 소속을 내부 반복으로 한꺼번에 바꿉니다.
# 한 문자열의 문자를 찾을 때는 모든 번호 비트가 같은 위치를 교집합으로 남깁니다. 이동 후 비어 버린 문자열은 마지막 실제 문자 집계에서 자연스럽게 제외됩니다.
# 첫·두 번째 Python 코드와 별도로 만든 비트 집합 구현입니다. N개 문자를 큰 정수 연산 단위 W로 처리하면 쿼리당 대략 O((N/W)*log Q), 메모리 O((N/W)*log Q+N)입니다.
# 