def solution(words):
    words = sorted(words)  # sorted는 원본을 바꾸지 않고 새 사전순 정렬 리스트 생성.
    needed = [1] * len(words)  # []는 리스트, *는 반복. 모든 단어는 최소 한 글자 입력 필요.
    for index in range(len(words) - 1):  # range로 정렬상 인접한 두 단어의 왼쪽 인덱스 순회.
        common = 0  # 두 단어가 공유하는 접두사 길이 초기화.
        for a, b in zip(words[index], words[index + 1]):  # zip은 같은 위치의 두 문자를 묶어 제공. 짧은 단어 길이까지만 순회.
            if a != b:
                break  # break는 현재 문자 비교 반복 종료.
            common += 1
        needed[index] = max(needed[index], common + 1)  # max는 큰 값 반환. 왼쪽 단어를 구분하려면 공통 접두사보다 한 글자 더 필요.
        needed[index + 1] = max(needed[index + 1], common + 1)  # 오른쪽 단어도 같은 구분 길이가 필요하므로 갱신.
    return sum(min(len(word), count) for word, count in zip(words, needed))
