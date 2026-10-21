# 인터럽트·DMA·캐시 계약 모형 / Interrupt, DMA and cache contract models

상태 비트 소거·완료 버퍼 소유권·캐시와 RAM의 차이를 분리하는 Python 호스트 예제입니다. 실제 MCU 레지스터·인터럽트·DMA·캐시 명령을 실행하지 않습니다. 입력과 잘못된 경로는 직접 만든 교육 자료입니다.

| 파일 | 실제 내용 |
| --- | --- |
| [fixtures.json](fixtures.json) | 상태 비트, TX/RX 바이트, 같은 line의 이웃 flag, 버퍼 번호의 자체 입력 |
| [models.py](models.py) | W1C, 버퍼 재사용 정책, 32바이트 write-back 캐시와 RAM의 추상 모형 |
| [verify.py](verify.py) | 비트 집합·바이트별 범위·입력 payload를 이용한 독립 기대값 검사 |

## 실행

Python 3.10 이상과 표준 라이브러리만 필요합니다. 이 폴더에서 실행하며 출력은 새 폴더를 지정합니다.

```powershell
python -B verify.py --output C:/temp/irq-dma-review-new
```

정상 결과는 `status=passed`·종료 코드 0입니다. `results.json`은 환경·인수·소스/입력 SHA-256·관측·오류 대조를 남깁니다. 8비트 정적 pending/mask 65,536조합과 128바이트 메모리 안의 시작/길이 8,385조합을 검사합니다. 이 수는 실제 IRQ·보드의 시험 횟수가 아닙니다.

잘못된 경로를 정상 계약에 넣어 검출기가 거부하는지 확인할 수 있습니다. 아래 세 명령은 각각 `status=failed`·종료 코드 1이 기대값입니다.

```powershell
python -B verify.py --inject w1c-rmw --output C:/temp/irq-rmw-fault-new
python -B verify.py --inject tx-no-clean --output C:/temp/dma-tx-fault-new
python -B verify.py --inject allow-owned-reuse --output C:/temp/dma-owner-fault-new
```

기존 출력 경로는 CLI 오류·종료 코드 2로 거부합니다. 이전 JSON을 덮어쓰지 않습니다. 검사 함수는 일반 예외를 발생시키므로 Python `-O`에서 생략되는 `assert`에 의존하지 않습니다.

## 모형의 경계

- W1C는 소거 전 pending과 처리한 mask의 정적 관계입니다. 읽기/쓰기 사이 새 IRQ 도착, 동일 비트의 여러 사건 누적, 실제 NVIC·레지스터의 부작용은 모형에 없습니다.
- 버퍼 모형은 A가 CPU 소유이고 B가 완료 대기일 때 새 전송 시작을 거부합니다. 이미 동작 중인 실제 DMA를 안전하게 중단했다는 결과가 아닙니다.
- 캐시는 32바이트 line·128바이트 RAM·단순 dirty 표시를 사용합니다. 실제 캐시의 용량·way·교체 정책·버스·store buffer·명령 지연·barrier를 재현하지 않습니다.
- RX 사전 처리 뒤 오래된 clean 사본을 채우는 사건은 사후 invalidate의 필요 조건을 분리한 가정입니다. MCU에서 speculative read를 관측한 기록이 아닙니다.

## 해설과 실행 기록

- [상태 비트 소거와 완료 버퍼 소유권](../../../설계와검증사례_engineering-cases/상태비트소거와완료버퍼소유권_irq-w1c-ownership.md)
- [캐시와 RAM의 데이터 불일치](../../../설계와검증사례_engineering-cases/캐시와RAM의데이터불일치_dma-cache-lines.md)
- [2026-10-21 실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/인터럽트DMA캐시모델검증_20261021.md)

## English

The standard-library fixtures compare deliberate W1C, ownership and cache-maintenance faults with explicit contracts. Independent bit-set and bytewise-range oracles check static state combinations. CLI mutation must fail, and existing output directories are refused. No hardware register, IRQ, DMA or cache-maintenance instruction is executed.
