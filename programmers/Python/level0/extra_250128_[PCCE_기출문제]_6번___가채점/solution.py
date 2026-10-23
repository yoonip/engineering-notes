def solution(numbers, our_score, score_list):
    answer = []
    for i in range(len(numbers)):
        if our_score[i] == score_list[numbers[i] - 1]:
            answer.append("Same")
        else:
            answer.append("Different")
    return answer

# 전체 코드 줄별 설명
# def solution(numbers, our_score, score_list):  # def는 함수 정의. 문의 학생 번호·가채점 점수·전체 실제 점수를 입력받음.
#     answer = []  # []는 빈 리스트. 비교 결과를 차례로 저장.
#     for i in range(len(numbers)):  # len은 길이, range는 0부터 길이-1까지 정수 생성.
#         if our_score[i] == score_list[numbers[i] - 1]:  # ==는 값 비교, []는 인덱스 조회. 학생 번호에 1을 빼 실제 성적 위치로 바꿈.
#             answer.append("Same")  # append는 끝에 추가. 두 점수가 같다는 문자열 저장.
#         else:  # 앞 조건이 거짓인 경우.
#             answer.append("Different")  # 점수가 다르다는 문자열 추가.
#     return answer  # return으로 문의 순서의 비교 결과 반환.

# 풀이 요약
# 문의 순서 i와 학생 번호 numbers[i]를 구분합니다. 실제 점수의 인덱스는 학생 번호-1입니다.
# 