# FTL의 GC와 폐기된 주소 재사용 / FTL garbage collection, TRIM and address reuse

GC가 예전 페이지를 복사하는 동안 같은 논리 주소에 새 자료가 쓰였다면 어느 값을 남겨야 할까요? 복사된 bytes의 CRC만 확인하면 옛 자료로 매핑을 되돌릴 수 있습니다. 이 사례는 GC 시작 당시의 논리 version·물리 주소·incarnation을 비교하고, TRIM 뒤 재사용된 PPN까지 구분합니다. 실제 SSD나 NAND를 실행하지 않은 호스트 파일 모델입니다.

[코드·고정 입력](../예제_examples/실무검증_practical-validation/ftl_mapping/README.md) · [매핑 게시 사례](FTL의매핑게시와전원중단_ftl-map-publication.md) · [실행 기록](검증기록_evidence/FTL매핑과GC중단검사_20261021.md)

## 1. GC는 현재 살아 있는 자료를 남겨야 합니다

GC는 garbage collection, 더 이상 참조하지 않는 자료가 차지한 공간을 회수하는 과정입니다. 여기서 valid는 현재 매핑이 가리키는 페이지, stale은 할당됐지만 더 이상 참조하지 않는 페이지, free는 다음 DATA에 쓸 수 있는 주소입니다. 이 셋의 합은 12입니다. stale 자료가 파일에 남아 있다는 사실과 응용이 그 자료를 읽어도 된다는 사실은 다릅니다.

erase block은 3페이지입니다. 블록에 live 자료가 있으면 이를 victim 밖의 빈 페이지로 복사하고 새 위치를 게시한 뒤 블록을 비웁니다. KIOXIA의 GC 기술 문서는 valid/invalid를 구분하고 필요한 자료를 이동한 뒤 block을 지우는 순서, 이동량이 생기는 비용을 설명합니다. 자체 victim 선택·token·CRC 형식이 해당 제품의 firmware와 같다는 뜻은 아닙니다. [KIOXIA GC, April 2023 Rev. 1.1a, pp. 1–3](https://www.kioxia.com/content/dam/kioxia/shared/business/memory/mlc-nand/asset/productbrief/KIOXIA_Understanding_Garbage_Collection_Tech_Brief.pdf)

초기 block 0에는 LPN0의 PPN0만 live이고 PPN1·2는 free입니다. plan-gc는 `[논리 version1, PPN0, incarnation1]`과 자료11111111을 ticket 파일에 남깁니다. finish-gc는 새 프로세스에서 현재 token이 같은지 확인하고 PPN4·incarnation 4로 옮긴 뒤 block 0을 ERASE합니다. LPN0의 값과 논리 version은 그대로이며 물리 참조만 바뀝니다.

## 2. CRC가 맞는 옛 사본도 최신 자료는 아닙니다

| 순서 | 논리·물리 상태 |
| --- | --- |
| GC snapshot을 잡습니다. | LPN0→PPN0·version 1·incarnation 1입니다. |
| host가 LPN0에 aaaa0001을 씁니다. | LPN0→PPN1·version 2·incarnation 4입니다. |
| 예전 GC가 완료를 시도합니다. | snapshot token과 현재 token이 달라 STALE_GC_SNAPSHOT입니다. |

정상 경로는 거부 전에 두 파일을 바꾸지 않는지도 확인합니다. bytes11111111의 CRC가 여전히 맞더라도 그것은 version 1의 값입니다. 비교할 기준은 자료 내부의 일관성뿐 아니라 현재 논리 주소의 소유권입니다.

```python
if mutation != "stale-gc":  # !=는 차이 비교이며 정상 경로에서 token 검사를 실행합니다.
    require(item["token"] == token(state, lpn), "STALE_GC_SNAPSHOT")  # []로 읽은 snapshot과 현재 참조를 비교합니다.
source = state["pages"].get(ppn)  # get은 원본 PPN이 없으면 None을 반환합니다.
```

전체 함수는 원본의 LPN·version·incarnation·자료·CRC와 victim 소속도 검사합니다. `stale-gc` 변이는 기록할 때와 매핑 저널을 재생할 때 모두 MOVE의 이전 token 검사를 무시합니다. 그 잘못된 경로를 실행하면 새 aaaa0001 대신11111111·version 1이 다시 보입니다. 같은 파일을 정상 복구기로 읽으면 MAP_BASE_CHANGED로 거부합니다. 잘못된 writer만 있어도 정상 reader가 무조건 옛 값을 공개한다는 주장은 아닙니다.

## 3. GC 전체의 원자성은 별도입니다

다른 일정에서는 snapshot 뒤 LPN1의 새 페이지가 victim block 0의 PPN1에 생깁니다. LPN0 token은 변하지 않아 GC가 LPN0을 PPN4로 옮기는 MOVE는 게시할 수 있습니다. 마지막 erase에서 LPN1이 block 0에 남은 것을 확인하고 ERASE_LIVE_BLOCK으로 거부합니다.

실제 결과는 LPN0→PPN4·LPN1→PPN1·LPN2→PPN6, 값11111111·bbbb0002·33333333입니다. 논리 값은 유지되지만 이미 게시한 MOVE를 원래 위치로 되돌리지 않습니다. valid 3·stale 2·free 7이고 DATA 사건과 매핑은 각각 5개입니다. 성공/실패 반환만으로 모든 파일 효과가 되돌려졌다고 판단하면 안 됩니다.

이 모델은 단일 프로세스 안의 임의 동시 실행을 돌리지 않습니다. plan과 완료 사이의 host 사건을 실제 별도 프로세스로 배치한 결정적 일정입니다. snapshot의 안전성, 최종 live 검사, GC 전체 transaction의 원자성을 서로 구분합니다.

## 4. 임시 공간과 재기록 비용을 계산합니다

여섯 host write를 LPN0·1·2에 두 번씩 보내면 valid 3·stale 6·free 3이 됩니다. block 0에는 live1·stale 2가 있습니다. GC는 free 하나에 live 자료를 복사한 뒤 block 0의 3페이지를 비워 free가 3→5로 늘어납니다. 순증은 `3−1=2`입니다.

| 비교 | GC 전 | GC 후 |
| --- | ---: | ---: |
| valid | 3 | 3 |
| stale | 6 | 4 |
| free | 3 | 5 |
| LPN0의 PPN·incarnation | 2·5 | 9·10 |
| LPN0·1·2의 논리 version | 3·3·3 | 3·3·3 |

seed를 제외한 host 자료는 6페이지×4바이트=24바이트입니다. GC 복사 1페이지를 더한 자료 기록은 7페이지×4바이트=28바이트라 이 구간의 자료 재기록 비는 `28/24=7/6≈1.167`입니다. metadata·ERASE 기록·ECC·NAND 내부 동작을 제외한 자체 예제입니다. 실제 SSD WAF·속도·수명을 측정한 값은 아닙니다. [KIOXIA L2P 문서의 쓰기 증폭 설명, pp. 3](https://europe.kioxia.com/content/dam/kioxia/shared/business/memory/ufs/asset/productbrief/KIOXIA_Understanding_Logical_Block_Address_Tech_Brief.pdf)

빈 페이지 수만으로 아무 victim이나 처리할 수 있는 것도 아닙니다. 별도 부하에서는 free가 PPN11 하나이고 victim block 3의 live는 PPN10입니다. 빈 공간이 같은 victim 안에 있어 외부 복사 공간은 0이고 NO_GC_TEMP_SPACE입니다. 일반 쓰기는 free 하나를 남기는 정책으로 GC_RESERVE_REQUIRED를 반환합니다. 다른 stale-only block 0을 회수하면 free 4가 됩니다. 한 페이지 reserve는 모든 victim의 처리 가능성이나 무한한 진척을 보장하지 않습니다.

## 5. TRIM tombstone과 물리 주소의 재사용

TRIM은 이 모델에서 ‘해당 LPN의 매핑이 없다’는 tombstone을 매핑 저널에 추가합니다. tombstone은 삭제 사실을 재시작 뒤에도 기억하는 표식입니다. LPN0을 TRIM하면 논리 version 2·참조None이 되고 읽기 결과도None입니다. 원래 PPN0의 bytes는 아직 물리 이력에 있습니다.

| 순서 | 확인한 상태 |
| --- | --- |
| TRIM 전에 GC snapshot을 잡습니다. | LPN0→PPN0·version 1·incarnation 1입니다. |
| LPN0을 TRIM합니다. | LPN0은None·version 2입니다. |
| live가 없는 block 0을 ERASE합니다. | PPN0을 다시 할당할 수 있습니다. ERASE 사건 번호는 4입니다. |
| LPN1을 새로 씁니다. | PPN0을 incarnation 5·LPN1 version 2로 사용합니다. |
| 옛 GC ticket으로 완료를 시도합니다. | STALE_GC_SNAPSHOT이며 새 자료와 파일을 바꾸지 않습니다. |

PPN 숫자 0이 같아도 incarnation 1의 LPN0과 incarnation 5의 LPN1은 다릅니다. 현재 매핑·논리 version·물리 세대가 모두 필요한 이유입니다. 다른 부하 trace에서도 TRIM·회수 뒤 PPN0을 LPN2 incarnation 13에 재사용했고 LPN0은None으로 유지했습니다.

`ignore-trim` 변이는 확정된 tombstone을 저널 재생에서 무시합니다. 같은 파일에서11111111이 다시 보이므로 None 리터럴과 다릅니다. 정상 reader는 tombstone을 보존합니다. 파일의 DATA를 훑어 가장 커 보이는 번호의 자료로 매핑을 다시 만드는 정책도 TRIM 기록을 잃으면 같은 종류의 오류를 만들 수 있습니다. 이 코드는 그런 자동 재구성을 하지 않습니다.

실제 deallocate 뒤 읽기 동작은 장치·기능 조건을 확인해야 합니다. NVMe1.4c의 DLFEAT에는 보고하지 않음·0·FF 동작이 구분되어 있고, 오류 보고 설정도 별도입니다. 이 예제의 None을 NVMe나 ATA의 반환 규칙으로 바꾸지 않습니다. TRIM은 secure erase의 시험도 아닙니다. 특히 이 모델의 append 이력은 ERASE 뒤에도 옛 bytes를 파일에 남깁니다. [NVMe Base1.4c Figure249·§6.7.1.1](https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf)

## 6. GC·TRIM 중단 지점과 범위

초기 live1의 GC에서 DATA 32·MOVE 48·ERASE 32 각각 prefix0·1·N−1·N을 선택한 12개 중단 지점을 실행했습니다. 복사 DATA만 남으면 새 사본은 stale이고 옛 매핑을 읽습니다. MOVE가 온전히 남으면 새 위치를 읽으며, ERASE가 부족해도 원본 block이 남아 있습니다. ERASE 32바이트가 완성되면 옛 block만 free가 됩니다. TRIM 매핑 prefix0·1·47·48의 4개도 비교해 완성된 tombstone에서만None이 되는 것을 확인했습니다.

새 프로세스의 inspect는 partial tail을 보류할 뿐 파일을 잘라내지 않습니다. 이후 write·GC는 TAIL_NEEDS_REPAIR로 거부합니다. 자동 재개·orphan 정리·checkpoint·로그 회전은 구현하지 않습니다. 복사 도중 중단이 논리 값을 보존해도 물리 공간이 일부 소모될 수 있습니다.

모든 중단은 선택 prefix를 실제 파일에 flush·fsync한 뒤 자식을 종료 23으로 끝내는 시험입니다. OS나 장치 전원을 끄지 않습니다. 전체 정상/-O의 241개 비교·98개 cut·409개 자식과 5개 변이의 검출 결과는 실행 기록에 있습니다. 파일 이력을 NAND program 횟수·물리 마모·장치 정전 내구성으로 해석하지 않습니다.

## 확인 문제

1. GC 사본의 CRC가 맞으면 새 매핑을 무조건 게시해도 되나요? 아닙니다. snapshot의 version·PPN·incarnation이 현재 매핑과 같은지 확인합니다.
2. free가 하나면 live 하나인 어떤 victim도 회수할 수 있나요? 아닙니다. 임시 페이지가 victim 밖에 있어야 합니다.
3. TRIM 뒤 같은 PPN을 다른 LPN에 썼다면 예전 GC ticket을 적용해도 되나요? 안 됩니다. 숫자가 같은 주소라도 논리/물리 세대와 소유자가 달라졌습니다.

## English

GC captures a logical/physical token, verifies it again, copies live data outside the victim, publishes MOVE and checks that no current reference remains before ERASE. An intentionally unguarded writer and replay path can replace a newer host value with an older valid-CRC copy. A separate schedule publishes one MOVE and then rejects erase because another live page entered the victim; the entire GC is not atomic.

Six host data writes plus one relocation yield a declared data-only ratio 7/6, excluding metadata and physical NAND effects. Free space must be outside the victim. TRIM records an unmapped tombstone; reusing PPN0 with a different incarnation cannot authorize an older ticket. None is a teaching policy, not universal device read-zero behavior or secure erasure. Selected file-prefix interruptions test this bounded model without NAND, SSD or actual power-loss execution.

## 읽은 판본과 범위

KIOXIA Part 4 GC, April 2023 Rev. 1.1a pp. 1–3와 Part 5 L2P, November 2023 Rev. 1.0 pp. 1–3를 2026-10-21에 읽었습니다. NVMe Base 1.4c는 표지 2021-03-09, Figure 249의 DLFEAT와 §6.7 Deallocate/§6.7.1.1을 읽었으며 전체 407쪽 구현을 주장하지 않습니다. Micron 전원 보호 PDF는 접근 거부되어 읽은 출처에 포함하지 않았습니다.
