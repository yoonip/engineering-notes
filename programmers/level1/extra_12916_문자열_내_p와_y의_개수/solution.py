def solution(s):
    s = s.lower()
    return s.count("p") == s.count("y")

def solution(s):
    s = s.lower()
    p_count = s.count("p")
    y_count = s.count("y")
    if p_count == y_count:
        return True
    else:
        return False

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 문자열 s를 입력받는 함수를 정의합니다.
#     s = s.lower()  # lower는 소문자 변환. =는 값 저장. lower()로 모두 소문자로 바꿔 대소문자 구분을 없앱니다.
#     return s.count("p") == s.count("y")  # return은 결과를 돌려주고 함수 종료. count는 등장 횟수. ==는 같음 비교. count()로 개수를 세고, 같으면 True, 다르면 False를 반환합니다.
# 
# def solution(s):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 문자열 s를 입력받는 함수를 정의합니다.
#     s = s.lower()  # lower는 소문자 변환. =는 값 저장. lower()로 모두 소문자로 바꿔 대소문자 구분을 없앱니다.
#     p_count = s.count("p")  # count는 등장 횟수. =는 값 저장. 소문자 p의 등장 횟수.
#     y_count = s.count("y")  # count는 등장 횟수. =는 값 저장. 소문자 y의 등장 횟수.
#     if p_count == y_count:  # if는 조건이 참일 때 실행. ==는 같음 비교. 두 등장 횟수가 같은지 비교.
#         return True  # return은 결과를 돌려주고 함수 종료. True·False는 참·거짓. 같으면 참을 반환.
#     else:  # else는 앞 조건들에 해당하지 않는 경우. 두 횟수가 다른 경우.
#         return False  # return은 결과를 돌려주고 함수 종료. True·False는 참·거짓. 거짓 반환.

# 풀이 요약
# 소문자로 통일한 뒤 p와 y의 등장 횟수를 비교한다. 대문자 P와 소문자 p를 같은 문자로 세게 된다. 두 문자가 모두 없으면 0=0이므로 True다.
# 문자 수 N: 시간 O(N), 소문자 문자열 공간 O(N).
