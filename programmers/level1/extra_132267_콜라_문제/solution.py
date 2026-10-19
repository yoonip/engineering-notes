def solution(a, b, n):
    answer = 0
    while n >= a:
        exchanged = (n // a) * b
        n = (n % a) + exchanged
        answer += exchanged
    return answer

# 전체 코드 줄별 설명
# def solution(a, b, n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. a: 교환에 필요한 빈 병 수, b: 받는 콜라 수, n: 현재 빈 병 수
#     answer = 0  # =는 값 저장. 교환으로 받은 콜라의 총개수를 저장
#     while n >= a:  # while은 조건이 참인 동안 반복. >=는 이상 비교. 빈 병이 a개 이상이면 계속 교환
#         exchanged = (n // a) * b  # //는 내림한 정수 몫. =는 값 저장. 교환 가능한 횟수에 b를 곱해 새로 받는 콜라 수 계산
#         n = (n % a) + exchanged  # %는 나머지. =는 값 저장. 교환하고 남은 빈 병 + 새로 받은 콜라를 마신 뒤 생긴 빈 병
#         answer += exchanged  # +=는 더하거나 연결한 값을 저장. 이번에 받은 콜라 수를 총합에 추가
#     return answer  # return은 결과를 돌려주고 함수 종료. 교환으로 받은 콜라의 총개수 반환

# 풀이 요약
# 현재 빈 병을 a개씩 묶어 받을 수 있는 b병을 계산한다. 교환하지 못한 나머지 병에 새로 받은 병을 더해 다음 상태로 삼는다. 새 병을 마신 뒤 빈 병이 된 것으로 계산하므로 받은 병도 다음 교환에 쓸 수 있다.
# 교환 반복 횟수 T: 시간 O(T), 보조 공간 O(1).
