# RAID 패리티 갱신 중단과 사본 복원 / RAID parity interruption and copy reconstruction

4바이트 데이터 두 개와 패리티 한 개를 실제 호스트 파일에 기록합니다. D0만 바뀐 상태와 P만 바뀐 상태를 따로 만들고, 매번 새 Python 프로세스에서 빠진 D1을 계산합니다. 유효한 전체 stripe redo와 별도 세대 기준이 있을 때에는 새 폴더로 복원합니다. 자체 XOR1 형식이며 Linux md·mdadm·물리 디스크·전원 차단을 실행하지 않습니다.

| 파일 | 역할 |
| --- | --- |
| [model.py](model.py) | 3개 멤버 파일·dirty/세대·56바이트 redo·새 사본 복원 CLI입니다. |
| [fixtures.json](fixtures.json) | 이전/새 stripe·혼합 상태·잘못 복원된 D1의 고정 리터럴입니다. |
| [verify.py](verify.py) | 별도 프로세스·고정 중단 경계·불완전 로그 prefix·원본 보존·변이를 검사합니다. |

[원리와 계산](../../../설계와검증사례_engineering-cases/RAID패리티의부분갱신과복원_raid-parity-write-hole.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/RAID패리티중단과복원검사_20261021.md)

## 실행

Python 3.10 이상 표준 라이브러리만 사용합니다. 이 폴더에서 독자가 정한 새 출력 경로를 사용합니다.

```powershell
python -X utf8 -B verify.py --output C:/temp/raid-normal-new
python -X utf8 -B -O verify.py --output C:/temp/raid-optimized-new
python -X utf8 -B -O verify.py --mutation trust-dirty --output C:/temp/raid-trust-new
python -X utf8 -B -O verify.py --mutation replay-incomplete --output C:/temp/raid-incomplete-new
python -X utf8 -B -O verify.py --mutation accept-two-missing --output C:/temp/raid-two-new
python -X utf8 -B -O verify.py --mutation skip-generation --output C:/temp/raid-stale-new
```

정상 검증의 종료값은 0, 의도적 변이를 검출한 검증의 종료값은 1입니다. 검증기의 기존 출력 폴더는 종료 2로 거부합니다. 모델 CLI가 정보 부족·잘못된 입력·기존 복원 목적지를 거부하면 종료 3입니다. `results.json`에는 실제 명령·stdout·stderr·종료값·환경·검사·소스와 fixture SHA-256을 남깁니다. `-O`에서도 `raise` 검사가 유지됩니다.

## 자료와 세대

이전 `[D0,D1,P]`는 `[10111213,a0a1a2a3,b0b0b0b0]`, 새 상태는 `[20212223,a0a1a2a3,80808080]`입니다. 세대는 7→8입니다. D0와 P 중 하나만 갱신한 뒤 D1을 계산하면 양쪽 순서 모두 `90919293`이며 원래 D1과 다릅니다. 이 계산은 `UNTRUSTED_DIAGNOSTIC`으로만 반환합니다.

`meta.json`은 자체 형식·stripe 0·현재 세대·dirty·보류 세대를 담습니다. clean 세대는 1~65534, dirty 세대는 1~65533만 지원합니다. metadata는 이 실험에서 신뢰하는 독립 기준이며 서명·별도 보안 저장소·공격자 방어가 없습니다. clean 표시는 원본 payload의 암호학적 증명이 아닙니다.

`redo.bin`은 `<4sII12s`의 24바이트 header와 SHA-256 32바이트입니다. header에 RDL1·stripe·대상 세대·전체 D0/D1/P가 있습니다. 정확한 길이·digest·stripe·세대·패리티를 검사합니다. 56바이트의 proper prefix 0~55는 복구 자료로 받아들이지 않습니다. 다른 세대의 온전한 기록도 거부합니다. 이 형식은 Linux md journal이나 PPL 형식이 아닙니다.

## 지원하는 복원

clean의 완전한 stripe는 패리티 일치를 검사하고, 한 멤버 결손은 다른 두 멤버의 XOR로 재구성합니다. dirty는 유효한 full-stripe redo가 필요합니다. dirty 표시만 있고 로그가 없으면 모든 멤버가 남아 있어도 `NEEDS_RECOVERY_DATA`입니다. 이 보수적인 정책은 데이터가 바뀌기 전인지, 갱신이 끝났는지를 표시 하나로 추측하지 않습니다. 두 멤버 이상 결손은 정상 로그가 있어도 자체 지원 범위 밖으로 거부합니다.

복원은 새 목적지 폴더에만 기록합니다. 읽기 검증·원본 해시 확인을 거쳐 파일을 만들고 readback을 비교합니다. 기존 목적지·원본 안의 목적지·symlink 입력·예상 밖 파일·길이 오류는 거부합니다. 동시 writer와 임의 host crash의 원자적 디렉터리 게시를 구현하지 않습니다. I/O 실패 시 새 폴더 일부가 남을 수 있으며 성공 결과로 보고하지 않습니다.

같은 mask로 D0·P를 바꾸면 패리티가 맞아도 원본과 달라질 수 있습니다. 별도 양성 반례가 이를 기록합니다. 복원 재실행 결과가 같다는 멱등성도 원본과 같다는 증명은 아닙니다.

## 공식 방식과의 연결

Linux 6.12의 [write journal](https://docs.kernel.org/6.12/driver-api/md/raid5-cache.html)과 [PPL](https://docs.kernel.org/6.12/driver-api/md/raid5-ppl.html)은 서로 다른 정보를 남깁니다. 이 예제는 새 stripe 전체를 저장하는 자체 redo만 실행합니다. [md 관리자 문서](https://docs.kernel.org/6.12/admin-guide/md.html)의 dirty/degraded 및 bitmap 설명은 결손과 갱신 미완료를 구분하는 배경 자료입니다. 열람 범위와 비교는 사례 본문에 있습니다.

`interrupt`는 dirty 표시→선택한 로그→첫 멤버→둘째 멤버→clean 표시 중 선택한 경계에서 동기화하고 정상 반환합니다. 새 프로세스가 그 파일을 읽습니다. 실제 프로세스 kill·OS crash·전원 제거·4바이트 원자성·장치 cache·회전 패리티 배치·RAID6·성능 시험은 아닙니다.

## English

Three four-byte host files hold one fixed XOR stripe. A mixed generation reconstructs missing D1 as 90919293 rather than the independent a0a1a2a3 oracle. A complete 56-byte full-stripe redo record with a matching trusted generation permits copy recovery. Dirty-only states, incomplete or stale records and multiple missing members are refused. Repeated recovery checks byte identity and source preservation. Consistent data/parity corruption demonstrates that XOR agreement is not proof of original content. Selected boundaries return normally after synchronization; this is not a Linux md, disk-power or sector-atomicity test.
