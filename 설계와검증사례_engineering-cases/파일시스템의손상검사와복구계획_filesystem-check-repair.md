# 파일시스템의 손상 검사와 복구 계획 / Filesystem checks and copy repair

파일을 읽을 수 없을 때 이름, inode, 데이터 블록 중 어느 연결이 틀렸는지부터 나눠 봅니다. inode는 파일의 크기와 저장 위치 등을 담는 관리 레코드입니다. 디렉터리에는 이름과 inode 번호의 연결이 있습니다. 블록 bitmap은 어느 저장 구간을 쓰고 있는지 표시합니다. 각 부분이 혼자 읽힌다는 사실과 서로 일치한다는 사실은 다릅니다. 실제 ext4의 관계는 [inode 문서](https://docs.kernel.org/filesystems/ext4/inodes.html)에서 확인할 수 있습니다.

[실행 코드와 fixture](../예제_examples/실무검증_practical-validation/filesystem_repair/README.md) · [파일 이름과 블록 소유권](파일이름과블록소유권의복구_filesystem-orphans-block-ownership.md) · [실행 기록](검증기록_evidence/파일시스템이미지검사와복구_20261021.md)

## 작게 만든 이미지의 계약

실행 대상은 새 호스트 파일에 기록한 자체 EDUFS1 JSON입니다. super에는 8바이트 데이터 블록 8개를, inode에는 종류·길이·블록 순서·이름 참조 수를 기록합니다. root 1, lost+found 2, 일반 파일 3·4·5, reports 디렉터리 6을 둡니다. 디렉터리와 inode는 JSON metadata에 별도로 저장합니다. 실제 ext4 block group이나 디렉터리 데이터 블록 배치를 구현한 형식은 아닙니다. 실제 [superblock 원문](https://docs.kernel.org/filesystems/ext4/super.html)은 전체 개수·기능·유지 관리 정보의 역할을 설명합니다.

| 파일 inode | 연결된 이름 | 블록 목록 | 논리 내용 |
| --- | --- | --- | --- |
| 3 | /config.bin | [0, 1] | `GAIN=1.25\n`, 10바이트입니다. |
| 4 | /reports/readme.txt | [2] | `OK\n`, 3바이트입니다. |
| 5 | /archive.bin | [3] | `ORPHAN\n`, 7바이트입니다. |

파일 3의 블록 수는 `ceil(10/8)=2`입니다. 16바이트를 배정하고 10바이트를 사용하므로 6바이트가 padding입니다. 세 파일의 논리 길이는 `10+3+7=20`, 데이터 블록 할당량은 `4×8=32`바이트입니다. 전체 데이터 용량 64바이트 중 32바이트가 비어 있습니다. JSON seed 파일 자체는 metadata와 16진수 표기까지 포함해 1,673바이트입니다. 두 용량을 혼동하지 않습니다.

```python
def needed_blocks(size):  # def는 size를 받는 함수를 정의합니다.
    return (size + 7) // 8  # //는 정수 몫이며 8바이트 단위로 올림합니다.
```

이 식은 크기가 0·3·7·10·64일 때 각각 0·1·1·2·8을 반환합니다. 이 형식은 sparse file과 미리 배정한 여유 블록을 지원하지 않으므로 실제 블록 목록 길이도 이 값과 같아야 합니다. 실제 ext4의 i_blocks 단위와 기능별 해석은 별도 규칙입니다.

## checksum이 맞아도 연결이 틀릴 수 있습니다

metadata_damage/image.json에는 다음 네 가지를 함께 넣었습니다. reports에 없는 inode 31을 가리키는 ghost.txt를 추가하고, 파일 3의 size를 10에서 19로, nlink를 1에서 7로 바꿉니다. bitmap에서는 사용 중인 블록 1을 뺍니다. 의미상 오류를 검사하려고 이미지 checksum을 다시 계산했습니다. 통신 중 무작위 비트가 바뀐 것과 구분한 합성 입력입니다.

검사기는 DANGLING_ENTRY, SIZE_CAPACITY, NLINK, BITMAP_MISSING을 각각 보고했습니다. 19바이트는 주어진 두 블록의 용량 16바이트를 넘습니다. 그러나 이 사실만으로 원래 길이가 10이었다고 추론할 수는 없습니다. 16바이트로 잘라 맞추면 원래 없던 padding까지 파일 내용에 포함할 수 있습니다.

```python
capacity = len(inode["blocks"]) * 8  # []로 블록 목록을 읽고 배정 용량을 계산합니다.
inode["size"] = capacity  # 길이 근거 없이 용량으로 바꾸는 의도한 잘못된 처리입니다.
```

guess-size 변이는 신뢰할 목록이 없는 입력에서 이 처리를 계획합니다. 정상 정책은 REFUSED이고 변이는 READY여서 검증기가 차이를 검출했습니다. 선언 길이가 잘못돼도 저장된 바이트에 후보 원문이 남아 있고 외부 manifest의 길이·digest와 일치하면 set_size를 계획할 수 있습니다. 여기서는 원래 길이 10과 그 10바이트의 SHA가 근거입니다. SHA만으로 사라진 바이트를 다시 만들지는 않습니다.

ext4도 [metadata checksum의 대상](https://docs.kernel.org/filesystems/ext4/checksums.html)을 구조별로 구분합니다. 이 예제는 자체 SHA-256 방식을 쓰며, 현재 구조의 checksum 통과와 원래 응용 자료의 동일성을 따로 검사합니다.

## 읽기 전용 계획을 사본에 적용합니다

plan은 이미지를 변경하지 않고 이미지·manifest의 실제 파일 SHA와 동작 목록을 반환합니다. 이 입력에서 고정 기대값은 다음 순서입니다.

| 동작 | 결정한 근거 |
| --- | --- |
| ghost.txt→31 항목을 제거합니다. | inode 31이 존재하지 않습니다. 대상 파일이나 원래 이름을 복원한 것은 아닙니다. |
| inode 3의 size를 10으로 바꿉니다. | 10바이트 후보가 외부 길이·내용 digest와 맞습니다. |
| inode 3의 nlink를 1로 바꿉니다. | 남아 있는 이름 참조를 다시 세었습니다. |
| bitmap을 [0,1,2,3]으로 맞춥니다. | 네 블록의 고유한 파일 소유권이 확인됐습니다. |

이 정책에서는 root nlink를 1로 고정하고 나머지는 이름 참조 수로 셉니다. `.`·`..`를 포함한 실제 Unix 디렉터리 링크 수 규칙은 구현하지 않습니다. bitmap에 사용 중 블록이 빠진 경우를 고치지만, 할당 표시만 있고 소유자가 없는 블록은 별도로 거부합니다. 그 비트가 단순 누수인지 inode가 사라진 파일의 흔적인지 알 수 없기 때문입니다. 실제 bitmap의 의미는 [ext4 bitmap 문서](https://docs.kernel.org/filesystems/ext4/bitmaps.html)에서 기능 조건과 함께 읽습니다.

repair는 지금 읽은 이미지와 manifest로 계획을 다시 계산합니다. 제출한 계획이 다르거나 입력 SHA가 달라졌으면 STALE_OR_MODIFIED_PLAN입니다. 계획의 동작도 먼저 메모리 사본에 적용해 후속 검사를 합니다. 그 뒤 `xb`로 새로운 출력 파일만 만듭니다. 원본과 같은 경로·기존 출력 파일은 거부하며, 자식 실행마다 원본 SHA가 그대로인지 대조합니다.

metadata 복구 결과는 seed와 전체 bytes·SHA가 같았습니다. 세 파일의 내용도 구현의 encoder/decoder 왕복 대신 fixture의 직접 정한 16진수와 비교했습니다. 복구 사본의 두 번째 계획은 빈 목록이고, 다시 만든 사본도 bytes가 같았습니다. 이 멱등성은 같은 복구를 되풀이해 추가로 내용을 바꾸지 않는다는 뜻입니다. 사라진 내용까지 알아냈다는 증거는 아닙니다.

## 실행과 실패 판정

코드 폴더에서 새 경로를 선택합니다.

```powershell
python -X utf8 -B verify.py --output C:/temp/fs-normal-new
python -X utf8 -B -O verify.py --output C:/temp/fs-optimized-new
python -X utf8 -B -O verify.py --mutation guess-size --output C:/temp/fs-size-new
```

최종 정상 두 실행은 각각 이미지 사례 30개·대조 215개·새 자식 63개에서 PASS·종료 0입니다. 네 변이를 기본/-O로 실행한 여덟 검증은 모두 의도한 불일치로 종료 1입니다. `raise`로 계약 위반을 처리하므로 최적화 시 생략되는 assert에 의존하지 않습니다.

CHECKED·종료 0은 검사 명령의 정상 처리를 뜻합니다. 구조 결과 FAIL이나 계획 REFUSED도 정상적인 분석 결과입니다. 잘못된 JSON, checksum, bool을 정수로 쓴 크기, 범위 밖 블록, 미지원 기능 등은 REJECTED·종료 3입니다. 기존 검증 출력 폴더 재사용은 종료 2로 차단됐고 results.json SHA가 보존됐습니다.

실제 [e2fsck 매뉴얼](https://man7.org/linux/man-pages/man8/e2fsck.8.html)은 검사·수정 상태를 더 다양한 종료 비트로 나타냅니다. 이 실습은 e2fsck나 mount를 실행하지 않으며 실제 저장장치 복구 절차를 대신하지 않습니다. 새 파일의 flush·fsync 호출로 전원 차단, 동시 writer, 디렉터리 내구성이나 원래 사용자 자료 복구를 검증한 것으로 확대하지 않습니다.

## 확인 문제

1. 10바이트 파일에 8바이트 블록 두 개가 필요한 이유는 무엇입니까? 나머지 6바이트도 논리 파일 내용입니까?
2. size 19와 용량 16의 불일치를 찾았다면 size를 16으로 바꿔도 됩니까?
3. 복구 후 구조 PASS와 두 번째 복구의 동일한 SHA만으로 원래 자료를 되찾았다고 말할 수 있습니까?

답: 1. 한 블록에 들어가지 않으므로 두 개를 쓰며, size 뒤 padding은 논리 내용에서 제외합니다. 2. 이 실습은 원래 길이를 모르면 거부합니다. 용량은 원래 길이의 증거가 아닙니다. 3. 구조와 처리의 고정점만 확인한 것입니다. 원래 자료의 길이·내용 등 별도의 신뢰할 근거가 필요합니다.

## English

The EDUFS1 fixture separates names, inode records, block ownership and allocation bits in a bounded JSON host file. Four simultaneous metadata faults produce four distinct findings. An external size/digest reference allows the ten-byte candidate to be selected; allocated capacity alone does not justify a new length. A read-only plan binds exact input hashes and actions. Applying it to a new copy restores the seed bytes and all three fixed payloads, and a second repair is idempotent. Both normal and optimized runs pass 215 comparisons in 30 cases with 63 children each; four deliberate mutations fail in both modes. These observations establish this educational contract, without executing ext4, e2fsck, mounted-device repair or power-loss testing.

## 출처

Linux Kernel의 inode·bitmap·checksum 온라인 원문과 e2fsprogs 1.47.4 e2fsck 매뉴얼의 DESCRIPTION·-n/-p/-y·EXIT CODE를 2026-10-21에 읽었습니다. 원문 링크는 해당 개념 옆에 두었습니다. Kernel 문서는 열람한 온라인 snapshot이며 설치된 커널 버전을 뜻하지 않습니다. 자체 geometry·SHA·복구 정책은 이 사례에서 정한 내용입니다.
