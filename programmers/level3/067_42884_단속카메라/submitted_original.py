def solution(routes):
    camera = float('-inf')
    answer = 0
    for start, end in sorted(routes, key=lambda route: route[1]):
        if start > camera:
            camera = end
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(routes):  # def는 함수 정의. 차량별 [진입 지점,진출 지점] 목록을 받음.
#     camera = float('-inf')  # float('-inf')는 음의 무한대. 아직 카메라가 없음을 모든 진입 지점보다 작은 값으로 표시.
#     answer = 0  # 설치한 카메라 수.
#     for start, end in sorted(routes, key=lambda route: route[1]):  # sorted는 정렬, key는 비교 기준, lambda는 짧은 익명 함수. 진출 지점이 빠른 차량부터 언패킹해 처리.
#         if start > camera:  # 현재 차량의 진입 지점이 마지막 카메라보다 뒤면 해당 카메라를 만나지 못함.
#             camera = end  # 가장 먼저 끝나는 미단속 구간의 끝에 설치해 뒤 차량도 최대한 함께 단속.
#             answer += 1  # +=는 더해 저장. 카메라 한 대 추가.
#     return answer  # 모든 차량을 단속하는 최소 카메라 수 반환.

# 풀이 요약
# 진출 지점 순으로 정렬하고 아직 카메라를 만나지 않은 차량의 진출 지점에 새 카메라를 둔다. 가능한 가장 뒤쪽에 두는 그리디 방식이다.
# 예: -15에 첫 카메라를 놓아 첫째·셋째 차량을, -5에 둘째 카메라를 놓아 둘째·넷째 차량을 단속한다. 끝점도 포함하므로 >로 비교한다.
# 차량 수 N일 때 시간 O(N log N), 정렬 결과를 포함한 공간 O(N).
# 