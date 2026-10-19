def solution(data, col, row_begin, row_end):
    data.sort(key=lambda row: (row[col - 1], -row[0]))
    answer = 0
    for index in range(row_begin, row_end + 1):
        value = sum(number % index for number in data[index - 1])
        answer ^= value
    return answer

# 전체 코드 줄별 설명
# def solution(data, col, row_begin, row_end):  # def는 함수 정의. () 안은 표·정렬 열·행 구간 입력.
#     data.sort(key=lambda row: (row[col - 1], -row[0]))  # sort는 제자리 정렬, lambda는 짧은 함수, key는 기준. 튜플 앞값은 오름차순, 음수 기본키는 내림차순 효과.
#     answer = 0  # =는 대입. XOR 누적값은 0으로 시작.
#     for index in range(row_begin, row_end + 1):  # range는 끝 미포함. 마지막 행까지 포함하도록 +1.
#         value = sum(number % index for number in data[index - 1])  # %는 나머지, 생성식 for와 sum으로 해당 행 나머지 합 계산. [] 인덱스는 0부터라 -1.
#         answer ^= value  # ^=는 비트 XOR 후 저장. 대응 비트가 다르면 1, 같으면 0.
#     return answer  # return으로 누적 해시값 반환.

# 풀이 요약
# 지정 열 오름차순·기본키 내림차순으로 정렬하고, 각 행 번호로 나눈 나머지 합을 XOR합니다.
# 예: 정렬 후 S2=0,S3=4이므로 0 XOR 4=4. N행·M열일 때 시간 O(N log N+NM), 정렬 공간 O(N).
