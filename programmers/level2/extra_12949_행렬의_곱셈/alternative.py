def solution(arr1, arr2):
    result = [[0] * len(arr2[0]) for _ in arr1]
    for i, row in enumerate(arr1):
        for k, value in enumerate(row):
            for j, other in enumerate(arr2[k]):
                result[i][j] += value * other
    return result
