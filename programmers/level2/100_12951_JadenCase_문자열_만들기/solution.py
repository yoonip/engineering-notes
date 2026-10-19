def solution(s):
    # 인수를 생략한 split()과 달리 연속·앞뒤 공백을 빈 원소로 보존.
    words = s.split(' ')
    changed = [word.capitalize() for word in words]
    return ' '.join(changed)
