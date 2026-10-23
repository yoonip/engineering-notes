def solution(n):
    # 예: 78의 1001110에서 10을 추출.
    lowest = n & -n
    raised = n + lowest
    # 올리면서 빠진 나머지 1들을 오른쪽 끝으로 모음.
    tail = ((n ^ raised) >> 2) // lowest
    return raised | tail
