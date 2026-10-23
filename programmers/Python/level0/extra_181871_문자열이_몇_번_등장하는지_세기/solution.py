def solution(myString, pat):
    return sum(myString.startswith(pat, i) for i in range(len(myString)))

# 전체 코드 줄별 설명
# def solution(myString, pat):  # def는 함수 정의. 원본 문자열과 찾을 패턴 입력.
#     return sum(myString.startswith(pat, i) for i in range(len(myString)))  # range·len으로 모든 시작 위치 순회. startswith(패턴,위치)는 해당 위치의 패턴 검사. sum은 참을 1로 합산.

# 풀이 요약
# 모든 시작 위치를 검사하므로 패턴이 서로 겹쳐 등장하는 경우도 모두 셉니다.
# 