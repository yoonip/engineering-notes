def solution(sequence, k):
    left = total = 0
    answer = [0, len(sequence)]
    for right, value in enumerate(sequence):
        total += value
        while total > k:
            total -= sequence[left]
            left += 1
        if total == k and right - left < answer[1] - answer[0]:
            answer = [left, right]
    return answer

# 전체 코드 줄별 설명
# def solution(sequence, k):  # def는 함수 정의. ()의 sequence,k는 수열과 목표 합 입력.
#     left = total = 0  # 연쇄 대입으로 왼쪽 인덱스와 구간 합을 0으로 초기화.
#     answer = [0, len(sequence)]  # []는 리스트, len은 길이. 실제 후보보다 긴 구간으로 초기화.
#     for right, value in enumerate(sequence):  # enumerate는 (인덱스,값)을 제공. for로 두 값을 풀어 받아 순회.
#         total += value  # +=는 더해 저장. 오른쪽 원소를 현재 구간에 포함.
#         while total > k:  # while은 조건 반복, >는 큼. 합이 목표를 넘는 동안 축소.
#             total -= sequence[left]  # -=는 빼서 저장, [left]는 원소 접근. 왼쪽 원소 제외.
#             left += 1  # 왼쪽 인덱스를 한 칸 이동.
#         if total == k and right - left < answer[1] - answer[0]:  # ==는 같음, and는 둘 다 참. 목표 합이고 기존보다 짧은지 검사.
#             answer = [left, right]  # 시작·끝 인덱스를 리스트로 교체. 길이가 같으면 이전의 앞선 답 유지.
#     return answer  # return으로 선택한 두 인덱스 반환.

# 풀이 요약
# 양수 수열이므로 오른쪽을 늘리면 합이 증가하고 왼쪽을 줄이면 감소합니다. 두 포인터로 합 k인 최소 길이 구간을 찾습니다.
# 예: [1,2,3,4,5],k=7은 [3,4]의 인덱스 [2,3]. 같은 길이는 먼저 찾은 답을 유지합니다. 시간 O(N), 공간 O(1).
