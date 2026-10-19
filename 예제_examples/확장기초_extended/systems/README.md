# 시스템 기초의 실행 모형

## 한국어

Linux 권한·파이프 상태, 의존성 DAG와 입력 digest, 셀 실행 상태, 2×2 선형계, Dijkstra, 장치 probe, debugger 상태, 차동구동 odometry, 파일 게시, bounded 레코드와 최신 UI 요청을 표준 라이브러리로 다룹니다.

저장소 루트에서 실행합니다.

```bash
python -m unittest discover -s 예제_examples/확장기초_extended/systems -p 'test_*.py' -v
```

테스트는 Fraction 기준해, Bellman–Ford, 알려진 바이트열과 이동 궤적, 실패 주입과 완료 순서 전수를 사용합니다. 실제 Linux 권한 판정, Git 객체 형식, Jupyter kernel, MATLAB, 보드 부팅·디버거, 로봇이나 모바일 앱을 에뮬레이션하지 않습니다. 각 함수의 입력 범위와 문서의 가정을 함께 읽습니다. 게시 예제는 임시 디렉터리의 단일 파일에서 검증하며, crash durability·동시 게시·원격 서비스의 exactly-once 보장을 포함하지 않습니다.

[구현](extended_models.py) · [테스트](test_extended_models.py) · [실행 기록](VALIDATION.json)

## English

These standard-library models cover mode bits/pipeline status, dependency DAGs and digests, cell state, 2×2 solves, Dijkstra, device probing, debugger state, differential-drive odometry, file publication, bounded records, and latest UI requests.

Run the command from the repository root. Tests use Fraction and Bellman–Ford oracles, known bytes and trajectories, fault injection, and exhaustive completion permutations. They do not emulate an operating system, Git objects, a Jupyter kernel, MATLAB, boards, a physical robot, or a mobile app. Follow each function's domain and article assumptions. Publication tests concern a single temporary-directory file, excluding crash durability, concurrent writers, and remote exactly-once semantics.

[Implementation](extended_models.py) · [Tests](test_extended_models.py) · [Execution record](VALIDATION.json)
