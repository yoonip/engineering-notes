# 파일시스템 이미지 검사와 사본 복구 / Filesystem image checks and copy repair

EDUFS1이라는 작은 자체 JSON 이미지를 새 호스트 파일로 만들고, 별도 Python 프로세스에서 검사·계획·사본 복구를 실행합니다. 원본 이미지를 덮어쓰지 않습니다. 실제 ext4 형식, raw disk, mount, e2fsck, 사용자 파일이나 장치 전원 차단은 실행하지 않습니다.

| 파일 | 내용 |
| --- | --- |
| [image_model.py](image_model.py) | 형식·checksum·디렉터리 그래프·블록 소유권 검사와 읽기 전용 계획, 새 파일 복구 CLI입니다. |
| [fixtures.json](fixtures.json) | 고정 seed 이미지, 외부 내용 목록, 원래 파일 바이트와 예상 복구 동작입니다. |
| [verify.py](verify.py) | 실제 이미지 손상 주입, 새 자식 실행, 독립 기대값과 원본 보존 대조를 기록합니다. |

[손상 검사와 복구 계획](../../../설계와검증사례_engineering-cases/파일시스템의손상검사와복구계획_filesystem-check-repair.md) · [이름과 블록 소유권](../../../설계와검증사례_engineering-cases/파일이름과블록소유권의복구_filesystem-orphans-block-ownership.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/파일시스템이미지검사와복구_20261021.md)

## 실행

Python 3.10 이상과 표준 라이브러리만 사용합니다. 이 폴더에서 실행하며 C:/temp 아래 경로는 독자가 선택하는 새 폴더의 예입니다.

```powershell
python -X utf8 -B verify.py --output C:/temp/fs-normal-new
python -X utf8 -B -O verify.py --output C:/temp/fs-optimized-new
python -X utf8 -B -O verify.py --mutation ignore-shared --output C:/temp/fs-shared-new
python -X utf8 -B -O verify.py --mutation guess-size --output C:/temp/fs-size-new
python -X utf8 -B -O verify.py --mutation drop-orphan --output C:/temp/fs-orphan-new
python -X utf8 -B -O verify.py --mutation skip-digest --output C:/temp/fs-digest-new
```

정상 검증기는 PASS·종료 0입니다. 의도한 네 변이는 ERROR·종료 1이며, 기존 검증 출력 폴더는 종료 2로 거부합니다. 최종 기본/-O 정상 실행은 각각 이미지 사례 30개·대조 215개·자식 63개입니다. 자식의 종료 0은 명령이 처리됐다는 뜻이며 `structural`, `identity`, 계획의 `status`를 따로 읽습니다. 손상된 구조를 CHECKED·종료 0으로 보고할 수 있습니다. 자식의 형식·입력·복구 거부는 REJECTED·종료 3입니다. 실제 e2fsck의 종료값과는 다른 계약입니다.

results.json에는 환경·소스/fixture SHA, 실제 자식 명령·종료·stdout·stderr, 이미지/manifest/plan SHA와 관측을 남깁니다. `metadata_damage`에는 손상 원본·manifest·계획·복구 사본·두 번째 복구 사본이 남습니다. `orphan_file/recovered.json`에는 새 이름으로 연결한 inode가 있습니다. 의도한 변이는 첫 불일치에서 멈추므로 정상 실행과 검사 수가 다릅니다.

이미 생성한 손상 파일을 직접 읽는 예입니다. 마지막 명령의 manual-copy.json은 아직 존재하지 않아야 합니다.

```powershell
python -X utf8 -B image_model.py --image C:/temp/fs-normal-new/metadata_damage/image.json --manifest C:/temp/fs-normal-new/metadata_damage/manifest.json --action check
python -X utf8 -B image_model.py --image C:/temp/fs-normal-new/metadata_damage/image.json --manifest C:/temp/fs-normal-new/metadata_damage/manifest.json --action plan
python -X utf8 -B image_model.py --image C:/temp/fs-normal-new/metadata_damage/image.json --manifest C:/temp/fs-normal-new/metadata_damage/manifest.json --action repair --plan C:/temp/fs-normal-new/metadata_damage/plan.json --output C:/temp/fs-normal-new/metadata_damage/manual-copy.json
```

## 자체 이미지와 신뢰할 자료

super는 데이터 블록 크기 8바이트·개수 8개·root inode 1·lost+found inode 2를 고정합니다. seed에는 inode 6개와 일반 파일 3개가 있습니다. 디렉터리 레코드는 이름→inode, 일반 inode는 길이·블록 순서·nlink를 기록합니다. blocks에는 각 8바이트의 16진수 자료와 SHA-256을, bitmap에는 할당된 데이터 블록 번호를 저장합니다. 디렉터리 내용은 JSON metadata에 있으며 데이터 블록을 소비하지 않는 자체 규칙입니다.

`.`·`..`, 실제 디렉터리 링크 수, sparse file, preallocation, extent, reflink는 지원하지 않습니다. root의 nlink는 1, 나머지는 전체 디렉터리의 이름 참조 수입니다. 같은 파일 inode를 두 이름으로 가리키는 hard link는 허용하며, 다른 파일 inode끼리 데이터 블록을 공유하는 것은 거부합니다. 미지원 geometry·feature도 거부합니다.

이미지 SHA-256은 checksum 필드를 제외한 정렬된 compact JSON을 검사합니다. 블록 checksum은 현재 8바이트를 검사합니다. 의미상 손상 사례에서는 둘을 다시 계산해 잘못된 연결이 checksum을 통과하도록 만들었습니다. 이 경우에도 그래프와 소유권 검사가 필요합니다.

별도 manifest는 inode·원래 길이·내용 SHA-256을 담습니다. 독자가 그 목록을 신뢰한다는 전제이며 서명·접근 제어는 구현하지 않습니다. manifest가 없으면 구조가 맞아도 원래 내용은 NOT_ESTABLISHED입니다. 올바른 길이만큼 실제 바이트가 존재하고 digest도 같아야 VERIFIED입니다. 선언 64바이트에 실제 8바이트와 그 8바이트 digest를 주면 MISSING_PAYLOAD_BYTES입니다. manifest에는 원래 이름이나 payload 사본이 없습니다.

## 복구 정책

검사는 원본을 읽기만 하고 계획은 입력 이미지와 manifest의 SHA에 묶입니다. 존재하지 않는 inode의 이름 항목 제거, 근거가 있는 크기 정정, 이름 참조 수 정정, 사용 중인데 비어 있다고 표시된 비트 설정, 고유 블록을 가진 일반 orphan의 새 이름 연결을 계획합니다. 사본에 적용한 뒤 구조와 내용 기준을 확인하고 새 파일만 `xb`로 생성합니다. 기존 출력과 원본 경로는 거부합니다.

공유 블록·디렉터리 순환/여러 부모·고아 디렉터리·없는 payload 블록·할당됐지만 소유자가 없는 블록은 REFUSED입니다. 원래 크기나 내용 근거가 부족해도 거부합니다. 무주인 할당 비트를 지워 공간을 되찾거나 원래 이름을 지어냈다고 주장하지 않습니다. 복구 사본의 후속 계획이 비어 있고 두 번째 사본 bytes가 같은지도 확인합니다.

## 코드 읽기

`import`는 모듈을 불러오고 `def`는 함수를 정의합니다. `dict`는 키와 값, `list`는 순서, `set`은 중복 없는 번호 집합을 담습니다. `in`/`not in`으로 존재를 검사하고 `[:]`로 논리 길이만큼 바이트를 선택합니다. `copy.deepcopy`는 중첩 자료를 독립 복사합니다. `with`는 파일을 닫고 `xb`는 새 파일만 만듭니다. `raise`는 실패를 명시하므로 `-O`에서도 생략되지 않습니다. `subprocess.run`은 이전 프로세스의 객체를 공유하지 않는 새 해석기를 실행합니다.

## 원문과 범위

[ext4 inode](https://docs.kernel.org/filesystems/ext4/inodes.html), [directory](https://docs.kernel.org/filesystems/ext4/directory.html), [bitmap](https://docs.kernel.org/filesystems/ext4/bitmaps.html)은 실제 구조를 읽는 출발점입니다. [e2fsprogs 1.47.4 e2fsck 매뉴얼](https://man7.org/linux/man-pages/man8/e2fsck.8.html)은 읽기 전용 모드와 수정·미수정 상태의 종료값을 구분합니다. 열람일은 2026-10-21입니다. 자체 예제의 고정 geometry·JSON·SHA·정책과 실제 파일시스템 구현을 구분합니다. `flush`·`fsync` 호출은 호스트에 기록을 요청하며 전원 오류 내구성을 입증하지 않습니다.

## English

Fresh Python processes check bounded EDUFS1 JSON images, propose an input-bound plan and write only a new repaired copy. Two normal/optimized executions each pass 215 comparisons across 30 image cases and 63 child calls; four deliberate mutations fail in both modes. Fixed bytes, expected actions, source preservation and an idempotent second copy provide independent checks. Structural consistency and trusted content identity are separate results. A new salvage name does not recover the old name, and a digest is not a backup. No ext4, raw device, mount, e2fsck or power-loss test is executed.
