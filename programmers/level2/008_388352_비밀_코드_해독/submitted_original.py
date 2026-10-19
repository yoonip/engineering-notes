from itertools import combinations


def solution(n, q, ans):
    attempts = [set(attempt) for attempt in q]
    answer = 0

    for candidate in combinations(range(1, n + 1), 5):
        code = set(candidate)
        valid = True
        for attempt, matched in zip(attempts, ans):
            if len(code & attempt) != matched:
                valid = False
                break
        if valid:
            answer += 1

    return answer

# 전체 코드 줄별 설명 (아래는 모두 실행되지 않는 주석입니다.)
# from itertools import combinations  # from~import는 모듈에서 이름을 가져옴. itertools는 반복 도구 모듈, combinations는 중복 없는 조합을 차례로 만드는 함수.
#
#
# def solution(n, q, ans):  # def는 함수 정의. n,q,ans는 입력 매개변수.
#     attempts = [set(attempt) for attempt in q]  # set은 중복 없는 집합 생성. [식 for~in]은 각 시도를 집합으로 바꾸는 리스트 컴프리헨션.
#     answer = 0  # 유효한 후보 수 초기화. =는 대입.
#
#     for candidate in combinations(range(1, n + 1), 5):  # range(1,n+1)은 1..n. combinations(...,5)는 순서 없이 5개 고른 튜플을 제공, for로 순회.
#         code = set(candidate)  # 후보 튜플을 집합으로 변환해 교집합 계산 준비.
#         valid = True  # True는 참. 일단 유효한 후보라고 표시.
#         for attempt, matched in zip(attempts, ans):  # zip은 같은 위치의 값들을 짝지음. 쉼표 언패킹으로 시도 집합과 일치 개수를 받음.
#             if len(code & attempt) != matched:  # &는 집합 교집합, len은 원소 수, !=는 다름 비교. 일치 개수가 틀리면 실행.
#                 valid = False  # False는 거짓. 조건에 안 맞는 후보라고 표시.
#                 break  # break는 가장 가까운 반복문을 종료. 나머지 시도 검사를 생략.
#         if valid:  # if는 조건부 실행. 모든 시도를 만족한 후보인지 확인.
#             answer += 1  # += 1은 1을 더해 저장. 유효 후보를 한 개 셈.
#
#     return answer  # return으로 후보 수 반환.

# 풀이 요약
# 1..n에서 서로 다른 5개를 고른 모든 조합을 검사합니다. 각 시도와의 교집합 크기가 ans와 모두 같으면 정답 후보입니다.
# 예: 후보 {1,2,3,4,5}, 시도 {1,2,6,7,8}의 일치 개수는 2입니다. 시간 O(nC5*시도 수), 집합 크기는 5로 고정입니다.
