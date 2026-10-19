def solution(cpr):
    answer = []
    basic_order = ["check", "call", "pressure", "respiration", "repeat"]
    for action in cpr:
        for i in range(len(basic_order)):
            if action == basic_order[i]:
                answer.append(i + 1)
    return answer

# 전체 코드 줄별 설명
# def solution(cpr):  # def는 함수 정의. cpr은 무작위 순서의 동작 이름 리스트.
#     answer = []  # []는 빈 리스트. 단계 번호를 차례로 저장.
#     basic_order = ["check", "call", "pressure", "respiration", "repeat"]  # 올바른 동작 순서를 문자열 리스트로 저장.
#     for action in cpr:  # for는 반복문. 입력 동작을 하나씩 action에 넣어 처리.
#         for i in range(len(basic_order)):  # len은 길이, range는 0부터 길이-1까지의 정수 순서 생성.
#             if action == basic_order[i]:  # if는 조건, ==는 같은 값 비교, []는 인덱스 접근.
#                 answer.append(i + 1)  # append는 끝에 추가. 0부터 시작하는 인덱스에 1을 더해 단계 번호 저장.
#     return answer  # return은 계산한 단계 번호 리스트 반환.

# 풀이 요약
# 정답 순서 리스트에서 동작의 인덱스를 찾아 1을 더합니다. 예제 첫 결과는 [2, 4, 5, 1, 3]입니다.
# 