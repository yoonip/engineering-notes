# RTOS 스케줄과 알림의 사건 모델 / Deterministic RTOS scheduling and notification models

실제 커널을 실행하기 전에 자원 대기와 알림 계약을 분리해 살펴보는 Python 예제입니다. 표준 라이브러리만 사용하며 실제 FreeRTOS 커널·MCU·ISR·시간 계측은 실행하지 않습니다. 잘못된 경로는 의도적으로 만든 교육용 사례입니다.

| 실행 코드 | 문제와 수정 경로 | 해설 |
| --- | --- | --- |
| [models.py](models.py)의 `priority_schedule` | 중간 우선순위 간섭과 상속 적용을 같은 작업량에서 대조합니다. | [뮤텍스 대기와 마감시간](../../../설계와검증사례_engineering-cases/뮤텍스대기와마감시간_rtos-priority-inversion.md) |
| [models.py](models.py)의 `wakeup_schedule`·`coalesced_batch` | 검사와 대기 사이의 도착, 알림 보존, 묶인 알림 뒤 큐 처리를 비교합니다. | [검사와 대기 사이의 알림 유실](../../../설계와검증사례_engineering-cases/검사와대기사이의알림유실_rtos-lost-wakeup.md) |
| [verify.py](verify.py) | 작업 블록의 독립 기대값·사건 순서 조건·payload 보존으로 판정합니다. | [2026-10-21 검증 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/RTOS스케줄과알림검사_20261021.md) |

## 실행

Python 3.10 이상에서 이 폴더를 기준으로 실행합니다. 출력 폴더는 새 이름이어야 하며, 기존 결과를 덮어쓰지 않습니다.

```powershell
python verify.py --output C:/temp/rtos-model-new
```

정상 검사는 종료 코드 0과 `status=passed`를 반환합니다. `results.json`에는 환경·인수·소스 SHA-256·관측 사건·독립 검사·결함 대조 결과가 들어갑니다. 우선순위 작업량 270조합과 각 조합의 마감시간 경계 2개, 알림 순서 3개를 확인합니다. 이 숫자는 실물 장치의 시험 횟수나 상태 공간 전체를 뜻하지 않습니다.

검출기가 실제로 오류를 거부하는지 확인하는 명령입니다. 두 실행은 의도대로 종료 코드 1과 `status=failed`가 나와야 합니다. 먼저 발생한 불일치도 JSON에 기록합니다.

```powershell
python verify.py --inject priority-no-inherit --output C:/temp/rtos-missing-inheritance-new
python verify.py --inject notify-clear --output C:/temp/rtos-clear-pending-new
```

`require()`는 조건이 틀리면 예외를 발생시킵니다. Python 최적화 옵션에 따라 생략되는 `assert`에 의존하지 않습니다. 중간에 예외가 발생한 결함 실행을 정상 검사와 같은 통과 결과로 합치지 않습니다.

## 모델의 경계

우선순위 모델은 단일 CPU·서로 다른 우선순위·뮤텍스 하나·시각 1의 H/M 준비를 가정합니다. 잠금 API 비용, 스위치 비용, ISR, tickless·SMP·중첩 잠금·타임아웃은 구현하지 않습니다. 사건 단위의 시간은 실제 FreeRTOS tick이나 밀리초와 대응시키지 않습니다.

알림 모델의 C·W·P는 추상 사건입니다. W의 알림 확인과 대기 등록은 하나의 동기화 연산으로 놓습니다. P가 대기자를 깨우는 경우에는 그 소비자가 다시 실행해 payload를 비우는 부분까지 묶었습니다. 실제 커널 내부의 모든 선점 지점이나 메모리 모델을 그대로 재현하지 않습니다.

## English

The standard-library fixtures compare priority inheritance with an independent block-order oracle and enumerate notification arrival around a check/wait boundary. CLI fault injection must fail verification. The JSON records environment, source hashes, observations, and scope. No FreeRTOS binary, MCU, ISR, or physical timing measurement is executed.
