def solution(sentence):
    n = len(sentence)
    if not sentence or any(not ('A' <= ch <= 'Z' or 'a' <= ch <= 'z') for ch in sentence):
        return 'invalid'
    positions = {}
    for i, ch in enumerate(sentence):
        if 'a' <= ch <= 'z':
            positions.setdefault(ch, []).append(i)
    def read_word(left, right):
        text = sentence[left:right]
        if not text or not ('A' <= text[0] <= 'Z'):
            return ''
        if all('A' <= ch <= 'Z' for ch in text):
            return text
        if len(text) % 2 == 0 or text[1] not in positions:
            return ''
        marker = text[1]
        found = positions[marker]
        if found[0] != left + 1 or found[-1] != right - 2 or len(found) != len(text) // 2:
            return ''
        for i, ch in enumerate(text):
            if i % 2 == 0 and not ('A' <= ch <= 'Z'):
                return ''
            if i % 2 == 1 and ch != marker:
                return ''
        return text[::2]
    previous = [None] * (n + 1)
    previous[0] = (-1, '')
    for start in range(n):
        if previous[start] is None:
            continue
        ch = sentence[start]
        if 'A' <= ch <= 'Z':
            end = start
            while end < n and 'A' <= sentence[end] <= 'Z':
                end += 1
                if previous[end] is None:
                    previous[end] = (start, sentence[start:end])
            if start + 1 < n and sentence[start + 1] in positions:
                end = positions[sentence[start + 1]][-1] + 2
                if end <= n:
                    word = read_word(start, end)
                    if word and previous[end] is None:
                        previous[end] = (start, word)
        else:
            found = positions[ch]
            if len(found) == 2 and found[0] == start:
                close = found[1]
                word = read_word(start + 1, close)
                if word and previous[close + 1] is None:
                    previous[close + 1] = (start, word)
    if previous[n] is None:
        return 'invalid'
    words = []
    end = n
    while end > 0:
        start, word = previous[end]
        words.append(word)
        end = start
    return ' '.join(reversed(words))

# 전체 코드 줄별 설명
# def solution(sentence):  # def는 함수 정의. 광고 문자열을 원문 단어들로 해석.
#     n = len(sentence)  # len은 문자열 길이.
#     if not sentence or any(not ('A' <= ch <= 'Z' or 'a' <= ch <= 'z') for ch in sentence):  # any는 하나라도 참, not은 부정. 빈 문자열·공백·영문 이외 문자는 거절.
#         return 'invalid'  # 유효하지 않은 암호문 표시.
#     positions = {}  # {}는 딕셔너리. 소문자 기호별 전체 출현 위치 저장.
#     for i, ch in enumerate(sentence):  # enumerate는 인덱스·값 제공.
#         if 'a' <= ch <= 'z':  # 소문자 기호인지 검사.
#             positions.setdefault(ch, []).append(i)  # setdefault는 기본 목록 생성, append는 위치 추가.
#     def read_word(left, right):  # [left,right) 구간이 대문자만 또는 규칙1로 된 단어인지 검사.
#         text = sentence[left:right]  # 슬라이스는 부분문자열 복사. 오른쪽 끝은 제외.
#         if not text or not ('A' <= text[0] <= 'Z'):  # 단어 내용은 비어 있지 않고 대문자로 시작해야 함.
#             return ''  # 빈 문자열을 검사 실패 표시로 사용.
#         if all('A' <= ch <= 'Z' for ch in text):  # all은 모두 참. 대문자만 있으면 그대로 단어.
#             return text  # 기호 없는 단어 반환.
#         if len(text) % 2 == 0 or text[1] not in positions:  # %는 나머지. 규칙1은 홀수 길이이며 둘째 글자가 소문자여야 함.
#             return ''  # 올바른 번갈이 패턴이 아니면 실패.
#         marker = text[1]  # 규칙1에 사용할 기호.
#         found = positions[marker]  # 해당 기호의 전체 출현 위치.
#         if found[0] != left + 1 or found[-1] != right - 2 or len(found) != len(text) // 2:  # !=는 다름, //는 정수 나눗셈. 기호가 현재 구간 밖에서도 쓰이거나 개수가 틀리면 거절.
#             return ''  # 기호 재사용 방지.
#         for i, ch in enumerate(text):  # 단어 구간의 모든 글자 검사.
#             if i % 2 == 0 and not ('A' <= ch <= 'Z'):  # 짝수 인덱스에는 원래 대문자가 있어야 함.
#                 return ''  # 다른 종류 기호가 섞이면 실패.
#             if i % 2 == 1 and ch != marker:  # 홀수 인덱스에는 모두 같은 기호가 있어야 함.
#                 return ''  # 다른 기호이면 실패.
#         return text[::2]  # [::2]는 두 칸 간격 슬라이스. 기호를 빼고 대문자만 복원.
#     previous = [None] * (n + 1)  # None은 아직 해석 불가. 각 끝 위치까지 가능한 해석의 직전 위치와 단어 저장.
#     previous[0] = (-1, '')  # 빈 앞부분은 해석 가능하다는 출발 상태.
#     for start in range(n):  # 모든 시작 위치를 왼쪽부터 DP로 확인.
#         if previous[start] is None:  # is None은 미도달 상태인지 확인.
#             continue  # 해석할 수 없는 앞부분이면 건너뜀.
#         ch = sentence[start]  # 현재 첫 글자.
#         if 'A' <= ch <= 'Z':  # 대문자로 시작하면 일반 단어나 규칙1 후보.
#             end = start  # 연속 대문자의 끝을 찾음.
#             while end < n and 'A' <= sentence[end] <= 'Z':  # and는 모두 참. 대문자 구간의 모든 단어 경계를 시도.
#                 end += 1  # +=는 더해 저장. 오른쪽 끝 한 칸 증가.
#                 if previous[end] is None:  # 아직 이 끝까지의 해석이 없으면 기록.
#                     previous[end] = (start, sentence[start:end])  # ()는 튜플. 해석한 일반 단어와 이전 위치 저장.
#             if start + 1 < n and sentence[start + 1] in positions:  # 둘째 글자가 소문자면 규칙1 후보.
#                 end = positions[sentence[start + 1]][-1] + 2  # 기호 마지막 출현 바로 뒤 대문자까지가 후보 구간.
#                 if end <= n:  # 마지막 기호 뒤 대문자가 실제로 있어야 함.
#                     word = read_word(start, end)  # 기호 위치와 교차 여부까지 검사.
#                     if word and previous[end] is None:  # 유효한 단어이면 도달 상태 기록.
#                         previous[end] = (start, word)  # 규칙1 단어 저장.
#         else:  # 소문자로 시작하면 규칙2로 감싼 단어여야 함.
#             found = positions[ch]  # 바깥 기호 출현 위치 조회.
#             if len(found) == 2 and found[0] == start:  # 규칙2는 기호가 정확히 두 번이고 현재가 첫 출현이어야 함.
#                 close = found[1]  # 닫는 바깥 기호 위치.
#                 word = read_word(start + 1, close)  # 내부가 대문자만 또는 별도 기호의 규칙1인지 검사.
#                 if word and previous[close + 1] is None:  # 유효하면 닫는 기호 뒤까지 도달.
#                     previous[close + 1] = (start, word)  # 규칙2 또는 두 규칙 결합 단어 저장.
#     if previous[n] is None:  # 전체 문자열을 단어들로 나눌 수 없는 경우.
#         return 'invalid'  # 실패 반환.
#     words = []  # 복원한 단어를 역순으로 담을 리스트.
#     end = n  # 문장 끝에서부터 경계를 따라감.
#     while end > 0:  # 시작 위치에 도달할 때까지 반복.
#         start, word = previous[end]  # 직전 위치·단어 언패킹.
#         words.append(word)  # 마지막 단어부터 추가.
#         end = start  # 앞 단어 끝으로 이동.
#     return ' '.join(reversed(words))  # reversed는 역순, join은 공백 하나로 단어 연결. 앞뒤 공백 없이 반환.

# 풀이 요약
# 하나의 단어 구간은 대문자만, 규칙1(대문자·기호 번갈아), 규칙2(기호로 감싸기), 두 규칙의 결합 중 하나다. 같은 기호의 전체 출현이 한 구간 안에서만 쓰이는지 검사한다.
# previous[end]에 앞부분을 유효하게 해석한 마지막 단어를 저장하는 DP를 사용한다. 가능한 경계를 모두 확인하므로 규칙1·2로 둘 다 해석되는 경우도 처리한다.
# 기호 재사용·기호 교차·두 규칙 중복은 구간 검사에서 거절한다. 길이 L≤1000, 시간·저장 문자열을 포함한 공간 O(L²). 가능한 원문 중 하나를 반환한다.
# 