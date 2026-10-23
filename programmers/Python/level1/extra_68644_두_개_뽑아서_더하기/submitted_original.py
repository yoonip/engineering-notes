
def solution(numbers):
    result = set()

    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            result.add(numbers[i] + numbers[j])

    answer = sorted(result)

    return answer


# ========== 공부용 코드 (전체 주석 처리) ==========

# def solution(numbers):                         # 정수 배열 numbers를 입력받는 함수
#     result = set()                             # 중복된 합계를 자동으로 제거하는 빈 집합 생성
#
#     for i in range(len(numbers)):              # 첫 번째 숫자의 인덱스 i를 0부터 끝까지 순회
#         for j in range(i + 1, len(numbers)):   # 두 번째 숫자는 i 다음 위치부터 순회하여 같은 인덱스와 중복 조합 방지
#             result.add(numbers[i] + numbers[j]) # 서로 다른 두 위치의 숫자를 더해 집합에 추가
#
#     answer = sorted(result)                    # 집합의 숫자들을 오름차순으로 정렬하여 리스트 생성
#
#     return answer                              # 중복 없이 정렬된 합계 리스트 반환
