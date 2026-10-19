def solution(targets):
    targets.sort(key=lambda target: target[1])
    answer = 0
    end = -1
    for start, stop in targets:
        if start >= end:
            answer += 1
            end = stop
    return answer

# 전체 코드 줄별 설명
# def solution(targets):  # def는 함수 정의. () 안 targets는 개구간 목록 입력.
#     targets.sort(key=lambda target: target[1])  # sort는 제자리 정렬. key는 정렬 기준, lambda는 짧은 함수, [1]은 구간 끝.
#     answer = 0  # =로 필요한 요격 수를 0으로 초기화.
#     end = -1  # 마지막 요격 위치의 오른쪽 경계. 모든 시작값보다 작은 -1로 초기화.
#     for start, stop in targets:  # for~in으로 구간을 순회. 두 값을 시작·끝 변수로 언패킹.
#         if start >= end:  # if는 조건 분기, >=는 이상. 개구간이므로 경계가 같아도 새 요격 필요.
#             answer += 1  # +=는 더해 저장. 요격 횟수 증가.
#             end = stop  # 현재 구간 끝 바로 왼쪽에 요격한다고 보고 경계 갱신.
#     return answer  # return으로 최소 요격 횟수 반환.

# 풀이 요약
# 끝이 빠른 구간부터 끝 바로 왼쪽에서 요격합니다. 다음 구간이 그 위치를 포함하지 않을 때만 새로 발사합니다.
# 예: 예제 구간을 끝 순으로 처리하면 3회. 끝점은 포함하지 않아 start >= end일 때 추가합니다. 시간 O(N log N), 정렬 공간 O(N).
