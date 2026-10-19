def solution(n, words):
    seen = set()
    for index, word in enumerate(words):
        if word in seen or (index > 0 and words[index - 1][-1] != word[0]):
            return [index % n + 1, index // n + 1]
        seen.add(word)
    return [0, 0]

# 전체 코드 줄별 설명
# def solution(n, words):  # def는 함수 정의. 참가자 수·말한 단어 목록 입력.
#     seen = set()  # set은 중복 없는 집합. 이미 사용한 단어 저장.
#     for index, word in enumerate(words):  # enumerate는 (인덱스,값) 제공. 발언 순서·단어를 언패킹.
#         if word in seen or (index > 0 and words[index - 1][-1] != word[0]):  # in은 중복 검사, or·and는 논리 연산. [-1]은 이전 단어 끝, [0]은 현재 첫 글자. !=면 연결 위반.
#             return [index % n + 1, index // n + 1]  # %는 나머지, //는 몫. 0부터인 순서를 1부터인 사람 번호·개인 차례로 변환해 리스트 반환.
#         seen.add(word)  # add로 이번 단어를 사용 목록에 추가.
#     return [0, 0]  # 끝까지 위반이 없으면 탈락자가 없다는 결과 반환.

# 풀이 요약
# 단어 중복과 앞 단어 끝·현재 단어 시작의 일치를 검사합니다. 처음 위반한 발언 인덱스의 나머지·몫으로 사람과 차례를 구합니다.
# 예: 3명이 9번째 tank를 다시 말하면 인덱스 8이므로 [3,3]. 전체 단어 길이 합 L에 대해 시간·공간 O(L).
