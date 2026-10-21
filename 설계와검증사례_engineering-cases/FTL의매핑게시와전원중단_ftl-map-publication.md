# FTL의 매핑 게시와 전원 중단 / FTL map publication across interrupted writes

새 자료가 기록되기 전에 주소표부터 새 위치로 바꾸면, 재시작한 뒤 아직 없는 자료를 읽으려 할 수 있습니다. 반대로 이전 위치를 먼저 지우면 새 쓰기가 끝나지 않았을 때 돌아갈 자료가 없습니다. 이 사례는 실제 파일과 새 Python 프로세스로 이 두 순서 오류를 재현합니다. NAND·SSD firmware·실제 전원 제거를 실행한 결과는 아닙니다.

[실행 코드와 입력](../예제_examples/실무검증_practical-validation/ftl_mapping/README.md) · [GC·TRIM 사례](FTL의GC와폐기된주소재사용_ftl-gc-trim-reuse.md) · [실행 기록](검증기록_evidence/FTL매핑과GC중단검사_20261021.md)

## 1. 같은 논리 주소가 다른 물리 위치를 가리킵니다

FTL은 Flash Translation Layer, 호스트가 쓰는 주소를 내부 저장 위치로 연결하고 관리하는 계층입니다. LPN은 논리 페이지 번호, PPN은 물리 페이지 번호입니다. 여기서는 논리 3개·물리 12개·사용자 자료 4바이트·erase block당 3페이지를 사용합니다. 실제 NAND page·sector 크기가 아닙니다.

KIOXIA의 L2P 기술 문서는 논리 주소가 유지되어도 GC 등의 내부 작업으로 물리 위치가 달라질 수 있고 매핑 metadata가 그 연결을 관리한다고 설명합니다. 이 예제는 그 개념에 자체 순서·CRC·세대 검사를 붙인 파일 모델입니다. 제조사 FTL의 기록 형식이나 복구 알고리즘을 재현하지 않습니다. [KIOXIA, November 2023 Rev. 1.0, pp. 1–3](https://europe.kioxia.com/content/dam/kioxia/shared/business/memory/ufs/asset/productbrief/KIOXIA_Understanding_Logical_Block_Address_Tech_Brief.pdf)

| 논리 주소 | 초기 물리 주소·incarnation | 초기 값 | LPN0 갱신 뒤 |
| --- | --- | --- | --- |
| LPN0 | PPN0·1 | 11111111 | PPN1·4의 aaaa0001을 가리킵니다. |
| LPN1 | PPN3·2 | 22222222 | 같은 매핑을 유지합니다. |
| LPN2 | PPN6·3 | 33333333 | 같은 매핑을 유지합니다. |

논리 version은 해당 LPN의 host write·TRIM 때 늘어납니다. incarnation은 물리 주소를 다시 사용했는지 구분하는 번호입니다. 이 코드에서는 DATA/ERASE 사건의 전체 순번을 DATA의 incarnation으로 씁니다. 따라서 ERASE 뒤 번호가 하나 건너뛰어도 오류가 아닙니다. 둘은 같은 ‘버전’으로 합칠 수 없습니다.

## 2. 두 파일의 역할과 불변 조건

`physical.log`는 DAT1 뒤에 32바이트 기록이 이어집니다. 내용 28바이트는 PAGE·형식·DATA/ERASE·사건 순번·PPN 또는 block·LPN·논리 version·자료 4바이트이고, 뒤 4바이트는 CRC32입니다. DATA를 재생하면 그 PPN의 현재 자료가 생기고 ERASE를 재생하면 한 블록의 3개 주소가 free가 됩니다.

`mapping.log`는 MAP1 뒤에 48바이트 WRITE/MOVE/TRIM 기록이 이어집니다. 현재 참조뿐 아니라 기대한 이전 `[version, PPN, incarnation]`을 함께 남깁니다. header를 포함한 44바이트에 CRC 4바이트를 붙입니다. `<`로 little endian을 지정하며 Python의 정수·bytes를 고정 크기로 바꿉니다.

이 파일들은 매체 상태를 재구성하는 자체 이력입니다. ERASE 기록을 붙였다고 파일의 과거 DATA bytes가 지워지는 것은 아닙니다. 실제 NAND의 전압·erase 단위·물리 지우기 명령은 없습니다. 파일은 각각 최대 65,536바이트, 번호와 version은 65,535까지인 교육 계약입니다. 로그 상한 때문에 모든 번호를 끝까지 쓸 수 있다는 뜻은 아닙니다.

복구 후 다음 조건을 확인합니다.

1. 현재 매핑의 PPN이 실제 재구성된 페이지에 있어야 합니다.
2. 그 페이지의 LPN·논리 version·incarnation이 매핑과 같아야 합니다.
3. 매핑이 가리킨 DATA CRC가 실제 기록 CRC와 같아야 합니다.
4. 서로 다른 live LPN이 같은 PPN을 동시에 소유하지 않아야 합니다.

최신 매핑이 틀렸을 때 옛 페이지를 검색해 임의로 정상값을 만드는 기능은 없습니다. 잘못된 참조는 명시적으로 거부합니다. CRC도 악의적인 metadata 변경을 막는 인증 수단은 아닙니다.

## 3. 수정 순서: 자료를 확인한 뒤 매핑을 게시합니다

새 PPN에 자료를 기록하고 다시 읽어 LPN·version·값을 확인한 뒤 WRITE 매핑을 추가합니다. 이전 PPN은 새 매핑 이후 stale이 될 뿐 즉시 지우지 않습니다. stale은 현재 매핑이 사용하지 않지만 아직 할당되어 있는 자료입니다. 전체 페이지 수는 `valid+stale+free=12`입니다.

```python
pages, _, _ = decode_physical(read_limited(root / "physical.log"))  # /는 Path 결합이며 파일의 물리 사건을 다시 읽습니다.
page = pages[ppn]  # []로 새 PPN에 기록된 자료를 고릅니다.
require((page["lpn"], page["version"], page["hex"]) == (lpn, version, value.lower()), "WRITE_READBACK_IDENTITY")  # tuple 비교로 주소·버전·값을 함께 확인합니다.
append_record(root, "mapping.log", mapping, "map", stage, cut)  # 자료 확인 뒤 매핑 기록을 추가합니다.
```

`def`는 함수를 정의하고 괄호는 인수를 전달합니다. `dict`는 PPN→자료, list는 LPN별 매핑을 저장합니다. `None`은 현재 참조가 없다는 값이고 `not in`은 해당 주소가 아직 할당되지 않았는지 확인합니다. 이 코드는 발췌이며 전체 소스에서는 입력·용량·기대 이전 token도 검사합니다.

초기에는 valid 3·stale 0·free 9입니다. 새 DATA가 온전히 남았지만 매핑은 아직 이전이면 valid 3·stale 1·free 8입니다. PPN1은 버려진 사본이며 응용 값은 아직11111111입니다. 매핑까지 완성하면 PPN1이 valid, PPN0이 stale이 되어 개수는 같아도 소유자가 달라집니다. 페이지 개수만 같다는 이유로 자료의 최신성까지 맞다고 판단하면 안 됩니다.

## 4. 잘못된 순서에서 실제로 관측한 것

| 의도한 오류 경로 | 명시 중단 위치 | 새 프로세스의 관측 |
| --- | --- | --- |
| publish-first | 매핑을 먼저 완성한 뒤 새 DATA 0바이트입니다. | 매핑은 PPN1·incarnation 4지만 페이지가 없어 MAPPED_PAGE_MISSING입니다. |
| erase-old-first | 이전 block을 먼저 ERASE하고 새 DATA 0바이트입니다. | 옛 PPN0이 사라져 기존 매핑도 MAPPED_PAGE_MISSING입니다. |
| wrong-page-identity | 새 DATA의 LPN을 1로 잘못 넣습니다. | 자료 CRC가 맞아도 WRITE_READBACK_IDENTITY로 매핑 게시를 막습니다. |

앞의 두 오류는 복구기가 잘못된 값을 정상처럼 반환하는 대신 참조를 거부한 결과입니다. 그래도 정상 쓰기 중단 계약인 ‘이전 상태를 읽을 수 있어야 함’을 만족하지 못합니다. availability 실패와 잘못된 값 반환을 구분합니다.

잘못된 LPN을 차단한 경우 이전 논리 값은 유지되지만 새 PPN은 stale 사본으로 남습니다. 사용한 물리 공간까지 되돌리는 원자적 작업은 아닙니다. 별도 손상 대조는 온전한 CRC를 가진 다른 LPN·다른 논리 version·다른 incarnation을 최신 매핑에 연결하고 PAGE_IDENTITY로 거부하는지도 확인합니다. 주소가 맞다는 것과 자료의 CRC가 맞다는 것은 다른 조건입니다.

## 5. 쓰기 경로의 82개 prefix

각 시험은 초기 파일을 새로 만들고, 선택한 기록의 앞 k바이트만 append한 자식을 종료 23으로 끝냅니다. 파일에는 flush·fsync 요청을 마친 prefix가 남으며 다음 새 프로세스가 두 파일을 처음부터 읽습니다.

| 중단 구간 | 열거 범위 | 기대한 논리 값·매핑 |
| --- | --- | --- |
| DATA 32바이트 | k=0~32, 33개 | 모두 이전 LPN0 값11111111·PPN0입니다. |
| 매핑 48바이트 | k=0~48, 49개 | k<48은 이전 값, k=48은 aaaa0001·PPN1입니다. |

DATA k=32는 새 자료만 완성돼 stale 1·free 8입니다. 매핑 k=47도 새 매핑이 부족하므로 이전 참조를 사용합니다. k=48에서만 논리 version 2가 됩니다. fixture의 DATA·매핑 전체 hex와 prefix bytes도 대조하므로 상태 값만 우연히 같은 경우와 구분합니다.

고정 기록보다 짧은 마지막 꼬리는 inspect에서 보류하지만, 완전한 CRC 오류는 거부합니다. 이후 write·GC는 TAIL_NEEDS_REPAIR로 멈춥니다. 복구는 읽기 전용이며 자동 truncation·checkpoint·저널 회전·재시도는 없습니다. 짧은 쓰레기가 잘린 기록처럼 보일 수도 있어 임의 손상 전체를 검출한다는 형식도 아닙니다.

## 6. 검증기의 실패와 실물 범위

최종 기본/-O는 같은 241개 검사·98개 중단 지점·409개 자식 호출로 PASS였습니다. 98개 중 쓰기 82개 외에 GC 12개·TRIM 4개가 포함됩니다. 다섯 의도적 구현 변이는 두 모드에서 모두 종료 1로 검출됐고 기존 출력 재사용은 2로 거부했습니다. 명령·소스 SHA·입력 경계·후속 GC 결과는 실행 기록에 있습니다.

자식은 동기화가 성공한 뒤 선택한 곳에서 끝납니다. 동기화 도중 고장·OS crash·directory fsync·NAND sector/page tearing·장치 cache·ECC·bad block·wear·실제 성능은 시험하지 않습니다. FTL의 논리 참조 계약을 호스트 파일로 실행한 결과를 실제 SSD의 정전 보장으로 바꾸지 않습니다.

## 확인 문제

1. 새 자료의 CRC가 맞으면 주소표부터 바꿔도 되나요? 아닙니다. 어느 LPN·논리 version·물리 incarnation의 자료인지와 기록 완료를 확인한 뒤 참조를 게시합니다.
2. DATA만 완성됐는데 값이 옛날 그대로이면 새 공간도 안 썼나요? 아닙니다. 미참조 사본이 stale 페이지로 남을 수 있습니다.
3. 잘못된 참조를 복구기가 거부하면 중단 처리가 성공한 것인가요? 이 시험의 정상 중단 계약은 이전 값이나 완성된 새 값을 복구하는 것입니다. MAPPED_PAGE_MISSING은 그 계약의 실패입니다.

## English

The file model separates three logical pages from twelve physical addresses. It verifies data identity before publishing a new reference and retains the old page until collection. A logical version differs from the physical incarnation used to distinguish address reuse. Publishing a map before data or erasing the old block first leaves a missing mapped page at the declared interruption. A correct reader rejects that reference; this is still a failed recovery contract. Eighty-two write prefixes retain the old mapping until the full new map record exists. These are actual host-file/process observations, not NAND or SSD power-loss validation.

## 읽은 판본과 범위

2026-10-21에 KIOXIA Managed Flash Background Operations Part 5, November 2023 Rev. 1.0의 pp. 1–3에서 L2P metadata·물리 위치 변경·자료 무결성·쓰기 증폭을 읽고 p.4 각주와 구분했습니다. 과거 문서의 UFS 최신판 표현을 현재 제품 정보로 옮기지 않았습니다. Part 4 GC, April 2023 Rev. 1.1a의 pp. 1–3도 연결했습니다. 자체 CRC·token·중단 형식은 직접 구성했습니다.
