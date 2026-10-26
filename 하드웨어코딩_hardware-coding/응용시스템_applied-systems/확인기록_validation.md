# 응용 시스템 예제의 로컬 실행 기록 | Local execution records for applied systems

[응용 시스템 목차](README.md) · [분야별 구조와 검증](분야별구조와검증_domain-architecture.md) · [공식 자료 안내](공개프로젝트와언어_sources-and-languages.md)

## 2026-10-26 실행

아래 결과는 Windows 호스트에서 직접 작성한 예제를 실행한 기록입니다. 온라인 문제의 채점 결과와 구분합니다. 각 폴더의 `example.json`에 소스 바이트의 SHA-256, 도구 판본, 명령·출력과 비교 결과를 담았습니다. 명령에 남은 절대 경로는 당시 실행 위치이며, 다른 컴퓨터에서는 각 README의 상대 경로 명령과 의존성 판본을 사용합니다.

| 예제와 결과 파일 | 실제로 실행한 것 | 확인한 결과 | 확인 범위 |
| --- | --- | --- | --- |
| [이동 로봇 좌표](01-이동로봇좌표_robot-frames/example.json) | Zig 0.16.0의 C++17 컴파일러로 `-Wall -Wextra -Werror -O2`를 적용해 컴파일하고 실행했습니다. | 9,526개 검사식, 역변환 점 105개, 합성 쌍 441개와 합성 점 2,205개를 통과했습니다. 순서를 뒤집은 대조 실행은 의도한 좌표 검사에서 종료 코드 1로 실패했습니다. | 별도 행렬 계산·손계산·거리 보존과 비교한 평면 좌표 계산입니다. |
| [실내 격자 경로](02-실내격자경로_grid-planning/example.json) | Python 3.12.14로 정적 지도와 원형 몸체의 A*를 실행했습니다. | 계획 사례 4,620개에서 검사식 12,444개를 통과했습니다. 512개 작은 지도에서 BFS 대조 4,608건을 수행했고 잘못된 입력 13건을 거절했습니다. 몸체를 점으로 바꾼 대조 실행은 의도한 기능 검사에서 실패했습니다. | 독립 BFS 거리·경로의 선분 기하와 비교한 4연결 한 셀 이동입니다. |
| [실내 AGV 측정 융합](03-실내로봇측정융합_robot-estimation/example.json) | Python 3.12.14로 단일 축 위치 필터와 별도 검사기를 실행했습니다. | 대수 조합 360개와 정한 시나리오 40단계에서 검사식 2,342개를 통과했습니다. 측정 수락 5건·오래된 값 1건·예정 표본 누락 1건·이상값 1건을 구분했습니다. | 정밀도 가중식·Joseph 분산·게이트 경계·거절 뒤 상태의 대조입니다. |
| [위성 교육 원궤도](04-위성교육궤도_satellite-orbit/example.json) | Python 3.12.14로 두 반지름에서 RK4 적분과 해석해 비교를 실행했습니다. | 6회 원궤도 계산·1,680개 적분 단계·수렴 비교 4쌍에서 검사식 8,435개를 통과했습니다. | 한 주기 표본의 위치·속도·비에너지·비각운동량 오차와 시간 간격 수렴입니다. |
| [2링크 URDF](05-로봇구조와관절_urdf/example.json) | `urdf-parser-py 0.0.4`로 XML을 읽고 별도 Python 검사로 평면 정기구학을 계산했습니다. | 관절각 25조합에서 수치 비교 325개를 통과했습니다. 잘못된 모델 5개와 관절 상태 2개를 거절했습니다. | 한정한 평면 모델의 트리·축·범위·대각 관성과 해석식 비교입니다. |
| [벤치 Protocol Buffers](06-벤치텔레메트리_protobuf/example.json) | `grpcio-tools 1.85.0`의 실제 `protoc`로 Python 코드를 생성하고 `protobuf 7.36.2`로 직렬화·복원했습니다. | 정상 전송값 조합 54개, 검사식 84개, 거절 조건 22개를 확인했습니다. 필드가 있는 0과 필드 누락을 구분했습니다. | 같은 단조 시계의 벤치 데이터 형식·순서·신선도와 잘못된 입력 후 상태입니다. |

집계 단위는 예제마다 다릅니다. 계획 사례 수, 적분 단계 수, 수치 비교 수를 합쳐 하나의 성능 수치나 커버리지로 제시하지 않습니다. 의도한 실패는 정상 결과에 합치지 않고 입력·실패 이유·종료 코드와 함께 보존합니다.

## 실제 완료 출력

```text
PASS robot-frames checks=9526 inverse_points=105 composition_pairs=441 composition_points=2205 max_error_m=2.512e-15
PASS grid-planning checks=12444 planner_cases=4620 exhaustive_maps=512 oracle_cases=4608 found_paths=793 invalid_rejections=13
PASS robot checks=2342 algebra_cases=360 steps=40 accepted=5 stale=1 missing=1 outlier=1
PASS orbit checks=8435 circular_runs=6 integrated_steps=1680 convergence_pairs=4
PASS urdf poses=25 comparisons=325 rejected_models=5 rejected_states=2
PASS protobuf valid=54 checks=84 rejected=22
```

좌표의 `max_error_m`는 별도 기대값과 부동소수점 계산의 최대 차이이며 센서 정확도가 아닙니다. 격자 검사에서 찾은 경로 793건은 지정한 지도·질의에서의 수치입니다. 필터의 RMSE는 직접 정한 고정 시나리오의 비교이고, 위성의 오차는 이상적 원운동의 해석해와 수치 적분 사이의 차이입니다. 실제 차량·로봇·위성의 성능 측정값으로 읽지 않습니다.

## 실행하지 않은 외부 체계

ROS 2·Gazebo·Autoware·CARLA·cFS·F Prime·SPARK·OpenModelica는 공식 문서·저장소·라이선스를 조사해 연결했습니다. 이 작업에서는 해당 런타임의 설치·예제 실행·통합을 수행하지 않았습니다. 실제 프로세서·센서·차량·우주 장치의 구동, HIL, 환경 시험과 안전 인증도 수행하지 않았습니다. URDF 파서와 `protoc`의 실제 실행을 ROS 통합이나 임무용 탑재 소프트웨어의 검증으로 바꾸어 표시하지 않습니다.

## 게시 자료의 정적 대조

현재 게시 소스의 해시, 카탈로그와 실행 기록의 연결, README의 전체 코드, Markdown 로컬 파일 링크는 [check_sources.py](check_sources.py)로 대조합니다. 결과의 `tools_reexecuted: false`는 컴파일러·파서·수치 실험을 다시 호출하지 않았다는 뜻입니다. 원래 실행은 각 `example.json`의 명령과 출력으로 확인합니다.

[게시 소스·문서 대조 결과](source-check.json)에 2026-10-26 대조 시각과 예제별 일치 결과를 보존합니다.

```bash
python -B 하드웨어코딩_hardware-coding/응용시스템_applied-systems/check_sources.py --report /path/to/current-source-check.json
```

코드를 바꾸면 원래 성공 기록과 해시가 달라져 이 대조가 실패합니다. 바뀐 소스를 다시 실행하고 기대값·결과를 검토한 뒤 해당 실행 기록을 갱신해야 합니다. 글의 문체만 수정할 때 기존 결과 수치와 소스는 바꾸지 않습니다.
