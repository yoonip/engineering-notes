def solution(land):
    a = b = c = d = 0
    for first, second, third, fourth in land:
        a, b, c, d = (
            first + max(b, c, d),
            second + max(a, c, d),
            third + max(a, b, d),
            fourth + max(a, b, c),
        )
    return max(a, b, c, d)

# 전체 코드 줄별 설명
# def solution(land):  # def는 함수 정의. 행마다 네 칸의 점수 목록 입력.
#     a = b = c = d = 0  # 연쇄 대입. 직전 행의 0~3열에 도착한 최대 점수 네 개를 저장하는 동적 계획법(DP) 상태.
#     for first, second, third, fourth in land:  # for에서 현재 행의 네 점수를 네 변수로 언패킹. 열은 항상 네 개.
#         a, b, c, d = (  # 튜플 언패킹 대입. 오른쪽 네 식을 전부 이전 값으로 계산한 뒤 동시에 갱신.
#             first + max(b, c, d),  # max는 최댓값. 0열은 직전 0열 a를 제외한 최대 점수에 현재 값을 더함.
#             second + max(a, c, d),  # 1열은 직전 1열 b 제외. 쉼표는 튜플 원소 구분.
#             third + max(a, b, d),  # 2열은 직전 2열 c 제외.
#             fourth + max(a, b, c),  # 3열은 직전 3열 d 제외. 고정된 네 계산으로 내부 반복 비용 절감.
#         )  # 여러 줄로 적은 오른쪽 튜플 종료.
#     return max(a, b, c, d)  # 마지막 행의 네 도착 위치 중 최대 점수 반환.

# 풀이 요약
# 현재 열과 다른 직전 열 세 개 중 최적 점수를 골라 누적한다. 각 행의 큰 점수만 즉시 고르는 탐욕은 다음 행 선택을 고려하지 못한다.
# 예: 5→7→4로 16점. 열은 네 개로 고정되어 한 행당 계산은 상수이므로 시간 O(N), 추가 공간 O(1).
# 