from bisect import bisect_right

def solution(arr, l, r):
    lengths = [0]
    sums = [0]
    for value in arr:
        lengths.append(lengths[-1] + value)
        sums.append(sums[-1] + value * value)

    def prefix(count):
        index = min(len(arr) - 1, bisect_right(lengths, count) - 1)
        return sums[index] + (count - lengths[index]) * arr[index]

    target = prefix(r) - prefix(l - 1)
    window = r - l + 1
    last_start = lengths[-1] - window
    current = prefix(window)
    start = left = 0
    right = bisect_right(lengths, window) - 1
    answer = 0
    while start < last_start:
        span = min(lengths[left + 1] - start, lengths[right + 1] - start - window, last_start - start)
        slope = arr[right] - arr[left]
        if slope == 0:
            if current == target:
                answer += span
        else:
            difference = target - current
            if difference % slope == 0 and 0 <= difference // slope < span:
                answer += 1
        current += slope * span
        start += span
        if start == lengths[left + 1]:
            left += 1
        if start + window == lengths[right + 1]:
            right += 1
    answer += int(current == target)
    return [target, answer]

# 전체 코드 줄별 설명
# from bisect import bisect_right  # from~import는 모듈의 도구를 가져옴. bisect_right는 정렬 목록에서 같은 값들의 오른쪽 삽입 위치를 이진 탐색.
# 
# def solution(arr, l, r):  # def는 함수 정의. arr는 압축된 값, l·r은 1부터 세는 구간 양끝.
#     lengths = [0]  # [0]은 원소 하나의 리스트. 각 값 묶음의 끝 위치를 누적 저장.
#     sums = [0]  # sums[i]는 앞 i개 묶음의 총합. 빈 앞부분의 합은 0.
#     for value in arr:  # for~in으로 배열 원소를 하나씩 순회.
#         lengths.append(lengths[-1] + value)  # [-1]은 마지막 원소. 값 value가 value번 등장하므로 전체 길이에 value 추가.
#         sums.append(sums[-1] + value * value)  # append는 끝에 하나 추가. 한 묶음의 합은 value의 제곱.
# 
#     def prefix(count):  # 앞 count개 원소의 합을 구하는 중첩 함수 정의.
#         index = min(len(arr) - 1, bisect_right(lengths, count) - 1)  # len은 길이, min은 작은 값. count가 속하는 묶음을 이진 탐색.
#         return sums[index] + (count - lengths[index]) * arr[index]  # 완전한 앞 묶음 합에 현재 묶음의 일부 합을 더해 return으로 반환.
# 
#     target = prefix(r) - prefix(l - 1)  # 누적합의 차이로 l~r 구간 합 K 계산.
#     window = r - l + 1  # 비교할 모든 구간의 길이.
#     last_start = lengths[-1] - window  # 0부터 세는 마지막 가능한 시작 위치.
#     current = prefix(window)  # 시작 위치가 0인 첫 구간의 합.
#     start = left = 0  # 연쇄 대입으로 현재 시작 위치와 왼쪽 묶음 번호를 0으로 초기화.
#     right = bisect_right(lengths, window) - 1  # 구간을 오른쪽으로 옮길 때 들어오는 원소의 묶음 번호.
#     answer = 0  # 합이 target인 구간 수 초기화.
#     while start < last_start:  # while은 조건이 참인 동안 반복. 마지막 시작점은 반복 뒤 따로 계산.
#         span = min(lengths[left + 1] - start, lengths[right + 1] - start - window, last_start - start)  # 나가는 값과 들어오는 값이 모두 일정한 이동 횟수.
#         slope = arr[right] - arr[left]  # 한 칸 이동할 때 구간 합 변화량 = 들어오는 값 - 나가는 값.
#         if slope == 0:  # if는 조건문, ==는 같음. 변화량 0이면 합이 계속 일정.
#             if current == target:  # 현재 합이 목표와 같은 경우만 해당 묶음의 시작점을 모두 셈.
#                 answer += span  # +=는 더해 저장. span개의 시작 위치를 한꺼번에 추가.
#         else:  # else는 앞 조건이 거짓일 때. 합이 일정하게 늘거나 줄어드는 경우.
#             difference = target - current  # 목표 합에 도달하기 위해 필요한 변화량.
#             if difference % slope == 0 and 0 <= difference // slope < span:  # %는 나머지, //는 정수 나눗셈. 정수 이동 횟수가 현재 구간 안에 있는지 and로 함께 검사.
#                 answer += 1  # 일정한 기울기에서는 목표 합을 만드는 시작점이 최대 하나.
#         current += slope * span  # *는 곱셈. span번 이동한 뒤의 합으로 한 번에 갱신.
#         start += span  # 시작점도 span만큼 이동.
#         if start == lengths[left + 1]:  # 나가는 원소의 묶음 끝에 도달했는지 확인.
#             left += 1  # 왼쪽 묶음을 다음으로 이동.
#         if start + window == lengths[right + 1]:  # 들어오는 원소도 현재 묶음 끝에 도달했는지 확인.
#             right += 1  # 오른쪽 묶음을 다음으로 이동.
#     answer += int(current == target)  # int는 참을 1, 거짓을 0으로 바꿈. 마지막 시작점 한 개를 계산.
#     return [target, answer]  # [] 리스트로 K와 C를 묶어 반환.

# 풀이 요약
# brr를 만들면 길이가 매우 커집니다. 각 묶음의 길이·합만 누적해 K를 구하고, 고정 길이 구간을 묶음 경계 사이에서 한꺼번에 이동합니다.
# 같은 묶음 안에서는 구간 합이 일정한 등차수열이므로 목표 합과 같은 위치를 나눗셈으로 셉니다. 시간 O(N), 공간 O(N).
# 예: [2,2,2]는 2가 여섯 번인 배열. 길이 1인 모든 구간 합이 2이므로 [2,6]입니다.
