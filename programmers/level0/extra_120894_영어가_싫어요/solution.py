def solution(numbers):
    words = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
    for value, word in enumerate(words):
        numbers = numbers.replace(word, str(value))
    return int(numbers)

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. 숫자 영어 이름을 연결한 문자열 입력.
#     words = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')  # ()는 튜플. 숫자 0~9의 영어 이름을 순서대로 저장.
#     for value, word in enumerate(words):  # enumerate는 0부터의 번호와 단어를 함께 제공.
#         numbers = numbers.replace(word, str(value))  # str은 숫자 문자열 변환, replace는 영어 이름을 해당 숫자로 모두 치환.
#     return int(numbers)  # int로 완성된 숫자 문자열을 정수로 변환.

# 풀이 요약
# 영어 이름을 대응하는 숫자 문자로 치환한 뒤 정수로 변환합니다.
# 