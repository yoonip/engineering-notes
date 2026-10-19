# 문제: 방금그곡
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/17683
# 풀이: 샤프 음을 소문자 한 글자로 정규화한다. 재생 시간만큼 반복한 악보에서 멜로디를 찾고 길이가 같은 곡은 입력 순서를 유지한다.
# 복잡도: 곡 수 M·정규화 입력 총 길이 S·생성 재생 길이 합 T·최대 한 곡 길이 D·검색어 길이 L: 부분문자열 검색을 보수적으로 계산한 시간 상한 O(S+M L+T L), 추가 공간 O(D+L).

def solution(m, musicinfos):
    def normalize(text):
        for note in 'ABCDEFG':
            text = text.replace(note + '#', note.lower())
        return text
    target = normalize(m)
    answer, longest = '(None)', -1
    for info in musicinfos:
        start, end, title, score = info.split(',')
        duration = (int(end[:2]) - int(start[:2])) * 60 + int(end[3:]) - int(start[3:])
        melody = normalize(score)
        played = (melody * (duration // len(melody) + 1))[:duration]
        if target in played and duration > longest:
            answer, longest = title, duration
    return answer
