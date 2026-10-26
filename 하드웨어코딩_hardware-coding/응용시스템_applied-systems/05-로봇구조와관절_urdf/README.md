# URDF 평면 팔의 링크·관절·순기구학 검사

[하드웨어 코딩 목차](../../README.md)

고정된 기준 링크에서 두 관절이 z축으로 도는 교육용 평면 팔을 직접 작성했습니다. 실제 urdf-parser-py로 XML을 읽고, 제한된 구조·관절·관성 조건과 말단 위치를 검사합니다. 0.4m·0.3m 두 링크의 기하를 읽는 선별 실습이며 ROS·Gazebo·동역학·실제 구동기를 실행한 기록은 아닙니다.

## 링크와 관절의 구분

URDF의 link는 좌표계·표시 형상·선택적인 질량 모형을 가진 부분입니다. joint는 부모 링크와 자식 링크 사이의 연결·원점·가능한 운동을 나타냅니다. [공식 urdfdom joint 정의](https://raw.githubusercontent.com/ros/urdfdom_headers/master/include/urdf_model/joint.h)는 부모에서 관절까지의 원점 변환과 자식 링크의 관절 프레임을 구분합니다.

| 이름 | 이 모델의 역할 | 단위와 위치 |
| --- | --- | --- |
| base_link | 외부에서 고정한다고 가정한 기준 | 파일 자체가 바닥 고정 구동기를 구현하지는 않습니다. |
| shoulder → upper_arm | 첫 z축 회전과 첫 링크 | 길이 0.4m, 각도 q₁은 rad입니다. |
| elbow → forearm | 첫 링크 끝의 두 번째 z축 회전 | 부모에서 관절 원점까지 x=0.4m입니다. |
| tool_mount → tool0 | 두 번째 링크 끝의 표시 프레임 | 고정 이동 x=0.3m입니다. |

upper_arm의 visual 원점 0.2m는 상자의 중심을 링크 중간에 놓습니다. 이 값이 관절 프레임이나 링크 길이를 바꾸는 것은 아닙니다. forearm의 visual 원점도 길이의 절반인 0.15m입니다. 형상·링크 프레임·관절 원점의 세 역할을 나누어 읽습니다.

## 순기구학의 계산 순서

이 예제는 모든 관절 원점 rpy가 0이고 회전축이 단위 +z입니다. 부모 좌표에서 관절 원점까지 먼저 이동한 뒤 그 관절의 회전을 적용합니다. 말단 변환은 Rz(q₁)·Tx(0.4)·Rz(q₂)·Tx(0.3)입니다. 마지막 말단 점에 적용할 때는 오른쪽부터 읽는 행렬곱입니다.

검사기의 forward는 파서가 찾은 base_link→tool0 관절 체인을 따라 동차행렬을 곱합니다. 독립 기준은 같은 행렬 코드를 복사하지 않고 다음 두 막대의 기하식을 사용합니다.

x=0.4cos(q₁)+0.3cos(q₁+q₂), y=0.4sin(q₁)+0.3sin(q₁+q₂), z=0입니다.

| 직접 구성한 입력 | 먼저 회전하는 링크 | 기대 말단 위치 |
| --- | --- | --- |
| q₁=0,q₂=0 | 두 링크가 +x로 이어집니다. | (0.7,0,0)m입니다. |
| q₁=0,q₂=π/2 | 첫 링크는 +x, 둘째 링크는 +y입니다. | (0.4,0.3,0)m입니다. |
| q₁=π/2,q₂=0 | 두 링크가 +y로 이어집니다. | (0,0.7,0)m입니다. |
| q₁=π/4,q₂=0 | 두 링크가 45°로 이어집니다. | 약 (0.494975,0.494975,0)m입니다. |

각도와 이동을 바꾸어 적용하면 결과가 달라집니다. 이 네 행은 기하를 따라가는 예이며 실제로는 두 관절 각각 −π/2·−π/4·0·π/4·π/2의 25조합을 검사했습니다.

## 제한된 모델 검사와 관성

validate는 링크·관절 이름 중복, 존재하지 않는 링크, 복수 부모, 단일 루트·연결·순환을 확인합니다. 이 계산기에 맞춰 관절 원점의 z와 rpy를 0으로 제한하고, fixed·revolute와 정확한 단위 +z 회전축만 허용합니다. 일반 URDF의 다른 축·prismatic·floating 관절이나 임의 3차원 모델을 검증하는 도구는 아닙니다.

회전 관절의 lower≤upper, 양수 effort·velocity와 유한값을 확인하고 입력 관절각도 파일의 범위 안인지 검사합니다. effort=1.0Nm와 velocity=0.5rad/s는 이 모델의 설명용 속성입니다. 이 값을 적었다고 모터 토크나 속도를 실제 제한한 것은 아닙니다.

질량은 1kg·0.6kg입니다. 두 상자의 질량 중심에서 축에 정렬된 대각 관성만 사용합니다. 예를 들어 첫 상자의 Ixx=m(b²+c²)/12≈0.000266667kg·m²이고 Iyy=Izz≈0.013466667kg·m²입니다. 검사기는 양수·유한 대각값, 0인 비대각값, 주관성의 삼각 부등식을 확인합니다. 실제 질량·관성을 계측하거나 일반 관성 프레임의 물리 타당성을 전부 증명한 범위는 아닙니다.

## 실제 결과와 오류 입력

2026-10-26에 Python 3.12.14와 urdf-parser-py 0.0.4를 사용한 실행이 종료 코드 0으로 끝났고 stderr는 비어 있습니다. 4링크·3관절을 파싱한 뒤 각 자세에서 위치 3개, 회전행렬의 열 내적 9개, 동차행렬 마지막 행 1개를 검사하여 25×13=325개 수치 비교를 수행했습니다. 위치 절대 오차 한도는 10⁻¹²m이며 회전의 직교성도 절대 오차로 대조합니다. 회전행렬의 모든 원소를 별도 정답 자세와 비교한 검사는 아닙니다.

| 메모리 복사본에 넣은 계약 위반 | 확인한 거절 |
| --- | --- |
| 첫 링크 질량 −1kg | 양수 질량 조건에서 거절합니다. |
| 회전축 (0,0,2) | 이 예제의 정확한 단위 +z 축 조건에서 거절합니다. |
| 존재하지 않는 자식 링크 | 연결 조건에서 거절합니다. |
| lower=2rad로 upper보다 큼 | 관절 범위 조건에서 거절합니다. |
| Ixx=NaN | 유한 관성 조건에서 거절합니다. |

모델 5개와 별도로 q₁=π·NaN의 잘못된 관절 상태 2개를 거절했습니다. 모든 URDF 오류나 모든 관절 상태를 전수 검사한 것은 아닙니다. 잘못된 모델은 원본 파일을 고치지 않고 메모리 문자열에서만 만들었습니다.

```text
PASS urdf poses=25 comparisons=325 rejected_models=5 rejected_states=2
```

실제 입력 자세·결과·파서 판본·소스 SHA와 기록은 [example.json](example.json)에 있습니다. 저장된 실행 결과와 현재 소스의 정적 일치 대조는 파서·기하 계산의 재실행과 구분합니다.

## 재현 명령과 현실 사용 조건

[공식 urdf_parser_py](https://github.com/ros/urdf_parser_py)는 standalone 파서입니다. 임시 --target 경로에 버전을 고정해 설치하고, 저장소 루트에서 다음 명령을 실행합니다. -O는 기대값 assert를 제거하므로 검사기가 거절합니다.

```powershell
$py = 'C:/path/to/python.exe'
$deps = Join-Path (Get-Location) 'tmp/urdf-example-deps'
& $py -B -m pip install --target $deps 'urdf-parser-py==0.0.4'
& $py -B '하드웨어코딩_hardware-coding/응용시스템_applied-systems/05-로봇구조와관절_urdf/check_model.py' --dependencies $deps --report 'tmp/urdf-model-validation.json'
```

이 모델에는 충돌 검사·접촉·모터·센서·제어기·물리적 바닥 고정을 연결하지 않았습니다. 실제 팔에는 치수·질량·관성·영점·축 방향·관절 제한·충돌 형상과 제어기 계약을 대조해야 합니다. XML을 읽고 수치 기하가 맞았다는 사실만으로 실제 로봇을 안전하게 움직일 수 있다고 판단하지 않습니다.

## 전체 소스와 줄별 메모

### bench_arm.urdf

```xml
<?xml version="1.0" encoding="UTF-8"?> <!-- 파일의 문자 인코딩 -->
<robot name="bench_planar_arm"> <!-- 고정된 바닥 기준의 교육용 두 링크 팔 -->
  <link name="base_link"/> <!-- 위치를 외부에서 고정한다고 가정할 기준 링크 -->
  <link name="upper_arm"> <!-- 길이 0.4m인 첫 링크 -->
    <visual> <!-- 표시용 상자와 링크 좌표의 관계 -->
      <origin xyz="0.2 0 0" rpy="0 0 0"/> <!-- 링크 시작에서 상자 중심까지의 이동 -->
      <geometry><box size="0.4 0.04 0.04"/></geometry> <!-- 미터 단위의 길이·폭·높이 -->
    </visual> <!-- 표시 형상 끝 -->
    <inertial> <!-- 1kg 균일 상자의 질량 중심과 관성 -->
      <origin xyz="0.2 0 0" rpy="0 0 0"/> <!-- 관성은 질량 중심에서 정의 -->
      <mass value="1.0"/> <!-- 킬로그램 단위의 설명용 질량 -->
      <inertia ixx="0.000266666666667" iyy="0.013466666666667" izz="0.013466666666667" ixy="0" ixz="0" iyz="0"/> <!-- 축 정렬 상자의 kg·m² 관성 -->
    </inertial> <!-- 첫 링크의 질량 모형 끝 -->
  </link> <!-- 첫 링크 정의 끝 -->
  <joint name="shoulder" type="revolute"> <!-- z축을 중심으로 도는 첫 관절 -->
    <parent link="base_link"/><child link="upper_arm"/> <!-- 부모에서 자식으로 이어지는 트리 -->
    <origin xyz="0 0 0" rpy="0 0 0"/><axis xyz="0 0 1"/> <!-- 기준점과 단위 회전축 -->
    <limit lower="-1.5707963267948966" upper="1.5707963267948966" effort="1.0" velocity="0.5"/> <!-- 라디안 범위와 설명용 제한값 -->
  </joint> <!-- 첫 관절 정의 끝 -->
  <link name="forearm"> <!-- 길이 0.3m인 두 번째 링크 -->
    <visual> <!-- 표시용 상자의 위치 -->
      <origin xyz="0.15 0 0" rpy="0 0 0"/><geometry><box size="0.3 0.04 0.04"/></geometry> <!-- 링크 시작에서 길이 절반 위치 -->
    </visual> <!-- 표시 형상 끝 -->
    <inertial> <!-- 0.6kg 균일 상자의 질량 모형 -->
      <origin xyz="0.15 0 0" rpy="0 0 0"/><mass value="0.6"/> <!-- 질량 중심과 질량 -->
      <inertia ixx="0.00016" iyy="0.00458" izz="0.00458" ixy="0" ixz="0" iyz="0"/> <!-- 축 정렬 상자의 관성 -->
    </inertial> <!-- 두 번째 링크의 질량 모형 끝 -->
  </link> <!-- 두 번째 링크 정의 끝 -->
  <joint name="elbow" type="revolute"> <!-- 첫 링크 끝에서 도는 두 번째 관절 -->
    <parent link="upper_arm"/><child link="forearm"/> <!-- 첫 링크에서 두 번째 링크로 연결 -->
    <origin xyz="0.4 0 0" rpy="0 0 0"/><axis xyz="0 0 1"/> <!-- 부모 링크 x축 끝에서 관절 시작 -->
    <limit lower="-1.5707963267948966" upper="1.5707963267948966" effort="1.0" velocity="0.5"/> <!-- 이 예제의 관절 범위 -->
  </joint> <!-- 두 번째 관절 정의 끝 -->
  <link name="tool0"/> <!-- 말단 점을 나타내는 질량 없는 표시 프레임 -->
  <joint name="tool_mount" type="fixed"> <!-- 말단 점까지의 고정 연결 -->
    <parent link="forearm"/><child link="tool0"/> <!-- 말단 프레임의 부모 -->
    <origin xyz="0.3 0 0" rpy="0 0 0"/> <!-- 두 번째 링크 끝의 말단 점 -->
  </joint> <!-- 고정 연결 끝 -->
</robot> <!-- 로봇 구조 정의 끝 -->
```

### check_model.py

```python
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
```

## 공식 근거와 직접 작성한 범위

- [공식 urdfdom joint 헤더](https://raw.githubusercontent.com/ros/urdfdom_headers/master/include/urdf_model/joint.h)는 부모·자식·관절 원점·축의 개념을 확인한 근거입니다.
- [공식 Python 파서 저장소](https://github.com/ros/urdf_parser_py)는 사용한 standalone 라이브러리의 출처이며, 현재 저장소와 설치한 0.0.4 판본을 구분합니다. BSD-3-Clause 외부 라이브러리의 소스나 바이너리를 이 폴더에 복제하지 않습니다.
- URDF 모델·기하 계산·검사 입력·설명은 직접 작성했습니다. 공식 예제 코드·그림을 복사하지 않았습니다.

자료 열람과 실제 실행 기준일은 2026-10-26입니다.
