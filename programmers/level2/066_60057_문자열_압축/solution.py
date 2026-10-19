def solution(s):
    answer = len(s)
    for size in range(1, len(s) // 2 + 1):
        previous = s[:size]
        count, length = 1, 0
        for start in range(size, len(s), size):
            current = s[start:start + size]
            if current == previous:
                count += 1
            else:
                length += len(previous) + (len(str(count)) if count > 1 else 0)
                previous, count = current, 1
        length += len(previous) + (len(str(count)) if count > 1 else 0)
        answer = min(answer, length)
    return answer

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, s는 압축할 문자열.
#     answer = len(s)  # len은 길이. 압축하지 않은 길이로 최솟값 초기화.
#     for size in range(1, len(s) // 2 + 1):  # //는 정수 몫. 두 번 반복 가능한 단위 길이까지만 검사.
#         previous = s[:size]  # [:끝] 슬라이스로 첫 조각 저장. 끝은 미포함.
#         count, length = 1, 0  # 연속 반복 수·완료된 압축 길이를 각각 대입.
#         for start in range(size, len(s), size):  # range(시작,끝,간격)으로 다음 조각 시작점 순회.
#             current = s[start:start + size]  # 단위 길이 조각을 추출. 끝에 남은 짧은 조각도 포함.
#             if current == previous:  # ==는 같음. 이전 조각과 연속 반복인지 검사.
#                 count += 1  # +=는 더해 저장. 반복 수 증가.
#             else:  # else는 새 조각이 시작되는 경우.
#                 length += len(previous) + (len(str(count)) if count > 1 else 0)  # str은 숫자를 문자열로 변환. 반복이 두 번 이상일 때만 횟수 자릿수 추가.
#                 previous, count = current, 1  # 새 조각으로 기준을 바꾸고 반복 수 1로 초기화.
#         length += len(previous) + (len(str(count)) if count > 1 else 0)  # 마지막 반복 묶음도 길이에 반영.
#         answer = min(answer, length)  # min은 최솟값. 단위 길이별 결과 비교.
#     return answer  # return으로 가장 짧은 압축 길이 반환.

# 풀이 요약
# 단위 길이마다 앞에서부터 조각을 나누고 연속한 같은 조각을 개수+조각으로 계산합니다. 한 번뿐인 개수 1은 생략합니다.
# 예: 'aabbaccc'→'2a2ba3c', 길이 7. 길이 N일 때 시간 O(N²), 임시 문자열 공간 O(N).
