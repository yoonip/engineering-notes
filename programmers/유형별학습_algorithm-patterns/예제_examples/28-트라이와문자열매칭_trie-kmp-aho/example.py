import sys  # 소문자 문자열 토큰 읽기
tokens = iter(sys.stdin.read().split())  # 공백 토큰 순회
n = int(next(tokens))  # 사전 크기
children = [[0] * 26]  # 0번 루트의 자식 표
terminal = [False]  # 각 접두사의 단어 종료 여부
for _ in range(n):  # 사전 삽입
    node = 0  # 루트에서 시작
    for character in next(tokens):  # 단어의 문자 순회
        letter = ord(character) - ord("a")  # 자식 번호
        if children[node][letter] == 0:  # 아직 없는 간선 확인
            children[node][letter] = len(children)  # 새 노드의 번호 연결
            children.append([0] * 26)  # 자식 표 생성
            terminal.append(False)  # 초기 종료 표시
        node = children[node][letter]  # 접두사 이동
    terminal[node] = True  # 단어 끝 보관
query, text, pattern = next(tokens), next(tokens), next(tokens)  # 두 탐색의 입력
node, exists = 0, True  # 질의 경로 초기 상태
for character in query:  # 트라이 접두사 확인
    child = children[node][ord(character) - ord("a")]  # 다음 문자 간선
    if child == 0:  # 경로가 없는 상태
        exists = False  # 접두사도 부재
        break  # 추가 탐색 중단
    node = child  # 접두사 이동
pi = [0] * len(pattern)  # 패턴의 접두·접미 경계 표
for i in range(1, len(pattern)):  # 경계를 한 문자씩 확장
    j = pi[i - 1]  # 직전 경계 길이
    while j and pattern[i] != pattern[j]:  # 경계 뒤 문자가 불일치
        j = pi[j - 1]  # 더 짧은 경계 복구
    if pattern[i] == pattern[j]:  # 경계 확장 가능
        j += 1  # 새 일치 길이
    pi[i] = j  # 현재 경계 저장
matched, count = 0, 0  # 텍스트 일치 길이와 발생 수
for character in text:  # 텍스트를 되돌리지 않는 검색
    while matched and character != pattern[matched]:  # 불일치 복구
        matched = pi[matched - 1]  # 겹친 후보 유지
    if character == pattern[matched]:  # 현재 문자 일치
        matched += 1  # 일치 길이 증가
    if matched == len(pattern):  # 패턴 전체 발생
        count += 1  # 결과 누적
        matched = pi[matched - 1]  # 겹치는 다음 발생 준비
print("WORD", "YES" if exists and terminal[node] else "NO")  # 완전 단어 출력
print("PREFIX", "YES" if exists else "NO")  # 접두사 출력
print("MATCHES", count)  # KMP 발생 수 출력
