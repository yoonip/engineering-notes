def solution(a):
    n = len(a)
    pairs = [0] * n
    used_until = [-1] * n
    for i in range(n - 1):
        first, second = a[i], a[i + 1]
        if first == second:
            continue
        if used_until[first] < i:
            pairs[first] += 1
            used_until[first] = i + 1
        if used_until[second] < i:
            pairs[second] += 1
            used_until[second] = i + 1
    return 2 * max(pairs)

# 전체 코드 줄별 설명
# def solution(a):  # def는 함수 정의. a는 원래 수열.
#     n = len(a)  # len은 원소 개수. 원소 값이 0~n-1이므로 값 자체를 배열 인덱스로 사용 가능.
#     pairs = [0] * n  # []는 리스트, *는 반복. 각 값을 공통 원소로 쓸 때 만든 쌍 수.
#     used_until = [-1] * n  # 공통 원소별로 마지막 사용 인덱스 기록. 서로 다른 후보의 탐색 상태는 독립적.
#     for i in range(n - 1):  # range(n-1)은 0~n-2. 인접한 두 칸을 왼쪽부터 확인.
#         first, second = a[i], a[i + 1]  # []는 인덱스 조회. 두 값을 언패킹 대입.
#         if first == second:  # ==는 같음. 같은 숫자끼리는 유효한 쌍이 아님.
#             continue  # 이번 인접 쌍을 건너뜀.
#         if used_until[first] < i:  # 공통값=first인 후보에서 두 칸 모두 아직 사용하지 않았는지 검사.
#             pairs[first] += 1  # +=는 더해 저장. 유효한 쌍 한 개 추가.
#             used_until[first] = i + 1  # 두 칸을 사용했으므로 마지막 사용 위치 갱신.
#         if used_until[second] < i:  # 공통값=second인 별도의 후보에도 같은 판단 적용.
#             pairs[second] += 1  # 이 공통값의 쌍 수 증가.
#             used_until[second] = i + 1  # 해당 후보의 마지막 사용 위치 갱신.
#     return 2 * max(pairs)  # max는 최댓값. 쌍마다 원소가 두 개이므로 최장 길이는 최대 쌍 수의 두 배.

# 풀이 요약
# 공통 원소별로 겹치지 않는 유효한 인접 쌍을 왼쪽부터 선택한다. 각 인접 쌍은 두 숫자의 후보에만 영향을 주므로 전체를 한 번만 훑는다.
# 가능한 쌍은 공통값과 다른 값이 만나는 경계의 인접 쌍으로 좁힐 수 있다. 가장 먼저 끝나는 쌍을 고르면 뒤에 쓸 공간이 최대한 남는다.
# 예제 3은 공통값 0으로 네 쌍을 만들어 길이 8. 시간 O(N), 공간 O(N).
# 