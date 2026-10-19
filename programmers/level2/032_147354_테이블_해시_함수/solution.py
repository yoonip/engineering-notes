def solution(data, col, row_begin, row_end):
    # 지정 열은 오름차순, 같으면 첫 열은 내림차순이다.
    data.sort(key=lambda row: (row[col - 1], -row[0]))
    answer = 0
    for index in range(row_begin, row_end + 1):
        # 정렬 후 1부터 시작하는 행 번호로 나머지를 구한다.
        value = sum(number % index for number in data[index - 1])
        answer ^= value
    return answer
