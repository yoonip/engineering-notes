from re import match

def solution(files):
    def key(filename):
        head, number = match(r'(\D+)(\d{1,5})', filename).groups()
        return (head.lower(), int(number))
    return sorted(files, key=key)

# 전체 코드 줄별 설명
# from re import match  # re는 정규식 모듈. match는 문자열 시작부터 패턴이 맞는지 검사해 결과 객체 반환.
# 
# def solution(files):  # def는 함수 정의, files는 파일명 목록 입력.
#     def key(filename):  # 중첩 함수. 파일 하나의 정렬 기준을 반환.
#         head, number = match(r'(\D+)(\d{1,5})', filename).groups()  # r은 원시 문자열. \D+는 숫자 아닌 문자, \d{1,5}는 숫자 1~5개. () 캡처를 groups로 꺼내 언패킹.
#         return (head.lower(), int(number))  # lower는 소문자 변환, int는 선행 0을 무시한 정수 변환. () 튜플 앞값부터 비교.
#     return sorted(files, key=key)  # sorted는 새 정렬 리스트. key 함수 기준이 같으면 Python의 안정 정렬이 원래 순서를 유지.

# 풀이 요약
# 파일명을 HEAD와 최대 다섯 자리 NUMBER로 나누어 (소문자 HEAD,정수 NUMBER)를 기준으로 안정 정렬합니다. TAIL은 정렬에 쓰지 않습니다.
# 예: img1.png와 IMG01.GIF는 같은 키라 원래 순서를 유지. 파일 N개·길이 L일 때 시간 O(NL log N), 공간 O(NL).
