def solution(s):
    n = len(s)
    if s == s[::-1]:
        return n
    answer = 1
    for center in range(2 * n - 1):
        left = center // 2
        right = left + center % 2
        while left >= 0 and right < n and s[left] == s[right]:
            left -= 1
            right += 1
        answer = max(answer, right - left - 1)
    return answer

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. s는 소문자 문자열.
#     n = len(s)  # len은 문자열 길이.
#     if s == s[::-1]:  # ==는 같음, [::-1]은 역순 슬라이스. 전체가 앞뒤 대칭이면 그보다 긴 부분문자열은 없음.
#         return n  # 전체 길이를 즉시 반환. 같은 글자가 반복되는 긴 입력도 빠르게 처리.
#     answer = 1  # 한 글자는 항상 팰린드롬이므로 최장 길이를 1로 시작.
#     for center in range(2 * n - 1):  # range는 끝 제외. 글자 위 중심 n개와 글자 사이 중심 n-1개를 모두 검사.
#         left = center // 2  # //는 정수 나눗셈. 확장을 시작할 왼쪽 인덱스.
#         right = left + center % 2  # %는 나머지. 짝수 번호 중심은 같은 글자(홀수 길이), 홀수 번호는 옆 글자(짝수 길이)에서 시작.
#         while left >= 0 and right < n and s[left] == s[right]:  # while은 조건 반복, and는 모두 참. 범위 안이고 양끝 글자가 같은 동안 확장.
#             left -= 1  # -=는 빼서 저장. 왼쪽으로 한 칸 확장.
#             right += 1  # +=는 더해 저장. 오른쪽으로 한 칸 확장.
#         answer = max(answer, right - left - 1)  # max는 최댓값. 반복 종료 시 양끝은 실패한 위치이므로 그 안쪽 길이로 계산.
#     return answer  # 연속된 부분문자열 중 최장 팰린드롬의 길이 반환.

# 풀이 요약
# 팰린드롬은 중심에서 좌우가 대칭이다. 홀수 길이는 한 글자, 짝수 길이는 두 글자 사이를 중심으로 같은 글자 쌍이 이어지는 만큼 확장한다.
# 예: abacde에서 b를 중심으로 a·a까지 확장하면 aba의 길이 3. abba 같은 짝수 길이도 사이 중심으로 잡아야 찾을 수 있다.
# 시간 O(N²). 중심 확장 자체는 추가 공간 O(1), 전체 문자열 역순 확인을 포함한 최대 추가 공간은 O(N).
# 