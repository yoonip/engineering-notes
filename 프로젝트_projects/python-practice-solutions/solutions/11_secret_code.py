# 둘만의 암호
# 분류: 알파벳 위치 표 / 나머지 연산
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/155652
# 선택 이유: 제외할 글자를 뺀 알파벳과 위치 표를 만든다. 결과는 리스트로 모아 join해 반복 문자열 복사를 피한다.
# 비용: 문자열 길이 L, 알파벳 26자 고정: 평균 시간 O(L), 추가 공간 O(L).

def solution(s, skip, index):
    excluded = set(skip)
    alphabet = [char for char in "abcdefghijklmnopqrstuvwxyz" if char not in excluded]
    positions = {char: position for position, char in enumerate(alphabet)}
    answer = []
    for char in s:
        next_position = (positions[char] + index) % len(alphabet)
        answer.append(alphabet[next_position])
    return "".join(answer)
