# 시간 초과 뒤 재시도와 늦은 쓰기 / Retry and late writes after timeout

[사례 본문](../../../설계와검증사례_engineering-cases/시간초과뒤늦은쓰기와재시도_block-io-timeout-retry.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/IO재시도와늦은완료검사_20261021.md)

이미 해석된 사건을 Python 객체에 순서대로 입력하는 교육용 모델입니다. 4바이트 LBA 하나의 `APPLY`와 호스트 `CALLBACK`을 구분하여, 옛 callback을 무시해도 옛 쓰기의 효과는 남는 반례를 실행합니다. 커널·NVMe·MMC·물리 장치·DMA·벽시계 타이머를 실행하지 않습니다.

| 파일 | 내용 |
| --- | --- |
| [model.py](model.py) | 응용 요청·제출 시도·버퍼 소유권·장벽·명시적 정지 증거의 상태입니다. |
| [fixtures.json](fixtures.json) | `AAAA`, `BBBB`, 응용 완료 목록 등 직접 적은 기대값입니다. |
| [verify.py](verify.py) | 7개 흐름, 정상·입력 거부·경계·4종 오류 변이를 검사합니다. |

## 입력과 상태

`start(rid, aid, kind, payload, slot)`에서 `rid`는 응용 요청, `aid`는 한 번의 제출 시도, `slot`은 버퍼 소유 표시입니다. 모두 1~24자의 ASCII 문자·숫자·밑줄·하이픈만 받습니다. `aid`와 `rid`는 한 실행에서 재사용하지 않습니다. 실제 장치의 태그 공간을 그대로 구현한 제한이 아닙니다. 요청은 최대 16개, 기본 시도 한도는 최초 제출을 포함하여 2개이며 1~4로 설정합니다. 쓰기는 소문자 16진수 8자리, 읽기는 payload `None`입니다.

`timeout()`은 `UNKNOWN`이며 진행 중 버퍼를 반환하지 않습니다. 성공 완료가 먼저 왔다면 이후 timeout은 `ALREADY_RESOLVED`입니다. `apply()`가 내부 값을 바꾸며 `complete()`는 요청·시도 세대가 맞는 callback만 처리합니다. 실패 완료는 자동 rollback 없이 `FAILED_UNCERTAIN`으로 남습니다. `give_up()`은 옛 시도의 활동이 끝난 뒤에만 응용 실패를 한 번 알립니다.

수정 경로는 미해결 쓰기가 있으면 새 겹침 쓰기를 막습니다. 쓰기 retry도 옛 시도가 `COMPLETED` 또는 `QUIESCED`여야 합니다. `quiesce(aid, stopped=True)`의 참값은 옛 작업이 이후 장치·버퍼에 영향을 주지 못한다는 별도의 모델 전제입니다. 이 코드가 정지 증거를 수집하거나 Linux `blk_mq_quiesce_queue()`를 호출하는 기능은 없습니다. `stopped=False`는 장벽을 풀지 않습니다.

읽기 retry는 옛 읽기의 버퍼를 그대로 보유하고 새 버퍼를 할당합니다. 여기서 읽기는 매체 값을 바꾸지 않는 단순 읽기입니다. clear-on-read 레지스터·읽기 부작용·장치 상태 전이는 지원하지 않습니다. `slot`은 Python 소유권 표식이며 실제 포인터나 DMA 버퍼가 아닙니다.

## 실행

Python 3.10 이상과 표준 라이브러리를 사용합니다. 이 폴더에서 실행하고 매번 새 결과 폴더를 지정합니다. 아래 `python`은 설치된 Python 실행 파일입니다.

```powershell
python -X utf8 -B verify.py --out C:/temp/io-retry-normal-new
python -X utf8 -B -O verify.py --out C:/temp/io-retry-optimized-new
python -X utf8 -B verify.py --mutation callback-filter-only --out C:/temp/io-retry-fault-new
```

정상은 exit 0/PASS, 변이는 exit 1/ERROR입니다. 기존 결과 폴더와 잘못된 fixture schema는 exit 2로 거부합니다. `Checks.equal()`은 직접 `raise AssertionError`를 실행하므로 `-O`에서도 비교가 남습니다. JSON에 환경·명령·소스 해시·각 실제 사건을 기록합니다. 새 결과는 지정한 폴더에만 쓰며 공개 예제 폴더에 결과를 누적하지 않습니다.

| 변이 | 검사가 발견하는 오류 |
| --- | --- |
| `callback-filter-only` | 옛 쓰기가 남았는데 retry를 허용합니다. |
| `release-buffer-on-timeout` | timeout만으로 버퍼 소유권을 풀어 읽기 retry가 같은 slot을 사용합니다. |
| `unbounded-retry` | 설정한 두 시도 뒤 세 번째 시도를 허용합니다. |
| `accept-stale-callback` | 옛 시도가 응용 완료를 다시 알립니다. |

2026-10-21에는 정상 기본·`-O` 각각 82개 검사와 45개 계약 거부가 통과했습니다. 4종 변이를 두 모드로 실행한 8회는 모두 기대한 exit 1이었습니다. 기존 결과 재사용 2회와 잘못된 fixture 1회는 exit 2였으며 기존 결과 바이트가 유지되었습니다.

## 문법과 출처

`def`는 함수 정의, `class`는 상태와 메서드를 묶는 형 정의입니다. `self`는 그 객체, `{}`는 사전, `[]`는 리스트 또는 항목 접근, `()`는 함수 호출입니다. `from ... import`는 같은 폴더의 형을 가져오며 `@dataclass`는 상태 필드의 초기화 함수를 만듭니다. `None`은 payload가 없다는 값, `not in`은 정해진 상태 집합에 없다는 검사입니다. 실제 줄별 예는 사례 본문에 있습니다.

Linux [6.12 blk-mq 문서](https://docs.kernel.org/6.12/block/blk-mq.html)의 Operation·Tag-based completion·`blk_eh_timer_return`·`blk_mq_ops.timeout`·`blk_mq_quiesce_queue`와 [v6.12 헤더](https://github.com/torvalds/linux/blob/v6.12/include/linux/blk-mq.h)의 timeout enum을 확인했습니다. 자체 `QUIESCED`는 커널 queue quiesce보다 강한 입력 전제이며, 호출 이름이 비슷하다는 이유로 장치 활동 종료를 보장하지 않습니다.

## English

This standard-library event model separates a device-side four-byte write from its host callback. A callback-only filter produces final `AAAA` after a newer `BBBB` has completed. The guarded path retains buffers and blocks overlapping writes until completion or explicit external evidence that an old attempt can no longer have effects. It then permits a bounded retry. Read retries retain distinct old and new buffer ownership. These are decoded events, not Linux block, NVMe, DMA, timing, or power-loss tests.
