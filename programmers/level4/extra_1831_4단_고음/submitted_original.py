from functools import cache

def solution(n):
    powers = [1]
    while powers[-1] <= n:
        powers.append(powers[-1] * 3)
    @cache
    def search(value, pending):
        if value < 3:
            return 0
        if value == 3:
            return int(pending == 2)
        required = (pending + 1) // 2
        if required >= len(powers) or value < powers[required]:
            return 0
        answer = search(value - 1, pending + 1)
        if pending >= 2 and value % 3 == 0:
            answer += search(value // 3, pending - 2)
        return answer
    return search(n - 2, 2)

# 전체 코드 줄별 설명
# from functools import cache  # from A import B는 모듈에서 가져오기. cache는 같은 인수의 함수 결과를 저장해 재계산을 줄이는 장식자.
# 
# def solution(n):  # def는 함수 정의. 만들려는 최종 음높이 n을 입력받음.
#     powers = [1]  # []는 리스트. 3의 거듭제곱을 순서대로 저장.
#     while powers[-1] <= n:  # [-1]은 마지막 원소. n을 넘는 거듭제곱까지 반복.
#         powers.append(powers[-1] * 3)  # append는 끝에 추가. 다음 3의 거듭제곱 계산.
#     @cache  # @는 장식자 적용 문법. 아래 재귀 함수의 (value,pending)별 결과를 기억.
#     def search(value, pending):  # 음높이를 거꾸로 되돌리며 아직 짝짓지 않은 +의 수를 함께 관리.
#         if value < 3:  # if는 조건문. 맨 처음 *가 만드는 음높이 3보다 작으면 불가능.
#             return 0  # return으로 가능한 문자열 개수 0 반환.
#         if value == 3:  # 시작 음높이 1에서 첫 *만 남은 상태인지 확인.
#             return int(pending == 2)  # ==는 같음 비교. 첫 *와 짝인 + 두 개만 남아야 하며 int로 참·거짓을 1·0으로 변환.
#         required = (pending + 1) // 2  # //는 정수 나눗셈. 남은 +를 짝짓기 위해 필요한 최소 * 개수.
#         if required >= len(powers) or value < powers[required]:  # or는 하나라도 참. 필요한 *를 적용한 최소 음높이보다 작으면 불가능한 가지 제거.
#             return 0  # 불가능한 상태는 재귀 확장 없이 종료.
#         answer = search(value - 1, pending + 1)  # 마지막 기호를 +로 가정해 1을 되돌리고 미사용 + 개수 증가.
#         if pending >= 2 and value % 3 == 0:  # and는 모두 참, %는 나머지. + 두 개가 있고 3으로 나누어질 때 *를 되돌릴 수 있음.
#             answer += search(value // 3, pending - 2)  # +=는 합산. * 하나를 되돌리며 해당 + 두 개를 짝지음.
#         return answer  # 이 상태에서 가능한 문자열 개수 반환.
#     return search(n - 2, 2)  # 올바른 문자열은 반드시 ++로 끝나므로 두 +를 먼저 제거하고 역방향 탐색 시작.

# 풀이 요약
# * 하나에는 뒤쪽의 + 두 개가 필요합니다. 뒤에서부터 +는 1을 빼고 개수를 누적하며, *는 3으로 나누고 누적 + 두 개를 소비합니다.
# 남은 +가 p개면 최소 ceil(p/2)개의 *가 필요하므로 현재 값이 3^ceil(p/2)보다 작으면 불가능합니다. 같은 상태는 메모이제이션으로 한 번만 계산합니다.
# 예: n=41은 **++++*++와 *+**+++++ 두 가지. 방문 상태 수 S에 대해 시간·공간 O(S), 재귀 깊이는 O(log n). Python3 학습용 코드입니다.
# 