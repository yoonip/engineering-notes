from itertools import permutations

def solution(n, submit):
    # 1~9 중 서로 다른 4개를 고른 순열 3024개를 list로 저장.
    digits = list(permutations(range(1, 10), 4))
    masks = [sum(1 << digit for digit in pattern) for pattern in digits]
    # 리스트 내포와 튜플 언패킹으로 네 자릿수를 실제 정수로 변환.
    numbers = [a * 1000 + b * 100 + c * 10 + d for a, b, c, d in digits]
    cache = {}

    def feedback_row(index):
        if index not in cache:
            # 질문의 네 숫자를 언패킹.
            a, b, c, d = digits[index]
            mask = masks[index]
            # 단서를 공통 수*5+스트라이크로 인코딩.
            cache[index] = bytes((mask & masks[i]).bit_count() * 5 + (a == w) + (b == x) + (c == y) + (d == z) for i, (w, x, y, z) in enumerate(digits))
        return cache[index]

    candidates = list(range(len(digits)))
    # turn은 현재 질문 회차.
    for turn in range(n):
        if len(candidates) == 1:
            return numbers[candidates[0]]
        # 질문 후보의 기본값.
        selected = candidates[0]
        if turn > 0:
            best = len(candidates) + 1
            # 남아 있는 비밀번호 각각을 다음 질문으로 가정.
            for guess in candidates:
                row = feedback_row(guess)
                # 응답 인코딩 0~24별 후보 수를 셀 리스트 초기화.
                counts = [0] * 25
                worst = 0
                for hidden in candidates:
                    # 이 질문·비밀번호 조합의 예상 단서 번호.
                    clue = row[hidden]
                    counts[clue] += 1
                    # 현재 최악 그룹 크기 갱신.
                    worst = max(worst, counts[clue])
                    if worst >= best:
                        break
                # 최악의 후보 수를 더 줄이는 질문인지 검사.
                if worst < best:
                    best, selected = worst, guess
                    # 어떤 응답이든 후보가 하나이면 더 좋은 질문은 없음.
                    if best == 1:
                        break
        clue = submit(numbers[selected])
        # 'xS yB'의 두 숫자를 추출.
        strikes, balls = int(clue[0]), int(clue[3])
        observed = (strikes + balls) * 5 + strikes
        # 방금 질문의 예상 응답 행.
        row = feedback_row(selected)
        candidates = [hidden for hidden in candidates if row[hidden] == observed]
    return numbers[candidates[0]]
