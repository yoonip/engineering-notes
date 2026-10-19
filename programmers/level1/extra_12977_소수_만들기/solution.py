from itertools import combinations

def solution(nums):
    answer = 0
    for a, b, c in combinations(nums, 3):
        total = a + b + c
        is_prime = True
        for i in range(2, int(total ** 0.5) + 1):
            if total % i == 0:
                is_prime = False
                break
        if is_prime:
            answer += 1
    return answer

# 전체 코드 줄별 설명
# from itertools import combinations  # from itertools import는 itertools 모듈에서 이름을 가져옴. combinations는 순서를 구별하지 않는 원소 조합을 만드는 함수. 숫자 여러 개를 중복 없이 선택하는 조합 함수를 가져옴
# 
# def solution(nums):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. nums: 서로 다른 숫자들이 들어 있는 리스트
#     answer = 0  # =는 값 저장. 합이 소수가 되는 조합의 개수를 저장. 처음에는 0
#     for a, b, c in combinations(nums, 3):  # for·in은 원소를 차례로 꺼내는 반복문. combinations는 중복 선택 없는 조합 생성. ()로 묶은 여러 값은 변경 불가 튜플. nums에서 숫자 3개를 선택하는 모든 조합을 하나씩 꺼냄
#         total = a + b + c  # =는 값 저장. 선택한 숫자 3개를 더한 결과를 total에 저장
#         is_prime = True  # =는 값 저장. True·False는 참·거짓. 일단 합계가 소수라고 가정하고 검사 시작
#         for i in range(2, int(total ** 0.5) + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. int는 정수 변환. **는 거듭제곱. 2부터 total의 제곱근까지 나누어떨어지는지 검사
#             if total % i == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. total을 i로 나눈 나머지가 0이면 약수가 존재한다는 뜻
#                 is_prime = False  # =는 값 저장. True·False는 참·거짓. 1과 자기 자신 이외의 약수가 있으므로 소수가 아님
#                 break  # break는 가장 가까운 반복문 종료. 소수가 아님을 확인했으므로 더 검사하지 않고 안쪽 for문 종료
#         if is_prime:  # if는 조건이 참일 때 실행. 모든 약수 검사를 통과해서 소수인 경우
#             answer += 1  # +=는 더하거나 연결한 값을 저장. 소수인 조합을 하나 발견했으므로 개수를 1 증가
#     return answer  # return은 결과를 돌려주고 함수 종료. 합이 소수가 되는 모든 조합의 개수를 반환

# 풀이 요약
# 세 원소의 조합을 중복 없이 만들고 합의 약수를 검사한다. 합성수라면 약수 쌍 중 하나가 제곱근 이하에 있으므로 그까지만 나누면 충분하다. 약수가 발견되면 즉시 중단하고, 없었던 조합만 센다.
# 원소 N개, 최대 합 M: 시간 O(C(N,3)√M), 조합 반복자의 입력 보관 공간 O(N).
