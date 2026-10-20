# 칩 산술·시험 자료의 오류 재현 / Offline chip arithmetic and test-data replay

Python 표준 라이브러리만 사용하는 실행 예제입니다. 기존 [practical-silicon-lab](../../../프로젝트_projects/practical-silicon-lab/README.md)의 `npu.py`, `correlation.py`, `training_ber.py`를 수정 없이 가져옵니다. 실제 칩·ATE·DDR PHY·RTL·계측기는 실행하지 않습니다.

## 실행

저장소 루트에서 다음 명령을 실행합니다. `--out`에는 새 폴더가 필요합니다. 기존 경로는 종료 코드 2로 거부하여 결과를 덮어쓰지 않습니다. 외부 패키지는 필요하지 않으며 Python 3.12.14에서 실행했습니다.

```shell
python -B 예제_examples/실무검증_practical-validation/chip/run_chip_cases.py --out /new/path/chip-run
```

전체 예상이 맞으면 종료 코드 0과 `status=PASS`, 예상 밖 차이가 있으면 코드 1과 `FAIL`을 반환합니다. 정상 DUT는 PASS, 의도된 layout·stale·overflow DUT는 FAIL이어야 실행기 확인을 통과합니다. 따라서 실행기 PASS와 DUT PASS를 구별합니다.

## 코드와 결과 읽기

| 함수·파일 | 비교하는 내용 | 결과 |
|---|---|---|
| `arithmetic()` | 손계산 기대값·이차원 기준·평탄 버퍼 DUT, int8 축소 계약 | `arithmetic/input.json`, `report.json` |
| `correlation()` | serial 연결과 잘못된 행 연결, ID·조건·정답 유효성 | `correlation/`의 CSV와 보고서 |
| `training()` | 분리된 통과 구간의 전체 중앙값과 연속 구간 중앙값 | `training/input.json`, `report.json` |
| `Checks` | 고정 기대값과의 비교, 예상된 `ValueError` 거부 | `summary.json`의 `checks` |
| `main()` | 환경·입력·기존 소스 hash, 미실행 범위 | `summary.json` |

확인 개수 44는 이 실행기의 비교·거부 항목 수입니다. 실리콘 고장 coverage, 생산품 수, 통계적 신뢰구간의 표본 수가 아닙니다. 모형이 다루지 않는 크기·채널·양자화·실제 메모리 일관성은 추가 검증이 필요합니다.

- [레이아웃·누산 폭 사례](../../../설계와검증사례_engineering-cases/칩산술의레이아웃과누산폭_chip-arithmetic-contract.md)
- [시험 ID·수율·오판율 사례](../../../설계와검증사례_engineering-cases/시험데이터의식별자와오판율_test-data-identity-metrics.md)
- [PVT·shmoo의 실습 연결](../../../현장계측과검증_measurement-validation/칩과시스템시험_chip-system-testing/조건별오동작과수율의경계_pvt-shmoo-characterization.md)
- [2026-10-21 실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/칩모델과시험자료검증_20261021.md)

## English summary

This standard-library replay imports three existing educational modules without changing them. It checks arithmetic contracts, identity-safe CSV joins, classification denominators and contiguous passing windows. Inputs and source hashes are retained. All fixtures are synthetic; no physical chip or instrument is used.
