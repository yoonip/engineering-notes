def solution(k, ranges):
    prefix = [0.0]
    while k > 1:
        next_value = k // 2 if k % 2 == 0 else 3 * k + 1
        prefix.append(prefix[-1] + (k + next_value) / 2)
        k = next_value
    n = len(prefix) - 1
    answer = []
    for start, offset in ranges:
        end = n + offset
        answer.append(prefix[end] - prefix[start] if start <= end else -1.0)
    return answer

# 전체 코드 줄별 설명
# def solution(k, ranges):  # def는 함수 정의. k는 초항, ranges는 적분 구간 목록 입력.
#     prefix = [0.0]  # []는 리스트. 0.0부터 시작하는 누적 넓이 저장.
#     while k > 1:  # while은 반복, >는 큼. 우박수가 1이 될 때까지 진행.
#         next_value = k // 2 if k % 2 == 0 else 3 * k + 1  # 조건 표현식. %는 나머지, //는 정수 몫. 짝수는 절반, 홀수는 3배+1.
#         prefix.append(prefix[-1] + (k + next_value) / 2)  # append는 추가, [-1]은 마지막 원소, /는 실수 나눗셈. 너비 1인 사다리꼴 넓이 누적.
#         k = next_value  # =로 다음 우박수를 현재 값으로 갱신.
#     n = len(prefix) - 1  # len은 길이. 누적 넓이 구간 수가 1까지의 변환 횟수.
#     answer = []  # 각 구간의 적분 결과를 담을 리스트.
#     for start, offset in ranges:  # for~in으로 구간 시작·끝 오프셋 언패킹.
#         end = n + offset  # 끝에서 센 오프셋을 실제 끝 좌표로 변환.
#         answer.append(prefix[end] - prefix[start] if start <= end else -1.0)  # [인덱스]의 누적 넓이 차. <=는 이하, 뒤집힌 구간이면 -1.0 선택.
#     return answer  # return으로 결과 리스트 반환.

# 풀이 요약
# 우박수열의 인접 점 사이 사다리꼴 넓이를 누적합니다. 각 구간은 끝 누적값에서 시작 누적값을 빼서 구합니다.
# 예: 5의 전체 넓이는 33.0, [3,-3]은 시작 3>끝 2라 -1.0. 수열 길이 L·질문 Q개일 때 시간·공간 O(L+Q).
