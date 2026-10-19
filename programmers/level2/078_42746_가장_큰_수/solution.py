def solution(numbers):
    parts = list(map(str, numbers))
    parts.sort(key=lambda value: value * 4, reverse=True)
    if parts[0] == '0':
        return '0'
    return ''.join(parts)

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. numbers는 0~1000 정수 목록 입력.
#     parts = list(map(str, numbers))  # map은 각 원소에 str을 적용해 문자열 변환, list는 목록으로 저장.
#     parts.sort(key=lambda value: value * 4, reverse=True)  # sort는 제자리 정렬, lambda는 짧은 함수. 최대 네 자리이므로 *4 반복 문자열을 비교키로 내림차순 정렬.
#     if parts[0] == '0':  # []는 첫 원소 접근, ==는 같음. 가장 앞이 0이면 모든 수가 0.
#         return '0'  # 여러 0을 이어 붙이지 않고 문자열 '0' 반환.
#     return ''.join(parts)  # join으로 정렬한 숫자 문자열들을 연결해 반환. 큰 정수로 변환할 필요 없음.

# 풀이 요약
# 앞뒤 연결 순서에서 더 큰 수를 만드는 숫자를 먼저 둡니다. 입력은 1000 이하라 반복 문자열 비교로 그 순서를 정할 수 있습니다.
# 예: [3,30,34,5,9]→9·5·34·3·30→'9534330'. 숫자 N개일 때 시간 O(N log N), 공간 O(N).
