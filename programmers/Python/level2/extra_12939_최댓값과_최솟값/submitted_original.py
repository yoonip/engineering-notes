def solution(s):
    numbers = list(map(int, s.split()))
    return f'{min(numbers)} {max(numbers)}'

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 공백으로 구분된 정수 문자열 입력.
#     numbers = list(map(int, s.split()))  # split은 공백으로 문자열 분리, map은 각 원소에 int 정수 변환 적용, list는 결과를 재사용 가능한 리스트로 저장.
#     return f'{min(numbers)} {max(numbers)}'  # min·max는 최솟값·최댓값. f문자열의 {} 안 값을 문자열에 넣고 사이에 공백 하나 추가.

# 풀이 요약
# 문자열을 숫자 목록으로 바꾼 뒤 최소·최대를 구한다. 문자열 상태로 비교하면 10이 2보다 작게 정렬될 수 있어 int 변환이 필요하다.
# 예: -1 -2 -3 -4는 -4 -1을 반환한다. 숫자 K개·문자열 길이 L일 때 시간 O(L), 공간 O(L).
# 