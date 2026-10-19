# 신규 아이디 추천
# 분류: 한 번의 순회 / 문자열 정규화
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/72410
# 선택 이유: 필터링과 연속 마침표 제거를 한 번에 처리한다. 리스트에 모은 뒤 join해 반복 치환·문자열 복사를 피한다.
# 비용: 입력 길이 L: 시간 O(L), 추가 공간 O(L). 길이 보정은 최대 15자에서 처리한다.

def solution(new_id):
    filtered = []
    for char in new_id.lower():
        if not (char.isalnum() or char in "-_."):
            continue
        if char == "." and filtered and filtered[-1] == ".":
            continue
        filtered.append(char)

    answer = "".join(filtered).strip(".")
    if not answer:
        answer = "a"
    answer = answer[:15].rstrip(".")
    while len(answer) < 3:
        answer += answer[-1]
    return answer
