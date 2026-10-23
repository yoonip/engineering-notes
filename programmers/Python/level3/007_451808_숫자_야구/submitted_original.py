from itertools import permutations

def solution(n, submit):
    digits = list(permutations(range(1, 10), 4))
    masks = [sum(1 << digit for digit in pattern) for pattern in digits]
    numbers = [a * 1000 + b * 100 + c * 10 + d for a, b, c, d in digits]
    cache = {}

    def feedback_row(index):
        if index not in cache:
            a, b, c, d = digits[index]
            mask = masks[index]
            cache[index] = bytes((mask & masks[i]).bit_count() * 5 + (a == w) + (b == x) + (c == y) + (d == z) for i, (w, x, y, z) in enumerate(digits))
        return cache[index]

    candidates = list(range(len(digits)))
    for turn in range(n):
        if len(candidates) == 1:
            return numbers[candidates[0]]
        selected = candidates[0]
        if turn > 0:
            best = len(candidates) + 1
            for guess in candidates:
                row = feedback_row(guess)
                counts = [0] * 25
                worst = 0
                for hidden in candidates:
                    clue = row[hidden]
                    counts[clue] += 1
                    worst = max(worst, counts[clue])
                    if worst >= best:
                        break
                if worst < best:
                    best, selected = worst, guess
                    if best == 1:
                        break
        clue = submit(numbers[selected])
        strikes, balls = int(clue[0]), int(clue[3])
        observed = (strikes + balls) * 5 + strikes
        row = feedback_row(selected)
        candidates = [hidden for hidden in candidates if row[hidden] == observed]
    return numbers[candidates[0]]

# 전체 코드 줄별 설명
# from itertools import permutations  # itertools에서 permutations를 import. 중복 없이 순서를 고려한 숫자 배치인 순열을 생성.
# 
# def solution(n, submit):  # def는 함수 정의. n은 질문 한도, submit은 숫자를 제출하면 단서를 돌려주는 채점기 함수.
#     digits = list(permutations(range(1, 10), 4))  # range의 끝 10은 제외. 1~9 중 서로 다른 4개를 고른 순열 3024개를 list로 저장.
#     masks = [sum(1 << digit for digit in pattern) for pattern in digits]  # <<는 비트 이동. 각 숫자 포함 여부를 비트로 표시하고 sum으로 합침.
#     numbers = [a * 1000 + b * 100 + c * 10 + d for a, b, c, d in digits]  # 리스트 내포와 튜플 언패킹으로 네 자릿수를 실제 정수로 변환.
#     cache = {}  # {}는 빈 딕셔너리. 질문 번호별로 모든 비밀번호 후보의 예상 단서 저장.
# 
#     def feedback_row(index):  # 한 질문에 대한 3024개 예상 응답을 만드는 중첩 함수.
#         if index not in cache:  # not in은 키가 없음. 한 번 계산한 질문은 다시 계산하지 않음.
#             a, b, c, d = digits[index]  # 질문의 네 숫자를 언패킹.
#             mask = masks[index]  # 질문에 포함된 숫자 집합.
#             cache[index] = bytes((mask & masks[i]).bit_count() * 5 + (a == w) + (b == x) + (c == y) + (d == z) for i, (w, x, y, z) in enumerate(digits))  # bytes는 작은 정수들을 압축 저장. &와 bit_count는 공통 숫자 수, == 비교 합은 스트라이크 수. 단서를 공통 수*5+스트라이크로 인코딩.
#         return cache[index]  # return으로 저장된 응답 행 반환.
# 
#     candidates = list(range(len(digits)))  # len은 개수. 아직 가능한 비밀번호들의 번호 목록.
#     for turn in range(n):  # for로 최대 n번 질문. turn은 현재 질문 회차.
#         if len(candidates) == 1:  # 후보가 하나이면 추가 제출 없이 비밀번호를 알 수 있음.
#             return numbers[candidates[0]]  # [0]은 첫 후보. 정답 정수를 반환하고 함수 종료.
#         selected = candidates[0]  # 질문 후보의 기본값.
#         if turn > 0:  # 첫 질문은 대칭성을 이용해 1234로 고정. 이후 후보를 가장 잘 나누는 질문 선택.
#             best = len(candidates) + 1  # 최소화할 최악의 남은 후보 수 초기값.
#             for guess in candidates:  # 남아 있는 비밀번호 각각을 다음 질문으로 가정.
#                 row = feedback_row(guess)  # 질문별 예상 응답을 조회하거나 생성.
#                 counts = [0] * 25  # 응답 인코딩 0~24별 후보 수를 셀 리스트 초기화.
#                 worst = 0  # 이번 질문에서 가장 큰 응답 그룹의 크기.
#                 for hidden in candidates:  # 현재 가능한 비밀번호에 대한 단서별 그룹 수 계산.
#                     clue = row[hidden]  # 이 질문·비밀번호 조합의 예상 단서 번호.
#                     counts[clue] += 1  # +=는 더해 저장. 같은 응답 그룹의 후보 수 증가.
#                     worst = max(worst, counts[clue])  # max는 큰 값. 현재 최악 그룹 크기 갱신.
#                     if worst >= best:  # >=는 이상. 이미 더 좋은 질문이 있으므로 계산 중단 가능.
#                         break  # break는 안쪽 후보 계산 반복 종료.
#                 if worst < best:  # if는 조건문. 최악의 후보 수를 더 줄이는 질문인지 검사.
#                     best, selected = worst, guess  # 두 변수에 새 최소값과 질문 번호 대입.
#                     if best == 1:  # ==는 같음. 어떤 응답이든 후보가 하나이면 더 좋은 질문은 없음.
#                         break  # 질문 탐색 반복도 종료.
#         clue = submit(numbers[selected])  # ()는 함수 호출. 실제 질문은 선택을 끝낸 후 이 한 곳에서만 수행.
#         strikes, balls = int(clue[0]), int(clue[3])  # int는 문자 숫자를 정수로 변환. 'xS yB'의 두 숫자를 추출.
#         observed = (strikes + balls) * 5 + strikes  # 실제 응답도 예상 단서와 같은 방식으로 인코딩.
#         row = feedback_row(selected)  # 방금 질문의 예상 응답 행.
#         candidates = [hidden for hidden in candidates if row[hidden] == observed]  # 리스트 내포의 if로 실제 단서와 일치하는 비밀번호만 남김.
#     return numbers[candidates[0]]  # 마지막 허용 질문 후 남은 한 후보를 반환. 전체 3024개 분기 검증에서 최대 6회에 확정됨.

# 풀이 요약
# 가능한 비밀번호 3024개를 유지합니다. 실제 단서와 모순되는 후보를 지우고, 다음 질문은 가장 큰 응답 그룹의 크기를 최소화하는 후보로 선택합니다.
# 질문은 서로 다른 1~9 숫자만 사용하므로 공통 숫자 수에서 스트라이크 수를 빼면 볼 수입니다. 이 선택·동률 순서의 전체 응답 트리를 검증해 최대 6번 질문이면 후보가 하나임을 확인했습니다.
# 예: 1234에 대한 응답이 1S 1B이면 공통 숫자는 2개, 제자리 숫자는 1개인 비밀번호만 남깁니다. 후보가 하나면 4S 응답을 추가로 받지 않아도 정답을 반환합니다.
