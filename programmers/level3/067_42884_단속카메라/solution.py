# 차량별 [진입 지점,진출 지점] 목록을 받음.
def solution(routes):
    # 아직 카메라가 없음을 모든 진입 지점보다 작은 값으로 표시.
    camera = float('-inf')
    # 설치한 카메라 수.
    answer = 0
    # 진출 지점이 빠른 차량부터 언패킹해 처리.
    for start, end in sorted(routes, key=lambda route: route[1]):
        # 현재 차량의 진입 지점이 마지막 카메라보다 뒤면 해당 카메라를 만나지 못함.
        if start > camera:
            # 가장 먼저 끝나는 미단속 구간의 끝에 설치해 뒤 차량도 최대한 함께 단속.
            camera = end
            # 카메라 한 대 추가.
            answer += 1
    # 모든 차량을 단속하는 최소 카메라 수 반환.
    return answer
