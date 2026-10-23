# s는 소문자 문자열.
def solution(s):
    # len은 문자열 길이.
    n = len(s)
    # 전체가 앞뒤 대칭이면 그보다 긴 부분문자열은 없음.
    if s == s[::-1]:
        # 같은 글자가 반복되는 긴 입력도 빠르게 처리.
        return n
    # 한 글자는 항상 팰린드롬이므로 최장 길이를 1로 시작.
    answer = 1
    # 글자 위 중심 n개와 글자 사이 중심 n-1개를 모두 검사.
    for center in range(2 * n - 1):
        # 확장을 시작할 왼쪽 인덱스.
        left = center // 2
        # 짝수 번호 중심은 같은 글자(홀수 길이), 홀수 번호는 옆 글자(짝수 길이)에서 시작.
        right = left + center % 2
        # 범위 안이고 양끝 글자가 같은 동안 확장.
        while left >= 0 and right < n and s[left] == s[right]:
            # 왼쪽으로 한 칸 확장.
            left -= 1
            # 오른쪽으로 한 칸 확장.
            right += 1
        # 반복 종료 시 양끝은 실패한 위치이므로 그 안쪽 길이로 계산.
        answer = max(answer, right - left - 1)
    # 연속된 부분문자열 중 최장 팰린드롬의 길이 반환.
    return answer
