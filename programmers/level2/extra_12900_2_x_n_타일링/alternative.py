def solution(n):
    modulus = 1000000007
    def multiply(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(2)) % modulus for j in range(2)] for i in range(2)]
    result, matrix = [[1, 0], [0, 1]], [[1, 1], [1, 0]]
    while n:
        if n & 1:
            result = multiply(result, matrix)
        matrix = multiply(matrix, matrix)
        n //= 2
    return result[0][0]
