# 합성 데이터 기반 검증 예제

`bench.py`는 0.80 V, 600 MHz의 교육용 설정과 10 ms의 합성 V/I sample을 사용한다. 장비나 전원 rail을 제어하지 않는다. `droop`은 전체 capture 구간을 120 mV 낮춘 모델이며 실제 transient 파형이 아니다. Energy는 동기화된 V/I sample의 사다리꼴 적분으로 계산한다.

| 프로그램 | 확인하는 것 | 범위 |
| --- | --- | --- |
| `bench.py` | 판정·오류 분류·종료 정리·파일 hash | none/droop/mismatch/timeout/malformed 모델 |
| `npu.py` | 독립 scalar reference와 flat-buffer 계산 비교 | 3×3 입력, 2×2 kernel의 cross-correlation |
| `training_ber.py` | 연속 pass tap 구간과 0-error BER 상한 | 물리 DDR PHY나 bit stream은 연결하지 않음 |
| `correlation.py` | 같은 serial의 합성 ATE/SLT 결과 결합 | 1,000개 합성 부품과 별도 synthetic truth |
| `coverage_account.py` | 시도·유효 판정·통과의 분모 | 함께 제공한 고정 예제 CSV |
| `validation_plan.yaml` | 요구·corner·관측·판정의 문서 구조 | 설정을 실제 하드웨어에 적용하는 실행 엔진은 없음 |
| `visa_readonly.py` | 실제 PyVISA transport의 최소 참조 | CLI는 `*IDN?` 식별 query만 수행 |

```sh
python -B check_examples.py
python -B npu.py --fault overflow --out ../results/npu-overflow
python -B correlation.py --out ../results/correlation --with-truth
```

`npu.py`의 `layout`, `stale`, `overflow`는 잘못된 결과를 만들어야 하는 결함 주입이다. 실제 accelerator의 throughput이나 accuracy benchmark가 아니다. Bench와 NPU는 기존 출력 폴더 덮어쓰기를 거부한다. Correlation은 같은 폴더를 재사용할 수 있으며, 기본 실행은 합성 CSV를 다시 만든다. `--analyse-existing`은 기존 CSV를 읽지만 보고서는 여전히 simulation-only로 표시한다.

Correlation 예제의 ATE/SLT matrix는 PASS/PASS=900, PASS/FAIL=60, FAIL/PASS=20, FAIL/FAIL=20이다. 독립 truth가 있을 때 good=940, bad=60, SLT pass=920이다. False accept는 10/60, false reject는 30/940, pass 집단의 불량 비율은 10/920으로 분모가 다르다. 서로 다른 serial·중복 serial·조건 불일치·잘못된 truth는 오류로 처리한다. 분모가 0인 통계는 `null`이다.

BER 상한은 독립이고 같은 오류확률을 갖는 bit trial 모델에서 관측 오류가 0일 때의 단측 상한이다. 실제 burst error나 시험 조건 변화를 이 식 하나로 설명하지 않는다. Tap의 개수와 두 끝 사이의 간격도 구분한다.

VISA 코드를 실물에 사용하려면 별도의 PyVISA/backend와 정확한 resource가 필요하다. 이번 오프라인 테스트는 `pyvisa` module을 mock으로 대체하여 식별 query와 close 경로만 확인한다. 이 transport는 완성된 power/scope bench adapter가 아니다.
