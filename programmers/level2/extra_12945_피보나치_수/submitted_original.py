def solution(n):
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, (previous + current) % 1234567
    return previous

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 구할 피보나치 수의 번호 입력.
#     previous, current = 0, 1  # 언패킹 대입으로 F(0),F(1) 초기화. 두 변수만 사용하는 동적 계획법(DP).
#     for _ in range(n):  # range(n)은 n번 반복, _는 쓰지 않는 반복 변수.
#         previous, current = current, (previous + current) % 1234567  # 오른쪽 값을 먼저 계산한 뒤 동시에 대입. %는 나머지. 연속 두 피보나치 값을 다음으로 이동.
#     return previous  # n번 이동한 후 previous가 F(n)의 나머지.

# 풀이 요약
# 다음 수는 직전 두 수의 합이므로 두 변수로 순서대로 갱신한다. 매번 나머지를 취해 수가 지나치게 커지는 것을 막는다.
# 예: (0,1)→(1,1)→(1,2)→(2,3)이므로 n=3의 답은 2. 시간 O(N), 공간 O(1).
# 