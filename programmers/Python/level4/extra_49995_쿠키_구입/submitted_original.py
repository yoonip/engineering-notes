def solution(cookie):
    n = len(cookie)
    answer = 0
    for middle in range(n - 1):
        left, right = middle, middle + 1
        left_sum, right_sum = cookie[left], cookie[right]
        while True:
            if left_sum == right_sum:
                answer = max(answer, left_sum)
            if left_sum <= right_sum:
                if left == 0:
                    break
                left -= 1
                left_sum += cookie[left]
            else:
                if right == n - 1:
                    break
                right += 1
                right_sum += cookie[right]
    return answer

# 전체 코드 줄별 설명
# def solution(cookie):  # def는 함수 정의. 바구니별 과자 수 리스트를 입력받음.
#     n = len(cookie)  # len은 길이. 바구니 개수를 구함.
#     answer = 0  # 같은 양으로 나눌 수 없을 때 반환할 기본값.
#     for middle in range(n - 1):  # range의 끝은 제외. 두 구간 사이의 경계를 0부터 n-2까지 고정.
#         left, right = middle, middle + 1  # 왼쪽 구간의 시작과 오른쪽 구간의 끝을 경계 바로 옆에서 시작.
#         left_sum, right_sum = cookie[left], cookie[right]  # []는 인덱스 접근. 양쪽 합을 각 한 바구니로 초기화.
#         while True:  # while True는 조건에 따른 break가 나올 때까지 반복.
#             if left_sum == right_sum:  # if는 조건문, ==는 같음 비교. 두 아들의 과자 수가 같은지 확인.
#                 answer = max(answer, left_sum)  # max는 큰 값 반환. 한 사람 몫의 최댓값 갱신.
#             if left_sum <= right_sum:  # 모든 값이 양수이므로 작은 쪽 합을 늘려야 같은 합을 찾을 수 있음.
#                 if left == 0:  # 왼쪽에 더 추가할 바구니가 없는지 확인.
#                     break  # break는 현재 while 반복 종료.
#                 left -= 1  # -=는 뺀 값 저장. 왼쪽 구간을 한 칸 확장.
#                 left_sum += cookie[left]  # +=는 더한 값 저장. 새 바구니의 과자 수 합산.
#             else:  # else는 왼쪽 합이 더 큰 경우 실행.
#                 if right == n - 1:  # 오른쪽에 더 추가할 바구니가 없는지 확인.
#                     break  # 현재 경계에서 탐색 종료.
#                 right += 1  # 오른쪽 구간을 한 칸 확장.
#                 right_sum += cookie[right]  # 새 바구니의 과자 수를 오른쪽 합에 추가.
#     return answer  # return으로 가능한 최대 한 사람 몫 반환. 두 사람 합계를 반환하지 않음.

# 풀이 요약
# 두 아들의 구간은 붙어 있어야 하므로 경계 m을 고정하고 양쪽 포인터를 바깥으로 확장합니다. 양수 배열이라 합이 작은 쪽만 늘리면 됩니다.
# 예: [1,1,2,3]에서 왼쪽 [1,2], 오른쪽 [3]을 선택하면 한 사람당 3개입니다.
# 각 경계에서 포인터가 최대 n번 움직입니다. 시간 O(n^2), 추가 공간 O(1).
# 