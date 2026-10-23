def solution(numbers, target):
    def visit(index, total):
        if index == len(numbers):
            return int(total == target)
        value = numbers[index]
        return visit(index + 1, total + value) + visit(index + 1, total - value)
    return visit(0, 0)
