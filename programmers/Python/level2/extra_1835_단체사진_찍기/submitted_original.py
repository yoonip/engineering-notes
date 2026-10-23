from itertools import permutations

def solution(n, data):
    conditions = [(text[0], text[2], text[3], int(text[4])) for text in data]
    answer = 0
    for order in permutations('ACFJMNRT'):
        positions = {friend: i for i, friend in enumerate(order)}
        for first, second, operator, wanted in conditions:
            gap = abs(positions[first] - positions[second]) - 1
            if operator == '=' and gap != wanted:
                break
            if operator == '<' and gap >= wanted:
                break
            if operator == '>' and gap <= wanted:
                break
        else:
            answer += 1
    return answer

# 전체 코드 줄별 설명
# from itertools import permutations  # import는 도구 가져오기. permutations는 원소를 순서 있게 배치한 모든 순열을 생성.
# 
# def solution(n, data):  # def는 함수 정의. 조건 개수와 다섯 글자 조건 문자열 목록 입력.
#     conditions = [(text[0], text[2], text[3], int(text[4])) for text in data]  # []는 리스트 컴프리헨션, ()는 튜플, int는 정수 변환. 두 친구·연산자·간격으로 조건 분리.
#     answer = 0  # 모든 조건을 만족하는 순서 수.
#     for order in permutations('ACFJMNRT'):  # 여덟 친구의 모든 줄서기 순회.
#         positions = {friend: i for i, friend in enumerate(order)}  # {}는 딕셔너리 컴프리헨션, enumerate는 번호·값 제공. 친구별 위치를 빠르게 조회할 표 생성.
#         for first, second, operator, wanted in conditions:  # 각 조건의 네 값을 언패킹.
#             gap = abs(positions[first] - positions[second]) - 1  # abs는 절댓값, []는 키 조회. 둘 사이의 다른 사람 수 계산.
#             if operator == '=' and gap != wanted:  # ==는 같음, !=는 다름, and는 모두 참. 같음 조건 위반이면 제외.
#                 break  # 현재 순서의 조건 검사 종료.
#             if operator == '<' and gap >= wanted:  # 미만 조건을 만족하지 못하면 제외.
#                 break  # 다음 줄서기 순서로 이동.
#             if operator == '>' and gap <= wanted:  # 초과 조건을 만족하지 못하면 제외.
#                 break  # 조건 검사 종료.
#         else:  # for가 break 없이 끝난 경우에만 실행. 모든 조건을 만족함.
#             answer += 1  # +=는 더해 저장. 유효한 순서 하나 추가.
#     return answer  # 조건을 만족하는 전체 경우의 수 반환.

# 풀이 요약
# 친구는 여덟 명으로 고정되어 8!=40320개 순서를 모두 검사할 수 있다. 각 순서에서 친구의 위치를 기록하고 모든 조건을 확인한다.
# 두 친구 사이의 다른 사람 수는 abs(위치 차이)-1이다. 옆에 서 있으면 간격은 1이 아니라 0이다.
# 예제 1은 인접 조건과 최소 간격 조건을 함께 만족하는 순서 3648개. 조건 Q개일 때 시간 O(8!·(8+Q)), 추가 공간 O(8+Q).
# 