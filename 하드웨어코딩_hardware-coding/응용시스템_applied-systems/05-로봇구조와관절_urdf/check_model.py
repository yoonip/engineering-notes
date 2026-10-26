"""독립 URDF 파서와 제한된 평면 모델의 구조·관절·순기구학을 검사합니다."""  # ROS나 물리 시뮬레이터 실행과 구분
import argparse  # 설치 경로와 결과 파일 선택
import hashlib  # 실행한 소스의 바이트 대조
from importlib.metadata import version  # 실제 파서 판본 확인
import json  # 검사 결과 보관
import math  # 미터·라디안 기하와 유한값 검사
from pathlib import Path  # 현재 소스 경로
import sys  # 임시 의존성 경로와 최적화 옵션 확인
ROOT = Path(__file__).resolve().parent  # 예제의 파일 위치
def require(condition, message):  # 잘못된 모델에 사용할 명시적인 오류
    if not condition: raise ValueError(message)  # 실행 옵션과 무관한 입력 검사
def validate(model):  # 이 예제에서 지원하는 고정 바닥·평면 관절 모델의 계약
    names = [link.name for link in model.links]  # 원래 링크 목록의 이름
    require(len(names) == len(set(names)), 'duplicate link')  # 사전으로 바꾸기 전에 중복 확인
    joints = [joint.name for joint in model.joints]  # 관절 이름 목록
    require(len(joints) == len(set(joints)), 'duplicate joint')  # 덮어써지는 관절 금지
    children = set()  # 한 링크의 부모가 둘이 되지 않게 기록
    adjacency = {name: [] for name in names}  # 트리 연결을 직접 확인할 표
    for joint in model.joints:  # 각 부모·자식과 관절 속성 검사
        require(joint.parent in adjacency and joint.child in adjacency, 'unknown link')  # 존재하는 링크끼리만 연결
        require(joint.child not in children, 'multiple parents')  # 트리의 단일 부모 조건
        children.add(joint.child)  # 이번 자식의 부모가 정해졌음을 기록
        adjacency[joint.parent].append(joint.child)  # 루트에서 방문할 연결
        require(joint.origin is not None, 'explicit origin required by this example')  # 이 검사기가 다루는 명시적 원점 계약
        origin = list(joint.origin.xyz) + list(joint.origin.rpy)  # 링크 사이의 이동과 회전
        require(all(math.isfinite(x) for x in origin), 'nonfinite origin')  # NaN을 정상 위치로 쓰지 않기
        require(joint.origin.rpy == [0, 0, 0] and joint.origin.xyz[2] == 0, 'nonplanar origin')  # 이 계산기의 지원 범위 명시
        require(joint.type in ('fixed', 'revolute'), 'unsupported joint')  # 일반 URDF의 모든 관절을 구현한 것으로 보이지 않게 제한
        if joint.type == 'revolute':  # 회전 관절의 추가 조건
            require(joint.axis == [0, 0, 1], 'axis must be unit positive z')  # 단위 z축만 지원
            limits = joint.limit  # 파일에 적은 범위와 제한
            require(limits is not None, 'missing limits')  # 회전 관절의 범위 필수
            values = [limits.lower, limits.upper, limits.effort, limits.velocity]  # 실제 파싱한 네 값
            require(all(math.isfinite(x) for x in values), 'nonfinite limit')  # 비유한 제한값 거절
            require(limits.lower <= limits.upper and limits.effort > 0 and limits.velocity > 0, 'invalid limits')  # 범위 순서와 양수 조건
    roots = set(names) - children  # 부모가 없는 링크가 루트 후보
    require(len(roots) == 1, 'one root required')  # 서로 끊긴 루트 금지
    seen = set()  # 방문한 링크를 기록
    def visit(name):  # 루트부터 트리 전체 확인
        require(name not in seen, 'cycle')  # 같은 링크로 돌아가는 연결 거절
        seen.add(name)  # 현재 링크 방문 처리
        for child in adjacency[name]: visit(child)  # 자식도 이어서 방문
    visit(next(iter(roots)))  # 유일한 루트에서 시작
    require(seen == set(names), 'disconnected model')  # 끊긴 순환 연결도 거절
    for link in model.links:  # 질량을 가진 링크의 제한된 관성 모델 확인
        if link.inertial is None: continue  # 고정 기준과 표시 프레임은 질량 모델 생략
        inertial = link.inertial  # 해당 링크의 질량 중심·관성
        inertia = inertial.inertia  # 실제 파서가 읽은 텐서 성분
        diagonal = [inertia.ixx, inertia.iyy, inertia.izz]  # 이 예제의 주축 관성
        require(math.isfinite(inertial.mass) and inertial.mass > 0, 'invalid mass')  # 양수 질량 계약
        require(all(math.isfinite(x) and x > 0 for x in diagonal), 'invalid inertia')  # 비유한 값과 음수 관성 거절
        require([inertia.ixy, inertia.ixz, inertia.iyz] == [0, 0, 0], 'only diagonal inertia supported')  # 일반 비대각 관성 검사는 구현하지 않기
        require(all(diagonal[i] <= sum(diagonal) - diagonal[i] + 1e-12 for i in range(3)), 'inertia triangle')  # 주관성의 삼각 부등식
def multiply(a, b):  # 4×4 동차변환의 직접 행렬곱
    return [[sum(a[row][k] * b[k][column] for k in range(4)) for column in range(4)] for row in range(4)]  # 이동·회전 합성
def transform(x, y, yaw):  # 미터 이동과 라디안 z회전을 행렬로 표현
    c, s = math.cos(yaw), math.sin(yaw)  # 반복해서 쓸 회전 성분
    return [[c, -s, 0, x], [s, c, 0, y], [0, 0, 1, 0], [0, 0, 0, 1]]  # 열벡터 점을 옮기는 변환
def forward(model, angles):  # 파일의 관절 체인을 따라 말단 변환 계산
    matrix = transform(0, 0, 0)  # 기준 링크에서 시작
    for name in model.get_chain('base_link', 'tool0', joints=True, links=False, fixed=True):  # 파서가 찾은 관절 순서 사용
        joint = model.joint_map[name]  # 현재 관절의 파일 속성
        yaw = 0.0 if joint.type == 'fixed' else angles[name]  # 고정 관절은 추가 회전 없음
        require(math.isfinite(yaw), 'nonfinite angle')  # NaN 관절값을 전달하지 않기
        if joint.type == 'revolute': require(joint.limit.lower <= yaw <= joint.limit.upper, 'angle outside limits')  # 파일의 라디안 범위 확인
        matrix = multiply(matrix, transform(joint.origin.xyz[0], joint.origin.xyz[1], 0))  # 먼저 부모 안의 관절 원점으로 이동
        matrix = multiply(matrix, transform(0, 0, yaw))  # 그 원점에서 관절 회전 적용
    return matrix  # 마지막 고정 tool_mount까지 합친 결과
def main():  # 실제 파서와 독립 기하식의 검사
    parser = argparse.ArgumentParser(description=__doc__)  # 실행 범위 안내
    parser.add_argument('--dependencies', type=Path)  # 임시 pip 설치 경로 선택
    parser.add_argument('--report', type=Path, required=True)  # 이번 결과 저장 위치
    args = parser.parse_args()  # 인자 읽기
    if sys.flags.optimize: parser.error('run without -O')  # 기대값 검사가 제거되지 않게 확인
    if args.dependencies: sys.path.insert(0, str(args.dependencies.resolve()))  # 전역 설치를 바꾸지 않고 파서 로드
    from urdf_parser_py.urdf import URDF  # 실제 외부 URDF 파서
    source = (ROOT / 'bench_arm.urdf').read_text(encoding='utf-8')  # 작성한 모델 읽기
    model = URDF.from_xml_string(source)  # 태그를 실제 URDF 객체로 파싱
    validate(model)  # 지원 모델의 구조·관절·관성 계약 확인
    require(model.get_root() == 'base_link', 'unexpected root')  # 기준 프레임의 실제 이름 확인
    cases, checks = 0, 0  # 수치 비교 집계
    trace = []  # 대표 자세의 입력·말단 위치 기록
    for shoulder in [-math.pi / 2, -math.pi / 4, 0, math.pi / 4, math.pi / 2]:  # 첫 관절의 경계와 중간값
        for elbow in [-math.pi / 2, -math.pi / 4, 0, math.pi / 4, math.pi / 2]:  # 두 번째 관절의 경계와 중간값
            matrix = forward(model, dict(shoulder=shoulder, elbow=elbow))  # URDF 체인을 실제로 합성
            expected = [0.4 * math.cos(shoulder) + 0.3 * math.cos(shoulder + elbow), 0.4 * math.sin(shoulder) + 0.3 * math.sin(shoulder + elbow), 0]  # 두 막대의 독립 삼각함수식
            for axis in range(3):  # 말단 x·y·z 대조
                assert math.isclose(matrix[axis][3], expected[axis], rel_tol=0, abs_tol=1e-12)  # 미터 단위의 절대 오차만 사용
                checks += 1  # 위치 비교 집계
            for a in range(3):  # 회전 행렬 열벡터의 서로 다른 조합
                for b in range(3):  # 회전은 직교 기저를 보존해야 함
                    assert math.isclose(sum(matrix[k][a] * matrix[k][b] for k in range(3)), float(a == b), rel_tol=0, abs_tol=1e-12)  # 내적과 단위 길이의 절대 오차 확인
                    checks += 1  # 회전 성질 비교 집계
            assert matrix[3] == [0, 0, 0, 1]  # 동차변환의 마지막 행
            checks += 1  # 마지막 행 비교 집계
            cases += 1  # 검사한 관절 조합
            if shoulder == 0 or elbow == 0: trace.append(dict(shoulder_rad=shoulder, elbow_rad=elbow, tip_m=expected))  # 읽기 쉬운 대표 흐름
    mutations = [('mass value="1.0"', 'mass value="-1.0"'), ('axis xyz="0 0 1"', 'axis xyz="0 0 2"'), ('child link="forearm"', 'child link="missing"'), ('lower="-1.5707963267948966"', 'lower="2.0"'), ('ixx="0.00016"', 'ixx="NaN"')]  # 원본을 고치지 않는 다섯 잘못된 모델
    for before, after in mutations:  # 값·축·연결·범위 오류 확인
        try: validate(URDF.from_xml_string(source.replace(before, after, 1)))  # 메모리 안의 복사본만 변경
        except (ValueError, AssertionError): pass  # 지정한 모델 오류가 거절되면 정상
        else: raise AssertionError('invalid model accepted: ' + before)  # 잘못된 모델의 통과를 숨기지 않기
    for shoulder in [math.pi, math.nan]:  # 범위 밖 값과 비유한 관절 입력
        try: forward(model, dict(shoulder=shoulder, elbow=0))  # 유효한 모델에 잘못된 상태 전달
        except ValueError: pass  # 상태 오류의 명시적 거절
        else: raise AssertionError('invalid angle accepted')  # 상태 검사가 생략되면 실패
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in ('bench_arm.urdf', 'check_model.py')}  # 검사한 파일의 바이트 해시
    report = dict(status='passed_urdf_parse_and_planar_checks', parser_version=version('urdf-parser-py'), source_sha256=hashes, links=len(model.links), joints=len(model.joints), pose_cases=cases, numerical_comparisons=checks, rejected_models=len(mutations), rejected_states=2, trace=trace, scope=dict(urdf_parser=True, limited_planar_validator=True, ros2_runtime=False, gazebo=False, dynamics=False, hardware=False))  # 실제 확인 범위 보관
    args.report.parent.mkdir(parents=True, exist_ok=True)  # 결과 파일 부모 준비
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')  # 재현 결과 저장
    print(f'PASS urdf poses={cases} comparisons={checks} rejected_models=5 rejected_states=2')  # 실제 집계 출력
if __name__ == '__main__': main()  # 직접 실행할 때만 외부 파서 호출
