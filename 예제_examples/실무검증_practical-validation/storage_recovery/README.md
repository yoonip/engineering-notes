# 중단된 데이터 저널 복구 / Recovering an interrupted data journal

Python 표준 라이브러리로 실제 호스트 파일을 기록하고 매번 새 Python 프로세스로 다시 읽습니다. DATA와 COMMIT을 분리해 여러 필드를 함께 확정하는 자체 redo 저널입니다. SQLite를 실행하거나 그 파일 형식을 구현하지 않습니다. 실제 전원 차단·OS crash·flash fault도 실행하지 않습니다.

| 파일 | 내용 |
| --- | --- |
| [models.py](models.py) | framing·길이·순번·CRC·COMMIT 결합 검사와 실제 파일 기록/복구 CLI입니다. |
| [fixtures.json](fixtures.json) | 직접 정한 상태·기록 bytes·크기·SHA-256의 고정 기대값입니다. |
| [verify.py](verify.py) | 새 프로세스 호출, prefix 중단 60개, 손상·경계·의도적 변이와 JSON 기록입니다. |

[사례 본문](../../../설계와검증사례_engineering-cases/중단된저널의트랜잭션복구_storage-journal-recovery.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/저장저널중단과복구검사_20261021.md)

## 실행

Python 3.10 이상에서 이 폴더를 작업 경로로 사용합니다. C:/temp는 독자가 정하는 새 출력 경로의 예입니다.

```powershell
python -X utf8 -B verify.py --output C:/temp/journal-normal-new
python -X utf8 -B -O verify.py --output C:/temp/journal-optimized-new
python -X utf8 -B -O verify.py --mutation apply-uncommitted --output C:/temp/journal-early-new
python -X utf8 -B -O verify.py --mutation ignore-crc --output C:/temp/journal-crc-new
python -X utf8 -B -O verify.py --mutation ignore-sequence --output C:/temp/journal-sequence-new
python -X utf8 -B -O verify.py --mutation commit-first --output C:/temp/journal-order-new
```

정상 실행은 PASS·종료 0, 네 변이는 ERROR·종료 1입니다. 기존 출력 폴더는 종료 2로 거부합니다. 모델 CLI의 의도한 입력/손상 거부는 종료 3, 선택 prefix를 동기화한 뒤 명시 종료한 자식은 23입니다. 검증기는 이 종료값과 별도의 리터럴 상태를 함께 확인합니다. 자식이 23으로 끝났다는 사실만으로 검증기가 실패한 것은 아닙니다.

각 정상 실행의 results.json에는 178개 검사·60개 cut·237개 자식 호출·13개 합성 손상/모호성 파일이 있습니다. actual command·stdout·stderr·exit·환경·소스/fixture SHA를 남깁니다. `happy/recovered.json`은 새 프로세스가 복원한 상태의 관측 보고서이며 crash-safe 데이터베이스 파일을 만든다는 뜻은 아닙니다.

## 자체 파일 계약

파일은 JNL1 4바이트로 시작합니다. 각 frame은 `<4sBBHI`의 12바이트 header, payload, CRC32 4바이트입니다. header에는 REC1·version1·kind·payload 길이·seq가 들어갑니다. `<`는 little endian이며 wire 표준이나 CPU native 구조체에 의존하지 않습니다.

DATA는 credit·stock 두 정수의 정렬된 compact JSON입니다. COMMIT payload는 그 DATA의 CRC 4바이트입니다. DATA/COMMIT의 seq가 같고 직전 확정 seq+1이어야 합니다. frame CRC는 header와 payload를 검사합니다. seq 1~65535·payload 1~128바이트·파일 최대 65536바이트·필드 값 0~1000은 교육용 한계이며 저장장치 사양이 아닙니다. 파일 상한 때문에 모든 seq까지 실제로 저장할 수 있다는 뜻도 아닙니다.

초기 파일 64바이트는 seq1·credit50·stock10입니다. 갱신 DATA는 `12+23+4=39`, COMMIT은 `12+4+4=20`, 합계 59바이트입니다. 둘을 다 확인하면 seq2·credit80·stock7이고 전체 파일은 123바이트입니다. cut 0~58은 이전 상태, cut59는 새 상태를 기대합니다. cut39는 DATA만 완성된 UNCOMMITTED_DATA이고 나머지 부족한 frame은 INCOMPLETE_FRAME입니다. cut0과59는 CLEAN입니다.

복구는 원본 저널을 읽기만 합니다. `committed_end`는 마지막 COMMIT 직후 위치입니다. 미확정 꼬리를 자동으로 잘라내거나 고치지 않으며, writer는 이런 꼬리가 있으면 TAIL_NEEDS_REPAIR로 추가 기록을 거부합니다. 잠금·동시 writer·checkpoint·회전·공간 회수·수명/마모 관리는 구현하지 않습니다.

## 손상과 부족한 끝부분

완전한 frame의 CRC 불일치·잘못된 magic·순번 누락·COMMIT 선행·COMMIT 결합 불일치는 거부하며 응용 상태를 반환하지 않습니다. 뒤에 정상 frame이 있어도 magic을 찾아 재동기화하지 않습니다. 그러나 짧은 마지막 header나 선언 길이에 못 미친 끝부분에서는 잘린 쓰기와 손상을 완전히 구별할 수 없습니다.

별도 대조는 길이를 합법 범위 128로 훼손합니다. 뒤에 온전한 COMMIT과 seq3 기록까지 있지만, parser가 요구하는 끝 위치 208보다 파일 182바이트가 작아 INCOMPLETE_FRAME으로 남습니다. seq1 상태와 ignored118만 반환합니다. 따라서 “내부 손상은 모두 검출한다”는 보장을 하지 않습니다. CRC도 인증이나 공격자 변경 방지가 아닙니다.

## 호스트 시험과 내구성

중단 자식은 지정한 prefix만 쓰고 `flush()`·`os.fsync()`를 호출한 뒤 `os._exit(23)`으로 끝납니다. 새 프로세스가 실제 파일을 다시 읽습니다. 이는 성공한 동기화 뒤 정한 바이트가 남는 호스트 시험입니다. 동기화 도중의 임의 장치 손상·재정렬·sector tearing·디렉터리 동기화·전원 제거를 시험하지 않습니다. Windows에서 실행했으며 Linux 파일시스템의 내구성을 시험한 결과도 아닙니다.

## 짧은 문법 안내

| 문법·기능 | 역할 |
| --- | --- |
| import / from ... import | json·struct·zlib 등의 기능을 불러옵니다. |
| def / class / self | 함수·검사 묶음의 형식·그 객체의 상태를 정의합니다. |
| bytes / dict / list / tuple | 기록 바이트·상태 키/값·확정 번호 목록·보류 DATA 묶음입니다. |
| `[]`, `[:cut]`, `[-4:]` | 키 접근·prefix·뒤 CRC 4바이트 선택입니다. |
| `is None`, `==`, `!=`, `in` | 보류 상태·동일성/차이·허용 형식을 비교합니다. |
| with / open / flush / fsync | 파일 범위와 사용자 버퍼·호스트 동기화 요청을 구분합니다. |
| struct.pack / unpack_from | 고정 크기 정수와 바이트를 변환합니다. |
| try / except / raise | 거부할 입력과 기대 계약 위반을 명시합니다. |
| subprocess.run | 앞 프로세스의 Python 객체를 재사용하지 않고 파일을 다시 읽습니다. |

## Sources and scope

[SQLite Atomic Commit](https://www.sqlite.org/atomiccommit.html)의 기록·동기화·복구와 crash-test 설명, [SQLite WAL format](https://www.sqlite.org/fileformat2.html#walformat)의 frame·commit marker·검사값을 참고했습니다. 자체 저널은 SQLite format과 다릅니다. [Linux man-pages 6.19 fsync](https://man7.org/linux/man-pages/man2/fsync.2.html)와 [Python 3.12 os.fsync](https://docs.python.org/3.12/library/os.html#os.fsync)는 파일·디렉터리 동기화와 플랫폼 경계를 읽는 자료입니다. 열람일은 2026-10-21입니다.

## English

A bounded two-key redo journal replays only DATA/COMMIT pairs with matching sequence and DATA checksum. Sixty persisted prefixes of one 59-byte update are reopened by fresh Python processes. Complete-frame corruption is rejected, but a damaged length can resemble an incomplete tail; this limitation has a positive demonstration. Four implementation mutations fail in normal and optimized runs. No SQLite execution, operating-system crash, flash power cut, or physical durability claim is made.
