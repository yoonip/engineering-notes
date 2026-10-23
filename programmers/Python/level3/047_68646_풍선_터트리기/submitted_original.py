def solution(a):
    answer = 0
    minimum = float('inf')
    for number in a:
        if number < minimum:
            answer += 1
            minimum = number
    minimum = float('inf')
    for number in reversed(a):
        if number < minimum:
            answer += 1
            minimum = number
    return answer - 1

# 전체 코드 줄별 설명
# def solution(a):  # def는 함수 정의. a는 서로 다른 번호가 적힌 풍선 목록.
#     answer = 0  # 끝까지 남길 수 있는 후보를 셀 변수.
#     minimum = float('inf')  # float('inf')는 무한대. 처음 원소도 최솟값으로 기록되게 초기화.
#     for number in a:  # for로 왼쪽부터 풍선을 순회.
#         if number < minimum:  # 지금까지 본 모든 왼쪽 풍선보다 작은지 비교.
#             answer += 1  # +=는 더해 저장. 왼쪽에 더 작은 풍선이 없으므로 생존 가능.
#             minimum = number  # 새 최솟값으로 갱신.
#     minimum = float('inf')  # 오른쪽에서 새로 탐색할 최솟값 초기화.
#     for number in reversed(a):  # reversed는 뒤에서 앞으로 순회하는 도구. 리스트 전체를 복사하지 않음.
#         if number < minimum:  # 오른쪽에 더 작은 풍선이 없는 후보 확인.
#             answer += 1  # 오른쪽 기준 생존 후보 추가.
#             minimum = number  # 오른쪽에서 본 최솟값 갱신.
#     return answer - 1  # 전체 최솟값 하나만 양쪽 탐색에서 중복되므로 한 번 차감.

# 풀이 요약
# 왼쪽과 오른쪽 모두에 자신보다 작은 풍선이 있으면 작은 풍선을 두 번 터뜨려야 해서 불가능하다. 한쪽의 최솟값이면 생존 가능하다.
# 예: [9,-1,-5]의 왼쪽 최소 기록은 9,-1,-5, 오른쪽은 -5. 중복 -5를 빼면 3개.
# 양쪽에서 최솟값이 갱신되는 원소 수를 더하고 전체 최솟값의 중복 1개를 뺀다. 시간 O(N), 추가 공간 O(1).
# 