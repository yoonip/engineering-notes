# 파일 이름과 블록 소유권의 복구 / Recovering names and block ownership

폴더에서 이름이 사라져도 inode와 데이터가 남을 수 있습니다. 반대로 이름이 보이고 구조 검사가 통과해도 원래 내용이 사라졌을 수 있습니다. 복구 결과를 판단할 때 이름의 연결, 저장 구간의 소유 관계, 논리 내용의 동일성을 따로 확인해야 하는 이유입니다.

[코드와 입력](../예제_examples/실무검증_practical-validation/filesystem_repair/README.md) · [검사와 사본 복구 절차](파일시스템의손상검사와복구계획_filesystem-check-repair.md) · [실행 기록](검증기록_evidence/파일시스템이미지검사와복구_20261021.md)

## 이름에서 내용까지 두 관계를 따라갑니다

EDUFS1의 directory entry는 이름과 inode 번호의 쌍입니다. inode의 blocks는 내용이 놓인 데이터 블록 번호의 순서입니다. 예를 들어 /config.bin→inode 3→블록 [0,1]을 따라가고 size 10만큼 읽으면 `GAIN=1.25\n`이 됩니다. 여기서 소유권은 어느 inode가 데이터 블록을 참조하느냐를 뜻합니다. 사용자 UID나 접근 권한을 뜻하지 않습니다.

검사기는 root inode 1에서 이름 연결을 따라가며 도달 가능한 inode를 모읍니다. 목록에 있는 전체 inode와 이 집합을 비교하면 이름을 잃은 후보가 나옵니다. 한편 각 파일의 블록 목록을 거꾸로 모아 `블록 번호→inode 집합`을 만듭니다. 두 관계를 따로 만들어야 정상 hard link와 잘못된 공유 블록을 구분할 수 있습니다. 실제 이름과 inode의 관계는 [ext4 directory 원문](https://docs.kernel.org/filesystems/ext4/directory.html)에서 확인할 수 있습니다.

| 관계 | 이 형식의 판정 |
| --- | --- |
| 두 이름→같은 파일 inode 3→블록 0 | 유효한 hard link입니다. nlink는 2, 블록 0의 소유자는 [3]입니다. |
| 서로 다른 파일 inode 3·4→같은 블록 0 | SHARED_BLOCK입니다. 블록 소유자는 [3,4]이며 자동 수정을 거부합니다. |
| 이름 경로 없음→남아 있는 파일 inode 5→고유 블록 3 | 일반 파일 orphan이며 조건이 맞으면 새 이름으로 연결합니다. |
| 할당 bitmap의 6→참조 inode 없음 | UNOWNED_ALLOCATED이며 파일 이름·순서를 추정하지 않습니다. |

블록을 두 번 세지 않으려고 `set`을 사용합니다. 같은 inode를 여러 이름으로 참조해도 서로 다른 소유자 두 개가 생기는 것은 아닙니다. 실제 파일시스템의 reflink나 공유 블록 기능을 지원하지 않는 자체 형식의 정책입니다. 알려지지 않은 기능을 기존 규칙으로 해석하지 않도록 super의 features가 비어 있지 않으면 거부합니다.

```python
owners = {}  # {}는 블록 번호와 inode 집합을 저장할 사전입니다.
for number, blocks in [(3, [0, 1]), (4, [0])]:  # for는 두 파일의 목록을 차례로 읽습니다.
    for block in blocks:  # 안쪽 반복문은 각 데이터 블록을 읽습니다.
        owners.setdefault(block, set()).add(number)  # 없으면 집합을 만들고 소유 inode를 추가합니다.
```

이 작은 입력의 owners[0]은 {3,4}입니다. 현재 블록을 다른 빈 블록에 복사하면 참조 충돌을 없앨 수는 있어도, inode 4의 원래 내용이 현재 블록 0에 있었다는 증거는 생기지 않습니다. 이 예제는 어느 파일의 내용을 채택할지 자동으로 결정하지 않습니다. ignore-shared 변이는 이런 충돌을 보고하지 않아 실제 SHARED_BLOCK 기대값과 대조할 때 실패했습니다.

## orphan의 내용과 원래 이름은 별도입니다

orphan_file/image.json에서는 root의 archive.bin→5 항목을 제거하고 inode 5의 이름 참조 수를 0으로 바꿨습니다. inode 5에는 size 7, blocks [3]이 남아 있고 블록 3에는 `ORPHAN\n`과 padding 한 바이트가 있습니다. 루트에서 도달 가능한 inode는 1·2·3·4·6이고, 차집합은 [5]입니다.

고유한 블록을 가진 정상 길이의 일반 파일이므로 계획은 lost+found inode 2에 inode_5→5를 추가하고 nlink를 1로 바꿉니다. 사본의 새 경로는 /lost+found/inode_5입니다. 원래 경로 /archive.bin은 되살아나지 않았습니다. manifest에도 이름은 없기 때문에 새 이름은 이 정책이 부여한 식별자일 뿐입니다.

새 사본의 inode 5 내용은 고정 기대값 `4f525048414e0a`, 즉 `ORPHAN\n`과 같았습니다. 모든 물리 블록 레코드도 주입 전과 같았습니다. 검증기는 fixture에 알고 있는 원문을 직접 비교할 수 있습니다. 그러나 manifest를 주지 않고 사용자 입장에서 검사하면 identity는 NOT_ESTABLISHED입니다. 외부 목록을 주었을 때 세 파일의 길이·digest가 모두 맞아 VERIFIED가 됐습니다. 실험자가 알고 있는 답과 이미지 자체가 제공하는 증거를 구분한 결과입니다.

drop-orphan 변이는 orphan inode를 삭제하고 bitmap에서 블록 3을 빼는 계획을 냅니다. 사후 구조만 맞출 수 있는 잘못된 결정이므로 검증기는 계획 단계에서부터 새 이름 연결의 고정 동작과 비교해 멈춥니다. 이 대조에서 실제 원본 파일을 지우거나 변이 계획을 디스크에 적용하지 않습니다.

ext4의 [orphan 추적](https://docs.kernel.org/filesystems/ext4/orphan.html)은 열려 있지만 unlink된 파일, truncate/extend 정리 등 정상적인 상황도 다룹니다. 이 글의 “root에서 도달할 수 없는 inode 후보”를 실제 ext4의 모든 orphan 목록과 동일하게 취급하지 않습니다.

## 디렉터리 그래프에서는 임의로 선을 끊지 않습니다

directory_cycle 입력에는 reports inode 6에서 root 1로 돌아가는 back 항목을 넣었습니다. 1→6→1은 순환입니다. 단순 재귀만 쓰면 끝없이 같은 경로를 따라갈 수 있습니다. 검사기는 방문 중인 노드와 방문을 끝낸 노드를 구분하며, 아직 방문 중인 노드로 돌아오는 간선을 DIRECTORY_CYCLE로 보고합니다.

서로 다른 두 디렉터리가 reports inode 6을 가리키는 입력도 있습니다. 이 형식에서 디렉터리는 root 이외에 부모 하나만 가지므로 DIRECTORY_PARENT_COUNT입니다. 이름이 끊긴 reports 디렉터리와 그 안의 파일도 별도 입력으로 만들었습니다. 일반 파일만 새 이름으로 연결하면 하위 경로 관계를 바꿀 수 있으므로 ORPHAN_DIRECTORY에서 자동 수정을 거부합니다. 중복된 이름이 다른 inode를 가리키는 경우도 어느 항목이 원래인지 고르지 않습니다.

이 정책은 일반 파일 hard link를 허용하되 디렉터리 hard link, `.`·`..`, symlink, mount 경계를 구현하지 않는 작은 그래프 계약입니다. root nlink=1과 나머지 이름 참조 수 역시 자체 규칙입니다. 실제 inode의 링크 수·블록 위치 해석은 [ext4 inode 원문](https://docs.kernel.org/filesystems/ext4/inodes.html)을 따로 읽어야 합니다.

## 구조가 일치해도 잃은 자료가 있습니다

resealed_changed_payload 입력에서는 파일 4의 `OK\n`을 같은 길이의 `NO\n`으로 바꾸고 블록·이미지 checksum을 모두 다시 계산했습니다. 경로·크기·소유권·bitmap은 맞으므로 structural PASS입니다. 외부 자료가 없으면 identity NOT_ESTABLISHED, 원래 `OK\n`의 digest를 주면 identity FAIL입니다. skip-digest 변이는 이를 VERIFIED라고 표시해 검증기에서 실패했습니다.

missing_inode_and_payload 입력은 inode 5, 그 이름과 할당 비트를 없애고 블록 3을 0으로 덮었습니다. 현재 남아 있는 파일만 보면 구조 PASS입니다. 그러나 외부 목록에는 inode 5가 있어 MISSING_FILE이 나옵니다. 내용 사본이 없으므로 계획은 REFUSED입니다. 이때 metadata의 연결을 새로 만들어도 `ORPHAN\n`이 다시 생기지는 않습니다.

또 다른 입력은 블록 6에 `LOSTDATA`를 두고 할당 표시만 남깁니다. 어느 inode의 몇 번째 블록인지, 유효한 파일의 일부였는지 알 수 없어 자동 해제·이름 부여를 하지 않습니다. 남은 바이트를 보존하는 것과 그 바이트의 파일 정체를 아는 것은 각각 확인할 사실입니다. 실제 복구에서는 별도의 백업·응용 형식·기록 등 추가 근거가 필요할 수 있지만 여기서는 그런 자료를 만들어 넣지 않았습니다.

길이도 내용 검증의 일부입니다. 선언 size 64와 manifest size 64에 실제 블록 하나의 8바이트 digest를 주어도 전체 64바이트가 존재하지 않습니다. 길이를 먼저 확인해 MISSING_PAYLOAD_BYTES로 분류합니다. 짧은 데이터를 hash한 값과 같다는 이유로 긴 파일을 VERIFIED로 표시하지 않습니다.

## 실행과 관측

```powershell
python -X utf8 -B verify.py --output C:/temp/fs-normal-new
python -X utf8 -B -O verify.py --mutation ignore-shared --output C:/temp/fs-shared-new
python -X utf8 -B -O verify.py --mutation drop-orphan --output C:/temp/fs-orphan-new
python -X utf8 -B -O verify.py --mutation skip-digest --output C:/temp/fs-digest-new
```

정상/-O는 각각 30개 이미지 사례·215개 대조·63개 자식에서 PASS입니다. 공유 블록·잘못된 길이 추정·orphan 삭제·digest 생략 변이는 기본/-O에서 모두 검출됐습니다. 검증기의 고정 바이트·소유권 목록·계획 기대값은 검사 대상의 검사 함수를 호출해서 생성하지 않습니다. 실제 파일을 새 프로세스로 읽은 결과와 독립 대조합니다.

## 확인 문제

1. 이름 두 개가 inode 하나를 가리킬 때와 inode 두 개가 블록 하나를 가리킬 때 차이는 무엇입니까?
2. /lost+found/inode_5에서 올바른 내용이 나왔다면 원래 파일 이름도 복원된 것입니까?
3. 원래 inode·이름·자료를 함께 지운 이미지가 구조 PASS라면 복구 성공입니까?

답: 1. 전자는 같은 파일에 붙은 hard link이고 후자는 이 형식이 금지한 데이터 블록 충돌입니다. 2. 새 식별자로 연결한 것입니다. 이름 근거가 따로 없으므로 옛 이름은 모릅니다. 3. 현재 구조가 일치할 뿐입니다. 외부 목록으로 누락을 찾을 수 있어도 payload 사본이 없으면 원문을 되살리지 못합니다.

## English

Names point to inode records, while inode block lists establish data ownership. Two names for one file inode are valid hard links; two distinct file inodes claiming block zero are refused. An unreachable regular inode with intact unique blocks can be linked under a new salvage name, without recovering its historical name. Directory cycles, multiple parents and orphan subtrees are refused rather than arbitrarily edited. Recomputed checksums permit a consistent image to contain different historical content. An external size/digest inventory detects changed or missing files, but supplies neither the old names nor missing payload bytes. Literal owners, salvage actions and payloads are checked against actual files. This is a bounded educational graph contract, separate from ext4 orphan processing and real filesystem recovery.

## 출처

ext4 Directory Entries 도입부·§4.3.1, Index Nodes 도입부·i_links_count/i_block, Orphan file 본문을 2026-10-21에 읽었습니다. 원문 링크는 관련 절에 연결했습니다. 일반 파일의 hard link 관계는 원문에서 확인한 개념이며 8바이트 geometry·공유 금지·자동 복구 거부 정책은 자체 실습 규칙입니다.
