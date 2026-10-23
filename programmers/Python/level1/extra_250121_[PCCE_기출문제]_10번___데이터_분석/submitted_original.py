
def solution(data, ext, val_ext, sort_by):
    columns = {
        "code": 0,
        "date": 1,
        "maximum": 2,
        "remain": 3
    }

    answer = []

    for row in data:
        if row[columns[ext]] < val_ext:
            answer.append(row)

    answer.sort(key=lambda x: x[columns[sort_by]])

    return answer
