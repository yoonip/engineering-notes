
from collections import Counter

def solution(participant, completion):
    p_counter = Counter(participant)
    c_counter = Counter(completion)

    result = p_counter - c_counter
    answer = list(result.keys())[0]

    return answer


from collections import Counter  # 값별 개수를 세는 도구를 가져옴

def solution(participant, completion):  # 참가자와 완주자 목록을 받음
    p_counter = Counter(participant)  # 이름별 참가 인원수 계산
    c_counter = Counter(completion)  # 이름별 완주 인원수 계산

    result = p_counter - c_counter  # 빼고 나면 완주하지 못한 사람만 남음

    for name in result:  # 남아 있는 이름을 꺼냄
        return name  # 해당 이름 반환



def solution(participant, completion):  # 참가자와 완주자 목록을 받음
    counts = {}  # 이름별 인원수를 저장할 빈 딕셔너리

    for name in participant:  # 참가자 이름을 하나씩 꺼냄
        if name in counts:  # 이미 기록한 이름이면
            counts[name] = counts[name] + 1  # 인원수 1 증가
        else:  # 처음 나온 이름이면
            counts[name] = 1  # 인원수를 1로 기록

    for name in completion:  # 완주자 이름을 하나씩 꺼냄
        counts[name] = counts[name] - 1  # 해당 이름의 인원수 1 감소

    for name in counts:  # 기록된 이름을 하나씩 꺼냄
        if counts[name] > 0:  # 남아 있는 인원이 있으면
            return name  # 완주하지 못한 사람의 이름 반환


def solution(participant, completion):  # 참가자와 완주자 목록을 받음
    participant.sort()  # 참가자 이름순 정렬
    completion.sort()  # 완주자 이름순 정렬

    for i in range(len(completion)):  # 완주자 수만큼 위치를 확인
        if participant[i] != completion[i]:  # 같은 위치의 이름이 다르면
            return participant[i]  # 참가자 쪽 이름을 반환

    return participant[-1]  # 전부 같았다면 마지막 참가자가 미완주자        
        
        


# ========== 공부용 코드 (전체 주석 처리) ==========

# from collections import Counter                  # collections 모듈에서 원소별 개수를 세는 Counter 클래스를 가져옴
#
# def solution(participant, completion):           # 참가자 목록과 완주자 목록을 입력받는 함수
#     p_counter = Counter(participant)             # 참가자들의 이름별 등장 횟수를 계산
#     c_counter = Counter(completion)              # 완주자들의 이름별 등장 횟수를 계산
#
#     result = p_counter - c_counter               # 참가자 수에서 완주자 수를 빼서 완주하지 못한 선수만 남김
#     answer = list(result.keys())[0]              # 남은 선수의 이름을 리스트로 변환하고 첫 번째 값을 가져옴
#
#     return answer                                # 완주하지 못한 선수의 이름을 문자열로 반환
