def solution(str1, str2):
    def chunks(text):
        text = text.lower()
        return sorted(text[i:i + 2] for i in range(len(text) - 1)
                      if all('a' <= ch <= 'z' for ch in text[i:i + 2]))
    a, b = chunks(str1), chunks(str2)
    i = j = overlap = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            overlap += 1
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    union = len(a) + len(b) - overlap
    return 65536 if union == 0 else overlap * 65536 // union
