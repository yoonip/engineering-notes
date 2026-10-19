def solution(lottos, win_nums):
    matched = 0
    unknown = lottos.count(0)
    for number in lottos:
        if number in win_nums:
            matched += 1
    best_rank = min(6, 7 - (matched + unknown))
    worst_rank = min(6, 7 - matched)
    return [best_rank, worst_rank]

# 전체 코드 줄별 설명
# def solution(lottos, win_nums):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. lottos: 구매한 로또 번호, win_nums: 당첨 번호 목록
#     matched = 0  # =는 값 저장. 알아볼 수 있는 번호 중 당첨 번호와 일치하는 개수를 저장
#     unknown = lottos.count(0)  # count는 등장 횟수. =는 값 저장. 0의 개수를 셈. 0은 지워져서 알 수 없는 번호를 의미
#     for number in lottos:  # for·in은 원소를 차례로 꺼내는 반복문. 구매한 번호를 하나씩 꺼내서 확인
#         if number in win_nums:  # if는 조건이 참일 때 실행. in은 포함 여부. 현재 번호가 당첨 번호 목록 안에 있는지 검사
#             matched += 1  # +=는 더하거나 연결한 값을 저장. 당첨 번호에 있다면 맞은 개수를 1 증가시킴
#     best_rank = min(6, 7 - (matched + unknown))  # min은 최솟값. =는 값 저장. 모르는 번호까지 전부 맞았을 때의 최고 순위
#     worst_rank = min(6, 7 - matched)  # min은 최솟값. =는 값 저장. 모르는 번호가 전부 틀렸을 때의 최저 순위
#     return [best_rank, worst_rank]  # return은 결과를 돌려주고 함수 종료. []는 리스트. [최고 순위, 최저 순위]를 리스트로 반환

# 풀이 요약
# 확실히 맞힌 수와 알아볼 수 없는 0의 수를 센다. 최고 순위는 0이 전부 당첨인 경우, 최저 순위는 0이 전부 빗나간 경우다. 0개·1개를 맞혀도 6등이므로 7-일치수의 상한을 6으로 제한한다.
# 로또와 당첨 번호가 각각 6개이므로 시간·보조 공간 O(1).
