def solution(words):
    words = sorted(words)
    needed = [1] * len(words)
    for index in range(len(words) - 1):
        common = 0
        for a, b in zip(words[index], words[index + 1]):
            if a != b:
                break
            common += 1
        needed[index] = max(needed[index], common + 1)
        needed[index + 1] = max(needed[index + 1], common + 1)
    return sum(min(len(word), count) for word, count in zip(words, needed))

# 전체 코드 줄별 설명
# def solution(words):  # def는 함수 정의. 중복 없는 학습 단어 목록을 입력받음.
#     words = sorted(words)  # sorted는 원본을 바꾸지 않고 새 사전순 정렬 리스트 생성.
#     needed = [1] * len(words)  # []는 리스트, *는 반복. 모든 단어는 최소 한 글자 입력 필요.
#     for index in range(len(words) - 1):  # range로 정렬상 인접한 두 단어의 왼쪽 인덱스 순회.
#         common = 0  # 두 단어가 공유하는 접두사 길이 초기화.
#         for a, b in zip(words[index], words[index + 1]):  # zip은 같은 위치의 두 문자를 묶어 제공. 짧은 단어 길이까지만 순회.
#             if a != b:  # if는 조건문, !=는 다름 비교. 첫 다른 문자를 찾았는지 확인.
#                 break  # break는 현재 문자 비교 반복 종료.
#             common += 1  # +=는 더한 값 저장. 같은 접두사 길이 증가.
#         needed[index] = max(needed[index], common + 1)  # max는 큰 값 반환. 왼쪽 단어를 구분하려면 공통 접두사보다 한 글자 더 필요.
#         needed[index + 1] = max(needed[index + 1], common + 1)  # 오른쪽 단어도 같은 구분 길이가 필요하므로 갱신.
#     return sum(min(len(word), count) for word, count in zip(words, needed))  # min은 작은 값, len은 길이, sum은 합계. 자기 길이를 넘겨 입력할 필요는 없음.

# 풀이 요약
# 사전순에서 한 단어와 가장 긴 접두사를 공유하는 단어는 바로 앞이나 뒤에 있습니다. 인접 쌍의 공통 길이+1을 양쪽에 반영합니다.
# 단어가 다른 단어의 접두사이면 자기 단어 전체만 입력하면 됩니다. 예: go·gone·guild는 각각 2·3·2글자로 합계 7.
# 총 문자열 길이 L, 단어 수 N일 때 시간 O(L*log N), 공간 O(N).
# 