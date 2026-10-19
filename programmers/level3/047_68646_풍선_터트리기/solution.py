# a는 서로 다른 번호가 적힌 풍선 목록.
def solution(a):
    # 끝까지 남길 수 있는 후보를 셀 변수.
    answer = 0
    # 오른쪽에서 새로 탐색할 최솟값 초기화.
    minimum = float('inf')
    # for로 왼쪽부터 풍선을 순회.
    for number in a:
        # 오른쪽에 더 작은 풍선이 없는 후보 확인.
        if number < minimum:
            # 오른쪽 기준 생존 후보 추가.
            answer += 1
            # 오른쪽에서 본 최솟값 갱신.
            minimum = number
    # 오른쪽에서 새로 탐색할 최솟값 초기화.
    minimum = float('inf')
    # 리스트 전체를 복사하지 않음.
    for number in reversed(a):
        # 오른쪽에 더 작은 풍선이 없는 후보 확인.
        if number < minimum:
            # 오른쪽 기준 생존 후보 추가.
            answer += 1
            # 오른쪽에서 본 최솟값 갱신.
            minimum = number
    # 전체 최솟값 하나만 양쪽 탐색에서 중복되므로 한 번 차감.
    return answer - 1
