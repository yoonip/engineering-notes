def solution(N, number):
    values = [set() for _ in range(9)]
    for count in range(1, 9):
        values[count].add(int(str(N) * count))
        for left_count in range(1, count):
            right_count = count - left_count
            for first in values[left_count]:
                for second in values[right_count]:
                    values[count].add(first + second)
                    values[count].add(first - second)
                    values[count].add(first * second)
                    if second != 0:
                        values[count].add(int(first / second))
        if number in values[count]:
            return count
    return -1

# 전체 코드 줄별 설명
# def solution(N, number):  # def는 함수 정의. 사용할 한 자리 숫자와 목표 정수를 받음.
#     values = [set() for _ in range(9)]  # []는 리스트, set()은 빈 집합. values[i]는 N을 정확히 i번 쓴 수식의 모든 결과. 중복은 집합으로 제거.
#     for count in range(1, 9):  # range는 끝 제외. N 사용 횟수를 1~8 순서로 늘림.
#         values[count].add(int(str(N) * count))  # str은 문자열 변환, *는 반복, int는 정수 변환. 5,55,555처럼 붙인 숫자 추가.
#         for left_count in range(1, count):  # 전체 수식을 왼쪽과 오른쪽 두 부분으로 나누는 모든 사용 횟수 시도.
#             right_count = count - left_count  # 오른쪽 수식에 쓸 N의 개수.
#             for first in values[left_count]:  # for로 왼쪽 수식의 가능한 결과 순회.
#                 for second in values[right_count]:  # 오른쪽 수식의 가능한 결과 순회.
#                     values[count].add(first + second)  # add는 집합에 추가. 덧셈 결과 저장.
#                     values[count].add(first - second)  # 뺄셈 결과 저장. 순서가 다른 경우도 반복에서 포함됨.
#                     values[count].add(first * second)  # 곱셈 결과 저장.
#                     if second != 0:  # !=는 다름. 0으로 나누는 연산 제외.
#                         values[count].add(int(first / second))  # /는 나눗셈, int는 소수 부분을 0 방향으로 버림. 음수 결과도 나머지를 버리는 규칙 적용.
#         if number in values[count]:  # in은 집합 포함 여부. 목표 결과를 만들 수 있는지 검사.
#             return count  # 적은 횟수부터 확인했으므로 처음 발견한 횟수가 최소.
#     return -1  # 8번까지 목표를 만들 수 없으면 -1 반환.

# 풀이 요약
# N을 i번 사용한 결과 집합을 만든다. 붙여 쓰기 외의 수식은 마지막 연산을 기준으로 두 작은 수식으로 나눌 수 있으므로 네 연산을 전부 조합한다.
# 예: (55+5)/5=12는 왼쪽 세 번·오른쪽 한 번을 조합하여 총 네 번. 음수·0도 이후 수식에 필요할 수 있어 보관한다.
# 집합 DP로 같은 결과를 한 번만 저장한다. 시간은 분할별 두 결과 집합 크기의 곱의 합, 공간은 1~8회 결과 집합 크기의 합.
# 