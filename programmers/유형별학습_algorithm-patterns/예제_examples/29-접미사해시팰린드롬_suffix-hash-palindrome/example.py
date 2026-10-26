import sys  # 문자열 토큰 읽기
text = sys.stdin.read().split()[0]  # 허용 범위의 비어 있지 않은 문자열
n = len(text)  # 문자 수
odd, even = [0] * n, [0] * n  # 홀수와 짝수 중심 반지름
left, right, best, total = 0, -1, 0, 0  # 가장 먼 회문 경계와 결과
for i in range(n):  # 홀수 중심 순회
    radius = 1 if i > right else min(odd[left + right - i], right - i + 1)  # 거울 범위 재사용
    while i - radius >= 0 and i + radius < n and text[i - radius] == text[i + radius]:  # 새 대칭 문자 비교
        radius += 1  # 회문 확장
    odd[i] = radius  # 해당 중심 반지름
    total += radius  # 중심별 발생 수
    best = max(best, 2 * radius - 1)  # 홀수 최장 길이
    if i + radius - 1 > right:  # 더 먼 오른쪽 경계 발견
        left, right = i - radius + 1, i + radius - 1  # 검증 구간 갱신
left, right = 0, -1  # 짝수 중심 경계 초기화
for i in range(n):  # 두 문자 사이의 중심 순회
    radius = 0 if i > right else min(even[left + right - i + 1], right - i + 1)  # 짝수 거울 범위
    while i - radius - 1 >= 0 and i + radius < n and text[i - radius - 1] == text[i + radius]:  # 대칭 문자 확장
        radius += 1  # 짝수 반지름 증가
    even[i] = radius  # 짝수 중심 상태 저장
    total += radius  # 해당 중심의 회문 수
    best = max(best, 2 * radius)  # 짝수 최장 길이
    if i + radius - 1 > right:  # 기존 경계를 넘는 회문
        left, right = i - radius, i + radius - 1  # 짝수 경계 갱신
print("MAX", best)  # 가장 긴 길이
print("COUNT", total)  # 위치를 구별한 전체 회문 수
