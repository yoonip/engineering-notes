def solution(s):
    s = s.lower()
    return s.count("p") == s.count("y")



def solution(s):  # 문자열 s를 받음
    s = s.lower()  # 전부 소문자로 바꿔 저장

    p_count = s.count("p")  # p의 개수를 저장
    y_count = s.count("y")  # y의 개수를 저장

    if p_count == y_count:  # 두 개수가 같으면
        return True  # 참을 반환하고 종료
    else:  # 두 개수가 다르면
        return False  # 거짓을 반환하고 종료


# def solution(s):                          # 문자열 s를 입력받는 함수를 정의합니다.
#     s = s.lower()                        # lower()로 모두 소문자로 바꿔 대소문자 구분을 없앱니다.
#     return s.count("p") == s.count("y")  # count()로 개수를 세고, 같으면 True, 다르면 False를 반환합니다.