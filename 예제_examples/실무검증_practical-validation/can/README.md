# CAN 복구 정책과 수신 계약 / Reproducible CAN policy and payload checks

표준 라이브러리 Python으로 합성 controller 관측과 자체 응용 프레임을 재생합니다. 실제 차량·설비·CAN 어댑터·SocketCAN·vcan에는 접속하지 않습니다. CAN error confinement, 물리 파형, arbitration, bit timing, CRC나 드라이버를 구현한 모형이 아닙니다.

## 실행

이 폴더에서 다음 명령을 실행합니다. Python 3.12.14·Windows AMD64에서 확인했습니다.

```powershell
python -B run_cases.py --output C:/temp/can-review-new
```

`-B`는 바이트코드 캐시를 쓰지 않게 합니다. Windows에서 `python`이 실행 파일 대신 Store 별칭으로 연결되어 있다면 설치한 Python 실행 파일의 경로를 사용합니다. 외부 패키지는 필요하지 않습니다. 출력 폴더는 매번 새 이름을 사용하며 기존 경로는 오류로 거부합니다.

`results.json`에는 입력별 판정, 의도적으로 잘못 만든 경로의 결과, 예상 입력 예외, Python·OS·명령·UTC 시각·소스/입력 SHA-256이 들어갑니다. 정상 계약과 오류 검출이 기대대로이면 PASS·종료 코드 0, 검사 실패나 예기치 않은 예외는 ERROR·1, 기존 출력 경로 등 CLI 오류는 2입니다. 의도한 결함이 검출됐다는 이유로 실행 전체를 ERROR로 표시하지 않습니다.

## 코드와 입력

| 파일 | 실제 내용 |
| --- | --- |
| [run_cases.py](run_cases.py) | 복구 상태 정책, 프레임 유효성 검사, 의도적인 오류 경로, 입력 예외, 결과 기록 |
| [controller_trace.json](controller_trace.json) | 25개 합성 관측과 리터럴 기대 action |
| [application_frames.json](application_frames.json) | 24개 응용 레코드와 기대 판정·알려진 mV |

복구 정책은 READY에서 bus-off를 관측하면 송신을 막습니다. 자체 대기시간 100 ms, 직전 1,000 ms 동안 최대 요청 2개, 요청 후 활성 확인을 구분합니다. 같은 미복구 회차의 bus-off 재관측은 대기 기준을 미루거나 새 요청으로 세지 않습니다. 이 시간·횟수는 제품 규격이나 CAN 표준이 아닙니다.

응용은 표준 ID 0x321·Classical data·정확히 8바이트만 사용합니다. 버전, 8비트 순번, little-endian mV, 32비트 ms 샘플 시각을 직접 정의했습니다. 샘플·수집·사용 시각은 동일한 순환 단조 시계이고 실제 차이가 반주기보다 작다는 가정입니다. 별도 ECU 시계와 호스트 시각을 동기화 없이 비교하는 절차가 아닙니다.

순번 차이는 정확히 1만 허용합니다. 따라서 유실 후 자동 재동기화가 없는 진단 정지 모형입니다. 실제 제품의 유실 허용·송신기 재부팅·명시적 재동기화·확인 timeout·명령 중복 처리는 별도 설계가 필요합니다.

## 확인한 결과

controller 관측 25개가 기대 action과 같았고, 재시작 요청은 140·300·1,140 ms였습니다. 응용 레코드 24개는 채택 6개·거부 18개였으며 잘못된 입력 12개는 `InputError`였습니다. 정상 실행과 `python -B -O`의 판정이 같았고, 사본의 기대값을 의도적으로 바꾼 검사는 `-O`에서도 실패를 검출했습니다. 코드의 `require`는 일반 `assert` 문처럼 최적화 옵션으로 사라지지 않습니다.

이 수는 직접 구성한 입력의 검사 수입니다. 실제 장애 수·실차 통과율·표준 적합성·모든 상태의 전수 검증을 뜻하지 않습니다. [2026-10-21 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/CAN정책과수신계약검증_20261021.md)에서 환경·해시·검사 범위를 확인할 수 있습니다.

## 원인과 해결

- [ACK와 복구 정책](../../../설계와검증사례_engineering-cases/CAN의ACK와복구정책_can-recovery-policy.md): 송신 대기열과 응용 완료 혼동, 요청 즉시 READY, 재시작 제한을 다룹니다.
- [수신값의 형식과 신선도](../../../설계와검증사례_engineering-cases/CAN수신값의형식과신선도_can-payload-contract.md): 바이트 순서, 거부 전 상태 변경, 대기열의 오래된 값, 순환 시계를 다룹니다.

## English

This standard-library runner replays 25 synthetic controller observations and 24 invented application records. It contrasts intentionally faulty restart/state-update paths with explicit contracts, checks twelve malformed inputs, and records reproducible inputs and environment. No physical CAN, SocketCAN/vcan, error-confinement, CRC, or automatic application resynchronization is tested.
