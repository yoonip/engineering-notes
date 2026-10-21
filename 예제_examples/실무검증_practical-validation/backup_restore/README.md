# 백업 payload 복원과 전체 파일 확인 / Backup payload restore and complete file checks

세대 7의 실제 백업 파일을 읽어 새 목적지에 세 파일·12바이트를 복원합니다. 원본을 삭제·변경한 뒤에도 별도 백업 payload를 사용하므로, 해시만 비교하는 검사와 내용 복원을 구분할 수 있습니다. 표준 라이브러리를 쓰는 호스트 파일 실습이며 실제 장치 정전이나 DB 복구를 실행하지 않습니다.

| 파일 | 내용 |
| --- | --- |
| [model.py](model.py) | 요청·manifest·경로·내용을 검사하고 새 staging을 완성한 뒤 목적지를 공개하는 CLI입니다. |
| [fixtures.json](fixtures.json) | 세 경로·원문 바이트·세대·총길이와 네 오류 변이 이름입니다. |
| [verify.py](verify.py) | 새 원본과 백업 생성, 손상 주입, 별도 프로세스 실행과 독립 literal 대조입니다. |

[원리와 사례](../../../설계와검증사례_engineering-cases/백업세트의내용복원과완전성_backup-restore-integrity.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/백업복원과누락검사_20261021.md)

## 실행

Python 3.10 이상이 필요합니다. 아래 출력은 각각 새 폴더여야 합니다. 이 폴더에서 실행합니다.

```powershell
python -X utf8 -B verify.py --output C:/temp/backup-fixed-new
python -X utf8 -B -O verify.py --output C:/temp/backup-optimized-new
python -X utf8 -B verify.py --mutation missing-file-allowed --output C:/temp/backup-missing-new
python -X utf8 -B verify.py --mutation skip-content-check --output C:/temp/backup-content-new
python -X utf8 -B verify.py --mutation accept-old-generation --output C:/temp/backup-old-new
python -X utf8 -B verify.py --mutation publish-before-complete --output C:/temp/backup-partial-new
```

기본/-O 정상 실행은 각각 PASS·종료 0이며 31개 사례·163개 대조·32개 자식 실행입니다. 각 변이는 기본/-O에서 ERROR·종료 1이었으며, 의도한 실패 기록은 results.json에 남습니다. 기존 검증 출력 폴더는 종료 2로 거부합니다. Windows의 symlink 생성은 WinError 1314로 실행하지 못해 capabilities.symlink를 NOT_EXECUTED로 기록했습니다. 이 경계를 통과했다고 세지 않습니다.

직접 복원하려면 정상 검증기가 만든 입력을 사용하고 아직 없는 목적지를 지정합니다.

```powershell
python -X utf8 -B model.py --backup C:/temp/backup-fixed-new/restore_deleted_and_changed/backup --request C:/temp/backup-fixed-new/restore_deleted_and_changed/request.json --destination C:/temp/backup-manual-new
```

복원 CLI는 RESTORED·종료 0, REFUSED·종료 3, 의도한 중단 INTERRUPTED·종료 4를 구분합니다. `--cut-after 1`은 첫 파일 기록 뒤 함수가 반환되는 결정적 중단점입니다. 프로세스를 강제 종료하거나 전원을 끈 실험은 아닙니다. 정상 중단은 destination.staging에 config.bin만 남기고 목적지는 만들지 않습니다. 같은 staging을 자동 재사용하지 않습니다.

## 신뢰와 범위

별도 RESTORE-REQUEST1에는 원하는 세대, 정확한 manifest 바이트의 SHA-256, 기대 경로 목록이 있습니다. BACKUP1 manifest에는 세대와 각 파일의 경로·길이·SHA-256이 있습니다. 두 JSON과 payload가 백업 세트를 이룹니다. 요청은 사용자가 이미 신뢰한 기준이라는 전제입니다. SHA 자체로 작성자를 인증하거나 요청 파일의 변조를 막지 않습니다.

파일은 최대 16개, 각 0~4096바이트이며 JSON은 각각 16384바이트 이하입니다. 이름은 제한된 ASCII 상대 경로만 허용합니다. `..`, 절대 경로, 역슬래시, Windows 예약 이름, 중복·대소문자 충돌, 파일/디렉터리 prefix 충돌, symlink와 Windows reparse 경로를 거부합니다. 빈 파일 복원은 형식상 허용하지만 이번 고정 성공 예의 파일 길이는 4·5·3바이트입니다. hard link·ACL·소유자·timestamp·sparse file·DB 일관성을 복원하지 않습니다.

실습 폴더에 경쟁 작성자가 없다는 전제입니다. 경로 검사와 파일 열기 사이의 공격적 경합까지 방어하는 백업 제품이 아닙니다. staging과 목적지는 같은 부모에 두고 기존 입력·출력을 덮지 않습니다. Python의 rename은 운영체제별 기존 목적지 처리 차이가 있으므로 사전 존재 검사를 운영체제 전반의 경쟁 없는 원자적 no-replace 기능으로 일반화하지 않습니다. flush·fsync·rename의 호출 성공은 정전 뒤 내구성 시험 결과가 아닙니다.

## 결과 읽기와 문법

results.json은 실제 자식 명령·종료·stdout/stderr, 입력 해시 보존, 고정 바이트와의 비교, 환경과 세 소스 SHA를 기록합니다. 기대값은 `config.bin=01020304`, `models/model.bin=1020304050`, `notes/readme.txt=4f4b0a`이며 복원 결과를 읽어 기대값을 새로 만들지 않습니다. 네 변이는 같은 기대값을 사용합니다.

`import`는 파일·해시·JSON 기능을 불러옵니다. `def`는 함수, `dict`는 경로와 자료의 대응, `set`은 중복 없는 경로 집합을 나타냅니다. `with`는 파일을 닫고 `xb`는 새 이진 파일만 만듭니다. `raise`는 실패를 명시하므로 `-O`에서도 검사가 남습니다. `subprocess.run`은 별도 Python 프로세스를 실행합니다.

## English

The verifier snapshots three real payload files, deletes or changes source files, and restores the backup into a fresh directory. A trusted request pins generation 7, the manifest digest and the complete path inventory. A staging directory is checked before publication; a deterministic interruption leaves only staging evidence. Fixed path/byte literals independently establish all three restored files and 12 logical bytes. Normal and optimized runs each pass 163 checks across 31 cases and 32 child calls. Four deliberate faults fail in both modes. Symlink creation is not executed because Windows denies the required privilege. This bounded single-writer exercise does not establish adversarial path-race safety, authenticated backup provenance, database consistency or power-loss durability.

## 직접 읽은 원문

- [Python 3.12 pathlib](https://docs.python.org/3.12/library/pathlib.html): 순수 경로와 파일 I/O, 경로 결합·대소문자 의미, is_symlink·rename입니다.
- [Python 3.12 os.rename](https://docs.python.org/3.12/library/os.html#os.rename): 운영체제별 기존 목적지 처리와 파일시스템 경계입니다.
- [PostgreSQL 17 SQL Dump §25.1–25.1.1](https://www.postgresql.org/docs/17/backup-dump.html): DB snapshot·복원 오류·부분 복원과 단일 트랜잭션의 차이입니다. 이 예제는 PostgreSQL 명령을 실행하지 않습니다.
- [AWS Well-Architected 2024-06-27 REL09-BP04](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/rel_backing_up_data_periodic_recovery_testing_data.html): 새 위치에서 실제 자료를 복원하고 내용·접근 가능성을 확인하는 절차입니다. AWS 서비스는 실행하지 않습니다.

열람일은 2026-10-21입니다. 자체 BACKUP1 형식·크기 제한·거부 정책은 이 실습에서 정했습니다.
