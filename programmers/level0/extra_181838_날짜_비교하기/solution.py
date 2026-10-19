def solution(date1, date2):
    return int(date1 < date2)

# 전체 코드 줄별 설명
# def solution(date1, date2):  # def는 함수 정의. [연,월,일] 형식의 두 리스트 입력.
#     return int(date1 < date2)  # 리스트의 < 비교는 앞 항목부터 차례대로 비교. int로 참·거짓을 1·0으로 변환.

# 풀이 요약
# 연·월·일 순서의 리스트 비교는 날짜의 선후 비교와 같습니다. 같은 날짜는 0입니다.
# 