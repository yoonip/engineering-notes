# 햄버거 만들기
# 분류: 스택
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/133502
# 선택 이유: 최근 재료를 스택에 쌓고 마지막 네 개만 검사하면, 제거 뒤 이어지는 햄버거도 처리할 수 있다.
# 비용: 재료 N개: 시간 O(N), 추가 공간 O(N).

def solution(ingredient):
    stack = []
    answer = 0

    for item in ingredient:
        stack.append(item)

        if stack[-4:] == [1, 2, 3, 1]:
            del stack[-4:]
            answer += 1

    return answer
