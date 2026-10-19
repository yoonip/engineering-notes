def solution(wallet, bill):
    wallet.sort()
    bill.sort()
    answer = 0
    while bill[0] > wallet[0] or bill[1] > wallet[1]:
        bill[1] //= 2
        bill.sort()
        answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(wallet, bill):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 지갑과 지폐의 두 변 길이를 입력받음.
#     wallet.sort()  # sort는 원래 리스트 정렬. 지갑의 짧은 변·긴 변 순서로 정렬.
#     bill.sort()  # sort는 원래 리스트 정렬. 지폐도 짧은 변·긴 변 순서로 정렬.
#     answer = 0  # =는 값 저장. 접은 횟수 초기화.
#     while bill[0] > wallet[0] or bill[1] > wallet[1]:  # while은 조건이 참인 동안 반복. or는 한 조건 이상 참. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. >는 큼 비교. 회전해도 한 변이 지갑보다 크면 계속 접음.
#         bill[1] //= 2  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. //=는 정수 몫을 저장. 긴 변을 반으로 접고 소수 부분을 버림.
#         bill.sort()  # sort는 원래 리스트 정렬. 접은 후 다시 짧은 변·긴 변 순서로 정렬.
#         answer += 1  # +=는 더하거나 연결한 값을 저장. 접은 횟수 증가.
#     return answer  # return은 결과를 돌려주고 함수 종료. 지갑 안에 들어갈 때까지 접은 횟수 반환.

# 풀이 요약
# 지갑과 지폐의 두 변을 각각 정렬하면 회전한 경우까지 짧은 변끼리, 긴 변끼리 비교할 수 있다. 들어가지 않으면 현재 지폐의 긴 변을 절반으로 접고 다시 정렬한다. 두 변이 모두 지갑 이하가 되는 첫 순간에 멈춘다.
# 접는 횟수 F: 시간 O(F), 보조 공간 O(1). 입력 리스트를 직접 정렬한다.
