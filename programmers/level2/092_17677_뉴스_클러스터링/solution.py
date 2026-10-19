from collections import Counter

def solution(str1, str2):
    def pairs(text):
        text = text.lower()
        return Counter(text[i:i + 2] for i in range(len(text) - 1) if 'a' <= text[i] <= 'z' and 'a' <= text[i + 1] <= 'z')
    first, second = pairs(str1), pairs(str2)
    intersection = sum((first & second).values())
    union = sum((first | second).values())
    return 65536 if union == 0 else intersection * 65536 // union

# 전체 코드 줄별 설명
# from collections import Counter  # collections의 Counter를 import. 원소별 중복 횟수를 저장하는 다중집합 자료구조.
# 
# def solution(str1, str2):  # def는 함수 정의. 비교할 두 문자열 입력.
#     def pairs(text):  # 중첩 함수. 영문자 두 글자 조각의 다중집합 생성.
#         text = text.lower()  # lower는 소문자 변환. 대소문자 구분 제거.
#         return Counter(text[i:i + 2] for i in range(len(text) - 1) if 'a' <= text[i] <= 'z' and 'a' <= text[i + 1] <= 'z')  # 슬라이스로 인접 두 글자 추출. len·range·생성식의 if와 and로 두 문자 모두 영문자인 경우만 집계.
#     first, second = pairs(str1), pairs(str2)  # 각 문자열의 다중집합을 만들어 두 변수에 대입.
#     intersection = sum((first & second).values())  # Counter의 &는 원소별 최소 개수 교집합. values는 개수, sum은 합계.
#     union = sum((first | second).values())  # Counter의 |는 원소별 최대 개수 합집합. 합집합 크기 계산.
#     return 65536 if union == 0 else intersection * 65536 // union  # 조건 표현식. 공집합 둘이면 1배율, 아니면 *로 배율 적용 후 //로 내림 나눗셈.

# 풀이 요약
# 인접한 영문자 쌍을 중복 횟수와 함께 세고, 교집합은 최소 횟수·합집합은 최대 횟수로 계산합니다. 둘 다 비면 유사도 1입니다.
# 예: FRANCE와 FRENCH는 교집합 2·합집합 8이라 16384. 두 문자열 길이 합 L에 대해 시간·공간 O(L).
