def solution(n):
    columns, descending, ascending = set(), set(), set()
    def place(row):
        if row == n:
            return 1
        count = 0
        for col in range(n):
            if col in columns or row - col in descending or row + col in ascending:
                continue
            columns.add(col)
            descending.add(row - col)
            ascending.add(row + col)
            count += place(row + 1)
            columns.remove(col)
            descending.remove(row - col)
            ascending.remove(row + col)
        return count
    return place(0)
