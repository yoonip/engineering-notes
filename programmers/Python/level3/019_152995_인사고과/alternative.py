# 각 사원보다 두 점수가 모두 높은 사원이 있는지 직접 검사합니다. 정렬의 동점 처리와 탈락 판정을 검증하는 기준
# 코드입니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(scores):
    eligible = [not any(c>a and d>b for c,d in scores) for a,b in scores]
    if not eligible[0]:
        return -1
    target = sum(scores[0])
    return 1+sum(ok and sum(row)>target for row,ok in zip(scores,eligible))
