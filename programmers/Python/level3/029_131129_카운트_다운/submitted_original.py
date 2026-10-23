def solution(target):
    scores = set(range(1, 21)) | {2 * value for value in range(1, 21)} | {3 * value for value in range(1, 21)} | {50}
    options = [(score, int(score <= 20 or score == 50)) for score in sorted(scores)]
    throws = [target + 1] * (target + 1)
    singles = [0] * (target + 1)
    throws[0] = 0
    for total in range(1, target + 1):
        for score, bonus in options:
            if score > total:
                break
            count = throws[total - score] + 1
            good = singles[total - score] + bonus
            if count < throws[total] or count == throws[total] and good > singles[total]:
                throws[total] = count
                singles[total] = good
    return [throws[target], singles[target]]

# 전체 코드 줄별 설명
# def solution(target):  # def는 함수 정의. target은 정확히 얻어야 할 점수.
#     scores = set(range(1, 21)) | {2 * value for value in range(1, 21)} | {3 * value for value in range(1, 21)} | {50}  # set·{} 집합 내포는 중복 제거, |는 합집합. 싱글·더블·트리플·불 점수 수집.
#     options = [(score, int(score <= 20 or score == 50)) for score in sorted(scores)]  # sorted는 오름차순. int는 참·거짓을 1·0으로 변환. 같은 점수면 싱글·불이 가능한 방법이 항상 유리.
#     throws = [target + 1] * (target + 1)  # []와 * 반복. throws[s]는 s점을 만드는 최소 다트 수.
#     singles = [0] * (target + 1)  # singles[s]는 최소 다트 수를 쓴 경우의 최대 싱글·불 횟수.
#     throws[0] = 0  # 0점은 다트를 던지지 않는 한 방법으로 시작.
#     for total in range(1, target + 1):  # range는 끝 제외. 작은 점수부터 DP를 계산.
#         for score, bonus in options:  # for~in으로 마지막에 던질 점수와 싱글·불 여부를 언패킹.
#             if score > total:  # if는 조건문, >는 초과. 남은 점수보다 큰 다트는 사용할 수 없음.
#                 break  # 정렬돼 있으므로 이후 점수도 불가능. break로 반복 종료.
#             count = throws[total - score] + 1  # 이전 점수의 최소 다트 수에 이번 한 발 추가.
#             good = singles[total - score] + bonus  # 이전 최선의 싱글·불 수에 이번 가산값 추가.
#             if count < throws[total] or count == throws[total] and good > singles[total]:  # or는 하나라도 참, and는 모두 참. 다트 수가 더 적거나 동률에서 싱글·불이 더 많을 때 갱신.
#                 throws[total] = count  # 최소 다트 수 저장.
#                 singles[total] = good  # 같은 최적해의 최대 싱글·불 수 저장.
#     return [throws[target], singles[target]]  # [] 리스트로 다트 수·싱글과 불 횟수를 순서대로 return.

# 풀이 요약
# 점수를 1부터 target까지 늘리며 마지막 다트의 점수를 모두 비교하는 DP입니다. 우선 다트 수를 최소화하고, 다트 수가 같을 때만 싱글·불을 최대화합니다.
# 동일한 점수를 싱글로도 낼 수 있으면 더블·트리플보다 항상 유리하므로 점수별 최선의 종류만 남깁니다. 서로 다른 점수 수 C≤43에 대해 시간 O(target×C), 공간 O(target).
# 예: 21은 트리플 7 한 발이라 [1,0]. 58은 불 50+싱글 8 두 발이므로 [2,2]입니다.
# 