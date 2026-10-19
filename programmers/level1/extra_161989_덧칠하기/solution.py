def solution(n, m, section):
    answer = 0
    painted_until = 0
    for position in section:
        if position > painted_until:
            answer += 1
            start = min(position, n - m + 1)
            painted_until = start + m - 1
    return answer

# 전체 코드 줄별 설명
# def solution(n, m, section):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. n: 벽 길이, m: 롤러 길이, section: 칠해야 하는 구역 번호 목록
#     answer = 0  # =는 값 저장. 롤러로 칠한 횟수. 아직 칠하지 않았으므로 0
#     painted_until = 0  # =는 값 저장. 마지막으로 칠한 구역 번호. 구역은 1번부터이므로 초기값은 0
#     for position in section:  # for·in은 원소를 차례로 꺼내는 반복문. 오름차순으로 주어진 구역 번호를 왼쪽부터 하나씩 확인
#         if position > painted_until:  # if는 조건이 참일 때 실행. >는 큼 비교. 이전에 칠한 범위보다 오른쪽이면 새로 칠해야 함
#             answer += 1  # +=는 더하거나 연결한 값을 저장. 칠하는 횟수 증가. answer = answer + 1과 같은 의미
#             start = min(position, n - m + 1)  # min은 최솟값. =는 값 저장. 현재 구역에서 시작하되, 벽 끝을 넘으면 왼쪽으로 조정
#             painted_until = start + m - 1  # =는 값 저장. 시작 구역부터 m칸을 칠했을 때의 마지막 구역 번호
#     return answer  # return은 결과를 돌려주고 함수 종료. 필요한 구역을 모두 칠한 최소 횟수를 반환

# 풀이 요약
# 가장 왼쪽의 아직 안 칠한 구역을 포함하면서 오른쪽을 최대한 덮는다. 끝을 넘는 롤러는 벽의 마지막 시작 위치로 옮긴다. 이미 덮은 범위 안의 다음 구역은 건너뛴다. 왼쪽 미처리 구역은 반드시 칠해야 하므로 이때 오른쪽을 넓게 덮는 선택이 불리하지 않다.
# 칠할 구역 수 K: 시간 O(K), 보조 공간 O(1).
