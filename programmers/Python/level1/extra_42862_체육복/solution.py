def solution(n, lost, reserve):
    lost_set = set(lost)
    reserve_set = set(reserve)
    need = lost_set - reserve_set
    extra = reserve_set - lost_set
    for student in sorted(extra):
        if student - 1 in need:
            need.remove(student - 1)
        elif student + 1 in need:
            need.remove(student + 1)
    return n - len(need)

# 전체 코드 줄별 설명
# def solution(n, lost, reserve):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. n: 전체 학생 수, lost: 도난당한 학생, reserve: 여벌이 있는 학생
#     lost_set = set(lost)  # set은 중복 없는 집합. =는 값 저장. 도난당한 학생 번호 목록을 집합으로 변환
#     reserve_set = set(reserve)  # set은 중복 없는 집합. =는 값 저장. 여벌이 있는 학생 번호 목록을 집합으로 변환
#     need = lost_set - reserve_set  # =는 값 저장. 도난당한 학생 중 여벌도 없는 학생 → 빌려야 할 대상
#     extra = reserve_set - lost_set  # =는 값 저장. 여벌이 있는 학생 중 도난당하지 않은 학생 → 빌려줄 수 있는 대상
#     for student in sorted(extra):  # for·in은 원소를 차례로 꺼내는 반복문. sorted는 정렬한 새 리스트. 빌려줄 수 있는 학생을 번호가 작은 순서로 하나씩 확인
#         if student - 1 in need:  # if는 조건이 참일 때 실행. in은 포함 여부. 바로 앞 번호 학생에게 체육복이 없다면
#             need.remove(student - 1)  # remove는 지정한 값의 첫 항목 삭제. 앞 학생에게 빌려주고, 필요한 학생 집합에서 제거
#         elif student + 1 in need:  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. in은 포함 여부. 앞 학생에게 빌려주지 않았고, 바로 뒤 학생에게 체육복이 없다면
#             need.remove(student + 1)  # remove는 지정한 값의 첫 항목 삭제. 뒤 학생에게 빌려주고, 필요한 학생 집합에서 제거
#     return n - len(need)  # return은 결과를 돌려주고 함수 종료. len은 길이. 전체 학생 수에서 끝까지 체육복이 없는 학생 수를 빼서 반환

# 풀이 요약
# 분실자이면서 여벌도 가진 학생은 자기 것을 써야 하므로 두 집합의 공통 원소를 먼저 제외한다. 여벌 학생을 번호순으로 보며 왼쪽 이웃에게 먼저, 없으면 오른쪽 이웃에게 빌려준다. 작은 번호부터 가장 왼쪽의 미해결 수요를 처리해 뒤의 선택을 막지 않는다.
# 분실 L명, 여벌 R명: 평균 시간 O(L+R log R), 공간 O(L+R).
