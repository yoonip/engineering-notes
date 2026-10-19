from collections import Counter

def solution(str1, str2):
    def pairs(text):
        # 대소문자 구분 제거.
        text = text.lower()
        return Counter(text[i:i + 2] for i in range(len(text) - 1) if 'a' <= text[i] <= 'z' and 'a' <= text[i + 1] <= 'z')
    first, second = pairs(str1), pairs(str2)
    # values는 개수, sum은 합계.
    intersection = sum((first & second).values())
    union = sum((first | second).values())
    return 65536 if union == 0 else intersection * 65536 // union
