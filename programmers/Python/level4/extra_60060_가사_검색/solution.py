from bisect import bisect_left, bisect_right  # from A import B는 모듈에서 함수 가져오기. bisect는 정렬된 리스트에서 이진 탐색으로 삽입 위치를 찾음.

def solution(words, queries):
    forward, backward = {}, {}  # {}는 빈 딕셔너리. 길이별 정방향·역방향 단어 목록 저장.
    for word in words:
        length = len(word)
        forward.setdefault(length, []).append(word)  # setdefault는 키가 없으면 빈 리스트 생성. append로 단어 추가.
        backward.setdefault(length, []).append(word[::-1])  # [::-1]은 역순 슬라이스. 접미사 검색을 접두사 검색으로 바꾸기 위해 뒤집어 저장.
    for groups in (forward, backward):  # ()는 튜플. 두 딕셔너리를 차례대로 처리.
        for group in groups.values():  # values()는 딕셔너리의 값들인 단어 목록을 제공.
            group.sort()  # sort()는 리스트 자체를 사전순으로 정렬.
    answer = []  # []는 빈 리스트. 패턴별 일치 단어 개수 저장.
    for query in queries:  # 주어진 검색 순서를 유지하여 순회.
        if query[0] == '?':
            query = query[::-1]  # 패턴을 뒤집어 ?가 뒤에 오도록 변경.
            group = backward.get(len(query), [])  # get은 키가 없으면 기본값 반환. 같은 길이의 역방향 단어 목록 선택.
        else:  # else는 앞 조건이 거짓일 때 실행.
            group = forward.get(len(query), [])  # 같은 길이의 정방향 단어 목록 선택.
        low = query.replace('?', 'a')  # replace는 문자열의 지정 문자를 치환. 소문자 최솟값으로 검색 하한 생성.
        high = query.replace('?', 'z')  # 소문자 최댓값으로 검색 상한 생성.
        count = bisect_right(group, high) - bisect_left(group, low)  # 상한 초과 위치-하한 이상 위치로 닫힌 범위의 단어 개수 계산.
        answer.append(count)  # 패턴의 일치 개수를 정답 끝에 추가.
    return answer  # return으로 검색 순서대로 결과 목록 반환.
