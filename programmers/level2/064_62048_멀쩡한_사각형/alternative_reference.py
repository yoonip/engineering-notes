def solution(w, h):
    # 선 아래의 완전한 칸을 세면 선 위에도 같은 수가 있다.
    return 2 * sum((h * column) // w for column in range(w))
