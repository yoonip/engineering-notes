def solution(d, budget):
    d.sort()
    total = 0
    answer = 0
    for cost in d:
        if total + cost>budget:
            break
        total +=cost
        answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(d, budget):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 요청 금액들과 전체 예산을 입력받음.
#     d.sort()  # sort는 원래 리스트 정렬. 적은 금액부터 지원하도록 정렬.
#     total = 0  # =는 값 저장. 지원한 금액 합계 초기화.
#     answer = 0  # =는 값 저장. 지원한 부서 수 초기화.
#     for cost in d:  # for·in은 원소를 차례로 꺼내는 반복문. 정렬한 요청 금액을 순서대로 확인.
#         if total + cost>budget:  # if는 조건이 참일 때 실행. >는 큼 비교. 이번 요청까지 지원하면 예산을 초과하는지 확인.
#             break  # break는 가장 가까운 반복문 종료. 이후 요청도 더 비싸므로 지원 중단.
#         total +=cost  # +=는 더하거나 연결한 값을 저장. 지원 금액 누적.
#         answer += 1  # +=는 더하거나 연결한 값을 저장. 지원 부서 수 증가.
#     return answer  # return은 결과를 돌려주고 함수 종료. 지원 가능한 최대 부서 수 반환.

# 풀이 요약
# 요청 금액이 작은 부서부터 지원한다. 같은 개수의 부서를 지원할 때 가장 작은 금액들을 고르면 지출이 최소다. 정렬한 다음 요청이 예산을 넘으면 그 뒤의 더 비싼 요청도 지원할 수 없으므로 멈춘다.
# 부서 N개: 시간 O(N log N), Python 정렬 보조 공간 상한 O(N). 입력을 정렬한다.
