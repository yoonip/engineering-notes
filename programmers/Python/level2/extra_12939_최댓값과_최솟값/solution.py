def solution(s):
    # split은 공백으로 문자열 분리, map은 각 원소에 int 정수 변환 적용, list는 결과를 재사용 가능한 리스트로 저장.
    numbers = list(map(int, s.split()))
    return f'{min(numbers)} {max(numbers)}'
