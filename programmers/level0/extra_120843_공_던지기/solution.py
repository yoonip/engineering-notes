def solution(numbers, k):
    return numbers[(2 * (k - 1)) % len(numbers)]

# 전체 코드 줄별 설명
# def solution(numbers, k):  # def는 함수 정의. 사람 번호 리스트와 던지는 순번 입력.
#     return numbers[(2 * (k - 1)) % len(numbers)]  # []는 인덱스 접근, %는 순환을 위한 나머지, len은 사람 수. 첫 던지기는 이동 0번이고 매번 두 칸씩 이동.

# 풀이 요약
# k번째로 던지는 사람은 처음 위치에서 2*(k-1)칸 이동한 위치입니다.
# 