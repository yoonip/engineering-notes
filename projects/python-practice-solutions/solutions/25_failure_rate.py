# 실패율
# 분류: 빈도 집계 / 정렬
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/42889
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(N, stages):
    counts = [0] * (N + 2)
    for stage in stages:
        counts[stage] += 1

    reached = len(stages)
    rates = []

    for stage in range(1, N + 1):
        if reached == 0:
            rate = 0
        else:
            rate = counts[stage] / reached

        rates.append((stage, rate))
        reached -= counts[stage]

    rates.sort(key=lambda item: (-item[1], item[0]))
    return [item[0] for item in rates]


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(N, stages):  # def로 함수를 정의합니다. N은 단계 수, stages는 각 사용자가 멈춘 단계 리스트입니다.
#     counts = [0] * (N + 2)  # 0이 N+2개인 리스트입니다. 인덱스 0부터 N+1까지 사용할 수 있습니다.
#     for stage in stages:  # 사용자들의 단계 번호를 하나씩 꺼냅니다.
#         counts[stage] += 1  # 해당 단계 번호를 인덱스로 사용해 인원을 1 늘립니다. +=는 더해서 다시 저장합니다.
#
#     reached = len(stages)  # len()은 원소 수입니다. 1단계에는 모든 사용자가 도달했으므로 전체 인원부터 시작합니다.
#     rates = []  # (단계 번호, 실패율) 튜플을 담을 빈 리스트입니다.
#
#     for stage in range(1, N + 1):  # range는 끝값을 제외하므로 +1하여 1단계부터 N단계까지 처리합니다.
#         if reached == 0:  # ==는 같은지 비교합니다. 도달 인원이 0인지 확인합니다.
#             rate = 0  # 이 경우 실패율을 0으로 저장하여 0으로 나누는 오류도 방지합니다.
#         else:  # 도달 인원이 있는 경우 실행합니다.
#             rate = counts[stage] / reached  # /는 나눗셈입니다. //와 달리 소수 부분을 유지합니다.
#
#         rates.append((stage, rate))  # 두 값을 튜플로 묶고 append()로 리스트 뒤에 추가합니다. 튜플은 원소를 바꿀 수 없는 값의 묶음입니다.
#         reached -= counts[stage]  # -=는 빼서 다시 저장합니다. 현재 단계에 멈춘 사람은 다음 단계에 도달하지 않았으므로 제외합니다.
#
#     rates.sort(key=lambda item: (-item[1], item[0]))  # lambda는 짧은 함수입니다. 정렬 키 튜플은 첫 값부터 비교합니다. 실패율에 -를 붙여 큰 실패율이 먼저, 동점은 작은 번호가 먼저 옵니다.
#     return [item[0] for item in rates]  # 리스트 컴프리헨션으로 정렬된 튜플의 0번 값인 단계 번호만 꺼내 반환합니다.
#
