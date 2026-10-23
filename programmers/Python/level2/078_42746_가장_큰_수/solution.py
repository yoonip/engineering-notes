def solution(numbers):
    # map은 각 원소에 str을 적용해 문자열 변환, list는 목록으로 저장.
    parts = list(map(str, numbers))
    parts.sort(key=lambda value: value * 4, reverse=True)
    # 가장 앞이 0이면 모든 수가 0.
    if parts[0] == '0':
        return '0'
    return ''.join(parts)
