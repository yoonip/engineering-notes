# 불을 켤 등대 집합을 모두 만들어 모든 뱃길의 끝점 중 적어도 하나가 선택됐는지 확인합니다. 트리 DP를 직접 정의와
# 대조합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(n,lighthouse):
    answer=n
    for mask in range(1<<n):
        if mask.bit_count()>=answer:continue
        if all(mask&(1<<(a-1)) or mask&(1<<(b-1)) for a,b in lighthouse):
            answer=mask.bit_count()
    return answer
