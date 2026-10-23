def solution(citations):
    citations.sort(reverse=True)
    answer = 0
    for count, cited in enumerate(citations, 1):
        if cited < count:
            break
        answer = count
    return answer

# 전체 코드 줄별 설명
# def solution(citations):  # def는 함수 정의. citations는 논문별 인용 횟수 목록.
#     citations.sort(reverse=True)  # sort는 제자리 정렬, reverse=True는 내림차순. 많이 인용된 논문부터 배치.
#     answer = 0  # =는 대입. 가능한 H-Index 초기화.
#     for count, cited in enumerate(citations, 1):  # enumerate(목록,1)은 논문 수를 1부터 부여. 개수·인용 횟수 언패킹.
#         if cited < count:  # if는 분기, <는 작음. 이 논문까지 count편이 count회 이상 인용되는지 검사.
#             break  # break는 반복 종료. 뒤 논문은 더 적게 인용돼 더 큰 h가 불가능.
#         answer = count  # 조건을 만족한 논문 수로 H-Index 갱신.
#     return answer  # return으로 가능한 최대 h 반환.

# 풀이 요약
# 인용 횟수를 내림차순으로 정렬하면 h번째 논문의 인용 수가 h 이상일 때 h편 이상이 h회 이상 인용됩니다.
# 예: [6,5,3,1,0]에서 세 번째 값 3까지 가능해 답 3. 시간 O(N log N), 정렬 공간 O(N).
