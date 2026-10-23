def solution(numbers):
    result = set()
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            result.add(numbers[i] + numbers[j])
    answer = sorted(result)
    return answer

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 정수 배열 numbers를 입력받는 함수
#     result = set()  # set은 중복 없는 집합. =는 값 저장. 중복된 합계를 자동으로 제거하는 빈 집합 생성
#     for i in range(len(numbers)):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. 첫 번째 숫자의 인덱스 i를 0부터 끝까지 순회
#         for j in range(i + 1, len(numbers)):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. 두 번째 숫자는 i 다음 위치부터 순회하여 같은 인덱스와 중복 조합 방지
#             result.add(numbers[i] + numbers[j])  # add는 집합에 원소 추가. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 서로 다른 두 위치의 숫자를 더해 집합에 추가
#     answer = sorted(result)  # sorted는 정렬한 새 리스트. =는 값 저장. 집합의 숫자들을 오름차순으로 정렬하여 리스트 생성
#     return answer  # return은 결과를 돌려주고 함수 종료. 중복 없이 정렬된 합계 리스트 반환

# 풀이 요약
# 서로 다른 두 인덱스를 i<j로 골라 모든 합을 구한다. 집합은 같은 합을 한 번만 남기고, 마지막 sorted가 오름차순 리스트를 만든다. 같은 값의 숫자라도 인덱스가 다르면 고를 수 있다.
# 원소 N개, 서로 다른 합 K개: 시간 O(N²+K log K), 공간 O(K).
