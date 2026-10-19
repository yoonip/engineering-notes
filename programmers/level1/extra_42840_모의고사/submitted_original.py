
def solution(answers):
    patterns = [
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]
    ]

    scores = [0, 0, 0]

    for i, answer in enumerate(answers):
        for j in range(3):
            if answer == patterns[j][i % len(patterns[j])]:
                scores[j] += 1

    max_score = max(scores)

    result = [i + 1 for i in range(3) if scores[i] == max_score]

    return result


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(answers):                                  # 실제 문제의 정답 리스트를 입력받는 함수
#     patterns = [                                        # 3명의 수포자가 반복해서 찍는 답안 패턴
#         [1, 2, 3, 4, 5],                               # 1번 수포자의 반복 패턴
#         [2, 1, 2, 3, 2, 4, 2, 5],                      # 2번 수포자의 반복 패턴
#         [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]                # 3번 수포자의 반복 패턴
#     ]
#
#     scores = [0, 0, 0]                                 # 각 수포자의 정답 개수를 0으로 초기화
#
#     for i, answer in enumerate(answers):               # 실제 정답의 인덱스 i와 정답 answer를 순서대로 가져옴
#         for j in range(3):                             # 0, 1, 2번 인덱스로 세 수포자를 순회
#             if answer == patterns[j][i % len(patterns[j])]:  # 실제 정답과 해당 수포자가 찍은 답이 같으면
#                 scores[j] += 1                         # 해당 수포자의 정답 개수를 1 증가
#
#     max_score = max(scores)                             # 세 수포자 중 가장 높은 정답 개수를 구함
#
#     result = [i + 1 for i in range(3) if scores[i] == max_score]  # 최고 점수와 같은 수포자의 번호를 리스트로 저장
#
#     return result                                      # 가장 많이 맞힌 수포자 번호들을 오름차순으로 반환
