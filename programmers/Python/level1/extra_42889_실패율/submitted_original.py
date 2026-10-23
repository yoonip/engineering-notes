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


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(N, stages):  # def로 함수를 정의합니다. 단계 수와 사용자별 현재 단계를 받습니다.
#     counts = [0] * (N + 2)  # 0이 N+2개인 리스트입니다. 모든 단계를 통과한 N+1도 인덱스로 사용합니다.
#     for stage in stages:  # 사용자들의 단계 번호를 하나씩 꺼냅니다.
#         counts[stage] += 1  # 해당 단계에 멈춘 사람 수를 1 늘립니다.
#
#     reached = len(stages)  # len()은 원소 수입니다. 처음에는 모든 사용자가 1단계에 도달했습니다.
#     rates = []  # 단계 번호와 실패율을 담을 빈 리스트입니다.
#
#     for stage in range(1, N + 1):  # 1부터 N까지 처리합니다. range는 끝값을 제외하므로 +1합니다.
#         if reached == 0:  # ==로 도달 인원이 0인지 비교합니다.
#             rate = 0  # 도달한 사람이 없으면 실패율은 0입니다. 0으로 나누는 오류도 방지합니다.
#         else:  # 도달 인원이 있으면 실행합니다.
#             rate = counts[stage] / reached  # /는 소수 부분을 유지하는 나눗셈입니다.
#
#         rates.append((stage, rate))  # 두 값을 튜플로 묶어 리스트에 추가합니다. 예: (1, 0.125).
#         reached -= counts[stage]  # 현재 단계에 멈춘 사람은 다음 단계에 도달하지 않았으므로 제외합니다.
#
#     rates.sort(key=lambda item: (-item[1], item[0]))  # lambda는 짧은 함수입니다. 실패율 내림차순, 동점이면 번호 오름차순으로 정렬합니다.
#     return [item[0] for item in rates]  # 리스트 컴프리헨션으로 정렬된 튜플에서 단계 번호만 꺼내 반환합니다.