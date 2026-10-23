def solution(storey):
    answer = 0
    while storey:
        storey, digit = divmod(storey, 10)
        if digit > 5 or (digit == 5 and storey % 10 >= 5):
            answer += 10 - digit
            storey += 1
        else:
            answer += digit
    return answer

# 전체 코드 줄별 설명
# def solution(storey):  # def는 함수 정의. storey는 현재 층 입력.
#     answer = 0  # =는 대입. 사용한 돌 수 초기화.
#     while storey:  # while은 조건 반복. 층이 0이면 거짓이 되어 종료.
#         storey, digit = divmod(storey, 10)  # divmod는 (몫,나머지) 반환. 두 값을 언패킹해 다음 자리와 현재 자리 분리.
#         if digit > 5 or (digit == 5 and storey % 10 >= 5):  # >·==·>=는 비교, or는 하나 이상 참, and는 둘 다 참, %는 나머지. 올림이 유리한 경우 검사.
#             answer += 10 - digit  # +=는 더해 저장. 현재 자리를 10까지 올리는 버튼 수 누적.
#             storey += 1  # 올림으로 다음 자리에 1 전달.
#         else:  # else는 앞 조건이 거짓인 경우.
#             answer += digit  # 현재 자리를 0까지 내리는 버튼 수 누적.
#     return answer  # return으로 최소 돌 개수 반환.

# 풀이 요약
# 일의 자리부터 0으로 만듭니다. 5보다 크면 올리고 작으면 내리며, 5면 다음 자리가 5 이상일 때 올립니다.
# 예: 16은 +1 네 번, -10 두 번으로 6개. 시간 O(log10(storey)), 공간 O(1).
