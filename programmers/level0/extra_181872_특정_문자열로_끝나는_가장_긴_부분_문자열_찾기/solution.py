def solution(myString, pat):
    end = myString.rfind(pat) + len(pat)
    return myString[:end]

# 전체 코드 줄별 설명
# def solution(myString, pat):  # def는 함수 정의. 문자열과 끝부분 패턴 입력.
#     end = myString.rfind(pat) + len(pat)  # rfind는 패턴이 마지막으로 시작하는 인덱스, len은 길이. 패턴이 끝난 다음 위치 계산.
#     return myString[:end]  # [:끝]은 처음부터 끝 직전까지의 슬라이싱.

# 풀이 요약
# 가장 뒤에 등장한 pat까지 처음부터 가져오면 가능한 가장 긴 부분 문자열입니다.
# 