# FTL의 매핑 게시와 GC·TRIM / FTL publication, GC and TRIM

3개 논리 페이지(LPN)를 12개 물리 페이지(PPN)에 연결하는 교육용 파일 모델입니다. 한 사용자 자료는 4바이트이고 erase block은 3페이지입니다. 실제 파일에 DATA/ERASE 사건과 매핑을 append하고 매번 새 Python 프로세스에서 재구성합니다. 실제 NAND program/erase·SSD firmware·NVMe 명령·OS crash·전원 차단 장비를 실행하지 않습니다.

| 파일 | 역할 |
| --- | --- |
| [models.py](models.py) | 물리 사건·매핑 재생, 자료 확인, GC snapshot·주소 세대·TRIM tombstone입니다. |
| [fixtures.json](fixtures.json) | 고정 값·LPN/PPN·버전·incarnation·기록 bytes와 작업 trace입니다. |
| [verify.py](verify.py) | 리터럴 비교, 98개 중단 지점, 잘못된 경로 5종, 손상·경계와 실행 JSON입니다. |

[매핑 게시 사례](../../../설계와검증사례_engineering-cases/FTL의매핑게시와전원중단_ftl-map-publication.md) · [GC·TRIM 사례](../../../설계와검증사례_engineering-cases/FTL의GC와폐기된주소재사용_ftl-gc-trim-reuse.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/FTL매핑과GC중단검사_20261021.md)

## 자체 매체와 복구 계약

`physical.log`는 DAT1 뒤의 고정 32바이트 DATA/ERASE 기록입니다. DATA에는 PPN·LPN·논리 version·4바이트 자료와 CRC32가 있습니다. 전체 물리 사건의 순번을 incarnation으로 사용해 같은 PPN의 재사용을 구분합니다. ERASE도 순번을 쓰므로 새 자료의 incarnation이 연속할 필요는 없습니다.

`mapping.log`는 MAP1 뒤의 48바이트 WRITE/MOVE/TRIM 기록입니다. 새 참조와 기대한 이전 `[논리 version, PPN, incarnation]`을 함께 기록합니다. host write·TRIM은 논리 version을 늘리고 GC MOVE는 그대로 유지합니다. 물리 페이지의 LPN·version·incarnation·CRC가 최신 매핑과 모두 맞아야 값을 공개합니다. journal CRC가 맞다는 사실만으로 다른 LPN의 자료를 돌려주지 않습니다.

ERASE는 파일에서 예전 bytes를 지우는 작업이 아니라 블록의 3개 주소를 free로 바꾸는 자체 사건입니다. 파일 이력에는 옛 자료가 남습니다. TRIM 뒤 반환하는 `None`도 자체 unmapped 정책입니다. 실제 SSD의 TRIM 뒤 읽기가 항상 0이라는 주장이나 secure erase 보장이 아닙니다.

일반 쓰기는 새 DATA 기록→다시 읽어 확인→매핑 게시 순서입니다. 이전 매핑을 먼저 지우지 않습니다. 미참조 DATA는 stale로 남고, GC가 현재 live인 페이지를 victim 밖으로 복사·확인·MOVE한 뒤 victim을 ERASE합니다. 유효 PPN 중복·존재하지 않는 페이지·다른 논리/물리 세대·CRC 불일치는 거부합니다.

고정 기록보다 짧은 끝부분은 `inspect`에서 보류합니다. `ready`·write·GC는 이런 꼬리를 TAIL_NEEDS_REPAIR로 거부합니다. 자동 truncation·checkpoint·로그 회전·공간 회수는 구현하지 않습니다. 완전한 기록의 CRC 손상은 거부하지만 임의 손상 전체를 진단하는 형식은 아닙니다.

## GC와 임시 공간

plan-gc는 현재 live 페이지와 매핑 token을 파일로 남깁니다. finish-gc는 새 프로세스에서 token·원본 내용·incarnation을 다시 확인합니다. 그 사이 host write나 TRIM이 있었다면 STALE_GC_SNAPSHOT입니다. 마지막 erase 직전에도 현재 live 페이지가 victim 안에 남았는지 확인합니다.

snapshot 뒤 다른 LPN의 새 live 페이지가 victim에 생기면, 기존 페이지의 MOVE를 게시한 뒤 ERASE_LIVE_BLOCK으로 중단될 수 있습니다. 논리 값은 보존되지만 GC 전체를 하나의 원자적 작업으로 되돌리는 기능은 아닙니다. 단일 프로세스 안의 임의 동시 실행도 구현하지 않았으며, plan/완료 사이의 순서를 별도 프로세스로 구성합니다.

일반 쓰기는 최소 free 1페이지를 남기는 자체 정책입니다. 그 한 페이지가 victim 안에 있으면 복사 공간으로 쓸 수 없습니다. 또한 live가 여러 개인 victim에는 더 많은 공간이 필요할 수 있습니다. NO_GC_TEMP_SPACE를 확인하며, 후보 선택 최적화·자동 재시도·무한 작업 진척을 보장하지 않습니다.

## 실행

Python 3.10 이상 표준 라이브러리만 사용합니다. 이 폴더에서 새 출력 경로를 지정합니다. 아래 C:/temp는 독자가 선택할 경로의 예입니다.

```powershell
python -X utf8 -B verify.py --output C:/temp/ftl-normal-new
python -X utf8 -B -O verify.py --output C:/temp/ftl-optimized-new
python -X utf8 -B -O verify.py --mutation publish-first --output C:/temp/ftl-map-first-new
python -X utf8 -B -O verify.py --mutation erase-old-first --output C:/temp/ftl-erase-first-new
python -X utf8 -B -O verify.py --mutation wrong-page-identity --output C:/temp/ftl-identity-new
python -X utf8 -B -O verify.py --mutation stale-gc --output C:/temp/ftl-stale-gc-new
python -X utf8 -B -O verify.py --mutation ignore-trim --output C:/temp/ftl-trim-new
```

정상은 PASS·종료 0, 다섯 변이는 ERROR·종료 1입니다. 기존 출력은 종료 2로 거부합니다. 모델 자식의 의도한 거부는 종료 3, 선택 prefix를 동기화한 뒤 명시 종료한 자식은 23입니다. 검증기는 종료값과 별도로 적은 상태를 함께 비교합니다. JSON에는 환경·명령·stdout/stderr·exit·소스/fixture SHA-256이 있습니다.

## 실행 범위와 계산

write DATA 0~32와 map 0~48의 82개 prefix를 모두 확인합니다. GC는 DATA/map/ERASE마다 0·1·N−1·N의 12개 지점, TRIM은 map 0·1·47·48의 4개 지점입니다. 합계 98개는 정한 유한 중단 행렬이며 모든 장치 고장의 열거가 아닙니다.

여섯 번의 host write 뒤 valid 3·stale 6·free 3입니다. 한 live 페이지를 복사하고 세 페이지 블록을 ERASE하면 free 5가 되어 순증은 2입니다. 이 구간의 host 자료 쓰기 6회와 GC 복사 1회는 자료 페이지 기록 7/6의 비율입니다. 초기 seed·매핑 metadata·ERASE 기록·ECC·NAND 내부 동작을 제외한 자체 계산으로 실제 SSD WAF 측정값이 아닙니다.

두 로그 파일의 상한 65,536바이트, 번호·version·incarnation의 상한 65,535는 교육용 제한입니다. GC ticket에는 같은 파일 크기 상한을 강제하지 않습니다. 로그 상한 때문에 모든 번호까지 실제로 쓸 수 있다는 뜻은 아닙니다. CRC는 인증이 아니며 악의적 metadata 변경을 막는 secure storage가 아닙니다.

## 짧은 문법 안내

| 문법·자료구조 | 이 코드에서의 뜻 |
| --- | --- |
| import / from ... import | struct·zlib·Path와 모델 함수를 불러옵니다. |
| def / class / self | 함수·검사 객체의 형식·그 객체의 상태를 정의합니다. |
| [] / {} / tuple | LPN별 참조 목록·PPN별 페이지 사전·비교할 token 묶음입니다. |
| `is None`, `not in`, `==` | unmapped 여부·빈 주소·기대 세대의 일치를 확인합니다. |
| enumerate / range / for | 위치와 값을 함께 읽거나 정한 범위를 순회합니다. |
| `//`, `%`, `[:cut]` | PPN의 블록 번호·짧은 꼬리·중단 prefix를 계산합니다. |
| with / flush / os.fsync | 파일 범위와 사용자 버퍼·호스트 동기화 요청을 나눕니다. |
| try / except / raise | 입력 거부와 기대 계약 위반을 구분합니다. |

## 출처와 실물의 경계

[KIOXIA L2P 기술 문서](https://europe.kioxia.com/content/dam/kioxia/shared/business/memory/ufs/asset/productbrief/KIOXIA_Understanding_Logical_Block_Address_Tech_Brief.pdf), November 2023 Rev. 1.0, [KIOXIA GC 기술 문서](https://www.kioxia.com/content/dam/kioxia/shared/business/memory/mlc-nand/asset/productbrief/KIOXIA_Understanding_Garbage_Collection_Tech_Brief.pdf), April 2023 Rev. 1.1a를 읽었습니다. 자체 token·CRC 기록 형식은 제조사 FTL 알고리즘을 재현한 것이 아닙니다.

자식은 지정 prefix만 쓰고 flush·fsync 성공 뒤 `os._exit(23)`으로 끝납니다. 실제 OS crash·동기화 도중 고장·sector tearing·directory fsync·장치 cache·NAND erase 시간·wear·bad block·ECC·실제 전압은 시험하지 않습니다.

## English

Three logical pages map to twelve physical pages in append-only host event files. Data identity is verified before map publication; GC rechecks its captured logical/physical token before copying and checks for live victim pages before erase. TRIM records an unmapped tombstone and physical incarnation distinguishes address reuse. Ninety-eight selected prefix interruptions are reopened by fresh processes. Recovery is read-only and does not truncate tails or make an entire GC atomic. The event log retains old bytes, and unmapped None is neither a device read-zero guarantee nor secure erasure. No NAND, SSD firmware, NVMe command, OS crash or physical power cut is executed.
