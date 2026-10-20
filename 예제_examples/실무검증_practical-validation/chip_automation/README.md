# 칩 시험 작업의 결과 검증 / Validating offline chip-job reports

실제 자식 프로세스 16개를 실행하여 종료 코드·출력 문자열·결과 계약의 차이를 확인합니다. 합성 정수 산술 작업이며 물리 칩·ATE·RTL 시뮬레이터·계측기는 사용하지 않습니다. Python 표준 라이브러리만 필요합니다.

## 실행

저장소 루트에서 다음 명령을 실행합니다. `--out` 경로는 새 폴더여야 하며 기존 경로는 종료 2로 거부합니다. CPython 3.12.14·Windows AMD64에서 실행했습니다.

```shell
python -B 예제_examples/실무검증_practical-validation/chip_automation/run_validation_jobs.py --out /new/path/chip-jobs
```

| 파일 | 역할 |
|---|---|
| [fixture_child.py](fixture_child.py) | 산술 작업과 의도된 잘못된 보고·종료·timeout을 실제 자식에서 만듭니다. |
| [run_validation_jobs.py](run_validation_jobs.py) | 고정 손계산 기대값, run ID·입력 hash·항목 집합·스키마·수치를 검사합니다. |
| 작업별 `job.json` | 명령, 종료 코드·timeout, 기대/관측 분류, 결과 hash를 남깁니다. |
| 전체 `summary.json` | 환경, 집계의 분모, 소스 hash와 16개 대조 결과를 남깁니다. |

전체 종료 0/PASS는 잘못된 조건도 포함한 대조가 모두 예상대로 분류됐다는 뜻입니다. 정상 job은 `ACCEPT`, 값이 틀렸다고 정직하게 보고한 job은 `DUT_FAIL`이며, 거짓 PASS·입력 불일치·누락·잘못된 실행은 다른 코드로 거부합니다. 실제 장치 16개를 합격시킨 결과가 아닙니다.

자식이 만든 기대값을 그대로 신뢰하지 않습니다. 부모는 손계산한 세 출력 185, 65,536, 0을 보유하며 자식의 산술 함수를 import하지 않습니다. 시도마다 다른 ID와 작업 폴더를 사용합니다. 해시는 추적 수단이며 출처 인증이나 보안 샌드박스는 아닙니다.

## 자세히 읽기

- [종료 상태·현재 결과·기능 판정의 구분](../../../설계와검증사례_engineering-cases/시험러너의종료상태와결과계약_chip-runner-result-contract.md)
- [2026-10-21 실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/칩시험러너오류재현_20261021.md)
- [기존 칩 산술·시험 자료 예제](../chip/README.md)
- [계측 명령·응답과 결과 기록](../../../현장계측과검증_measurement-validation/계측자동화_instrument-automation/명령응답과시험결과기록_scpi-pyvisa-automation.md)

## English summary

The runner launches sixteen controlled synthetic jobs and validates structured evidence independently of their exit codes and stdout. Every attempt has a new folder, ID and input hash. Expected failures remain visible. No hardware or external simulator is connected.
