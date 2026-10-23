def solution(m, musicinfos):
    def normalize(text):
        # 기본 음 문자 순회.
        for note in 'ABCDEFG':
            text = text.replace(note + '#', note.lower())
        return text
    # 기억한 멜로디를 정규화 함수로 변환.
    target = normalize(m)
    answer, longest = '(None)', -1
    # 방송 정보가 들어온 순서대로 순회.
    for info in musicinfos:
        start, end, title, score = info.split(',')
        # 시작·종료 차이를 분으로 계산.
        duration = (int(end[:2]) - int(start[:2])) * 60 + int(end[3:]) - int(start[3:])
        melody = normalize(score)
        # 실제 재생 시간만큼 반복 후 슬라이스로 자름.
        played = (melody * (duration // len(melody) + 1))[:duration]
        if target in played and duration > longest:
            # 같은 시간은 갱신하지 않아 먼저 입력된 곡 유지.
            answer, longest = title, duration
    return answer
