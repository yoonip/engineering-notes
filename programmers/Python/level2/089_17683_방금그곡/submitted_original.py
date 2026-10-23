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

# 전체 코드 줄별 설명
# def solution(m, musicinfos):  # def는 함수 정의. 기억한 멜로디·방송 곡 정보 입력.
#     def normalize(text):  # 중첩 함수. # 붙은 음을 한 글자로 바꿔 음 단위 비교.
#         for note in 'ABCDEFG':  # for~in으로 기본 음 문자 순회.
#             text = text.replace(note + '#', note.lower())  # +는 연결, lower는 소문자 변환, replace는 치환. C# 등을 c처럼 표현.
#         return text  # return으로 음 하나당 문자 하나인 문자열 반환.
#     target = normalize(m)  # 기억한 멜로디를 정규화 함수로 변환.
#     answer, longest = '(None)', -1  # 일치 곡이 없을 때의 제목·현재 최장 재생 시간 초기화.
#     for info in musicinfos:  # 방송 정보가 들어온 순서대로 순회.
#         start, end, title, score = info.split(',')  # split은 쉼표 기준 분리. 네 필드를 언패킹.
#         duration = (int(end[:2]) - int(start[:2])) * 60 + int(end[3:]) - int(start[3:])  # 슬라이스로 시·분 추출, int로 정수 변환. 시작·종료 차이를 분으로 계산.
#         melody = normalize(score)  # 악보의 # 음도 같은 방법으로 한 문자로 변환.
#         played = (melody * (duration // len(melody) + 1))[:duration]  # len은 음 수, //는 정수 몫, *는 문자열 반복. 실제 재생 시간만큼 반복 후 슬라이스로 자름.
#         if target in played and duration > longest:  # in은 부분 문자열 검사, and는 둘 다 참, >는 큼. 일치하면서 더 오래 재생된 곡 선택.
#             answer, longest = title, duration  # 같은 시간은 갱신하지 않아 먼저 입력된 곡 유지.
#     return answer  # 찾은 제목 또는 '(None)' 반환.

# 풀이 요약
# # 음을 소문자 한 글자로 바꾼 뒤, 실제 방송 길이만큼 악보를 반복·절단해 기억한 멜로디를 찾습니다. 동률은 먼저 입력된 곡입니다.
# 예: ABC는 ABC#과 다르므로 세 번째 예제의 답은 WORLD. 실제 생성 재생 문자열의 총 길이에 비례하는 시간, 최대 한 곡 재생 길이에 비례하는 임시 공간.
