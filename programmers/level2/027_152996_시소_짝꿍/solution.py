from collections import Counter

def solution(weights):
    counts = Counter(weights)
    answer = 0
    for weight, count in counts.items():
        answer += count * (count - 1) // 2
        for numerator, denominator in ((2, 1), (3, 2), (4, 3)):
            if weight * numerator % denominator == 0:
                partner = weight * numerator // denominator
                answer += count * counts[partner]
    return answer

# 전체 코드 줄별 설명
# from collections import Counter  # from~import로 collections의 Counter 가져오기. 원소별 개수를 세는 딕셔너리형 자료구조.
# 
# def solution(weights):  # def는 함수 정의, weights는 몸무게 목록 입력.
#     counts = Counter(weights)  # Counter를 호출해 몸무게별 인원 수 집계.
#     answer = 0  # =는 대입. 짝의 수 초기화.
#     for weight, count in counts.items():  # items()는 (키,값) 제공. for로 몸무게·인원 수를 언패킹.
#         answer += count * (count - 1) // 2  # +=는 더해 저장, //는 정수 몫. 같은 몸무게에서 두 명을 고르는 조합 수.
#         for numerator, denominator in ((2, 1), (3, 2), (4, 3)):  # ()는 튜플. 무거운 상대와의 세 가지 무게 비를 순회.
#             if weight * numerator % denominator == 0:  # %는 나머지, ==는 같음. 상대 몸무게가 정수인 경우만 선택.
#                 partner = weight * numerator // denominator  # *는 곱셈. 정확히 나누어 상대 몸무게 계산.
#                 answer += count * counts[partner]  # [키]로 상대 인원 수 접근. Counter의 없는 키는 0, 인원 수 곱을 누적.
#     return answer  # return으로 중복 없이 센 사람 쌍 수 반환.

# 풀이 요약
# 균형 가능한 무게 비는 1:1, 1:2, 2:3, 3:4입니다. 같은 무게는 조합, 다른 무게는 인원 수의 곱으로 셉니다.
# 예: [100,180,360,100,270]은 4쌍. 더 무거운 상대만 세어 중복 방지. 사람 N명·서로 다른 무게 U개일 때 시간 O(N+U), 공간 O(U).
