# 작업 진행과 워치독 리셋 기록 / Task progress and watchdog reset records

주기적인 feed가 멈춘 task를 가리는 경로와, 모든 task의 새로운 진행을 확인한 뒤 feed하는 경로를 비교합니다. 8비트 tick 순환, 허용 feed 창, reset 원인 보존과 연속 watchdog 재부팅 정책을 함께 확인하는 표준 라이브러리 Python 모형입니다. 실제 MCU·RTOS·하드웨어 워치독·retention 메모리를 실행하지 않습니다.

| 파일 | 역할 |
| --- | --- |
| [models.py](models.py) | 진행 epoch·freshness, 순환 tick, feed 창, sticky 원인과 부팅 정책을 구현합니다. |
| [fixtures.json](fixtures.json) | 직접 만든 사건과 손으로 정한 literal 기대값을 담습니다. |
| [verify.py](verify.py) | 유한 sweep·경계·오류 주입을 검사하고 새 폴더에 JSON을 기록합니다. |

## 실행

이 폴더에서 Python 3.10 이상으로 아래 명령을 실행합니다. 결과 폴더는 아직 없어야 합니다. `-B`는 bytecode 생성을 막고 `-X utf8`은 텍스트 입출력 인코딩을 고정합니다.

```powershell
python -X utf8 -B verify.py --output C:/temp/watchdog-run-new
python -X utf8 -B -O verify.py --output C:/temp/watchdog-optimized-new
python -X utf8 -B verify.py --inject periodic-feed --output C:/temp/watchdog-periodic-new
python -X utf8 -B verify.py --inject raw-deadline --output C:/temp/watchdog-wrap-new
python -X utf8 -B verify.py --inject clear-before-capture --output C:/temp/watchdog-capture-new
python -X utf8 -B verify.py --inject always-restart --output C:/temp/watchdog-boot-new
```

| 종료 코드 | 의미 |
| --- | --- |
| 0 | 수정 경로와 literal 기대값이 같고 내부 오류 대조가 검출됐습니다. |
| 1 | 계약이 다르거나 입력·실행 중 오류가 발생했습니다. 주입한 네 오류도 이 경로로 거부됩니다. |
| 2 | 기존 결과 폴더나 명령행 인수 때문에 실행을 시작하지 않았습니다. |

`-O`에서도 동작하도록 검사에 `assert`를 사용하지 않습니다. 실제 실행에서 정상은 기본/최적화 모두 0, 네 오류는 기본/최적화 모두 1이었습니다. 기존 출력 경로 재사용은 2였고 JSON 해시가 유지됐습니다.

## 계약과 범위

모형 feed 창은 이전 feed 뒤 `[4, 12)` tick입니다. 모든 task는 이전 feed에서 소비한 sequence보다 새 값이어야 하고, 마지막 checkpoint 나이는 10 tick 이하여야 합니다. sequence는 끝없이 커지는 Python 정수이며 고정 폭 카운터의 순환은 구현하지 않습니다. checkpoint는 실제 작업 완료를 보고하는 사건으로 가정하며 단순 timer 호출로 대체하지 않습니다.

tick은 0~255로 순환하고 비교하는 실제 시간 차이는 128 미만이라고 전제합니다. 이미 한 바퀴 이상 지난 시간의 모호함을 작은 tick 두 개만으로 복원할 수는 없습니다. `monitor`는 poll 사건에서 창을 평가합니다. 입력의 deadline=266에 poll이 있어 reset을 266으로 보고하며, poll 사이 비동기 하드웨어 리셋 타이머를 실행한 결과가 아닙니다.

리셋 원인 1·2·4는 모형 비트입니다. 실제 RCC 비트 위치가 아닙니다. 원인 snapshot을 먼저 남긴 다음 소거하고, 여러 원인을 모두 보존합니다. 부팅 ledger는 값이 부팅 간 보존된다는 가정 아래 세 번째 연속 watchdog 부팅에서 recovery를 선택합니다. 실제 retained RAM의 CRC·전원 상실·원자적 기록·복구 프로그램은 구현하지 않습니다.

정상 실행은 32,768 tick/window 조합, literal 창 경계 5개, health 경계, 내부 오류 대조 6개와 입력 거부 7개를 확인합니다. 같은 검사에 포함된 대조를 독립 고장 수나 fault coverage로 합산하지 않습니다. 실제 시간 단위·클록 허용오차·debug freeze·option bytes는 장치 문서와 보드에서 따로 확인해야 합니다.

- [원리와 실제 출력](../../../설계와검증사례_engineering-cases/작업진행을확인하는워치독과리셋기록_watchdog-health-reset.md)
- [2026-10-21 실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/워치독진행상태와리셋검사_20261021.md)
- [예외 상태와 고장 원인 추적](../../../현장계측과검증_measurement-validation/펌웨어와디버깅_firmware-debugging/예외상태와고장원인추적_cortex-m-fault-debugging.md)

## English

This deterministic host suite contrasts periodic watchdog feeding with per-task fresh progress epochs. It checks an explicit `[4, 12)` tick window, wraparound, capture-before-clear reset records and a three-failure recovery policy. Reset time is sampled at scripted polls; asynchronous hardware timing, MCU resets and persistent storage are not executed.
