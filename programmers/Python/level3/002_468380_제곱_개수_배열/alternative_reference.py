def solution(arr, l, r):
    expanded = [value for value in arr for _ in range(value)]
    length = r - l + 1
    target = sum(expanded[l - 1:r])
    current = sum(expanded[:length])
    count = int(current == target)
    for end in range(length, len(expanded)):
        current += expanded[end] - expanded[end - length]
        count += current == target
    return [target, count]
