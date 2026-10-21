# 백업 세트의 내용 복원과 완전성 / Backup payload restore and completeness

백업 파일이 존재하거나 검사 프로그램이 종료 0을 반환해도, 필요한 파일을 모두 되살렸다는 뜻은 아닙니다. 이 사례는 세 파일의 실제 원문을 별도 백업 세트에 보관하고, 원본 하나를 삭제하고 다른 하나를 변경한 뒤 새 폴더로 복원합니다. 마지막에는 파일 수나 해시 합계 대신 정확한 경로 집합과 각 파일의 원문 바이트를 비교합니다. [AWS Well-Architected 2024-06-27 판본의 복원 시험 원칙](https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/rel_backing_up_data_periodic_recovery_testing_data.html)도 새 위치에 복원한 자료가 실제로 존재하고 읽히는지 검사하도록 설명합니다. 이번 실습은 AWS 서비스를 호출하지 않습니다.

[전체 코드·입력](../예제_examples/실무검증_practical-validation/backup_restore/README.md) · [실행 기록](검증기록_evidence/백업복원과누락검사_20261021.md) · [파일시스템의 구조 복구](파일시스템의손상검사와복구계획_filesystem-check-repair.md)

## 해시와 payload가 제공하는 정보

payload는 실제 내용 바이트입니다. SHA-256은 내용을 짧은 식별값으로 대응시키는 해시 함수입니다. 원래 파일이 5바이트였다는 정보와 그 해시가 있어도 사라진 5바이트를 다시 만드는 백업 사본은 생기지 않습니다. 해시는 갖고 있는 후보가 기준과 같은지 검사하는 데 쓰며, 복원은 보관한 payload를 다시 써야 합니다.

[기존 파일시스템 사례](파일이름과블록소유권의복구_filesystem-orphans-block-ownership.md)는 남아 있는 inode와 블록을 새 이름으로 연결합니다. 없는 payload의 원문은 복원하지 않습니다. 이번 예제는 백업에 원래 이름과 바이트를 함께 보관한다는 점이 다릅니다. 원본은 변경 전 복사하고, 손상 이후에는 복원 프로그램이 원본 폴더를 읽지 않습니다.

| 원래 경로 | 원문 16진수 | 논리 길이 |
| --- | --- | ---: |
| config.bin | `01020304` | 4바이트 |
| models/model.bin | `1020304050` | 5바이트 |
| notes/readme.txt | `4f4b0a`, 즉 `OK\n` | 3바이트 |

전체 payload는 4+5+3=12바이트입니다. manifest와 JSON 문법, 디렉터리·파일시스템 metadata가 차지하는 물리 공간은 이 합계에 넣지 않습니다. 세 파일을 같은 4바이트 자료로 바꾸어도 합계는 12바이트가 됩니다. 따라서 합계와 개수는 필요한 관측이지만 내용 동일성의 충분조건이 아닙니다.

## 백업 내부의 일치와 원하는 백업의 선택

BACKUP1의 manifest는 세대와 각 경로·길이·내용 해시를 기록합니다. generation은 서로 다른 시점의 사본을 구별하는 정수 표지이며 시간이 저절로 인증되는 값은 아닙니다. 세대 6의 온전한 백업도 세대 7을 원한 사용자에게는 다른 복원 입력입니다.

복원 요청에는 별도로 세대 7, 기대 경로 세 개, 정확한 manifest 바이트의 SHA-256을 넣습니다. 프로그램은 그 요청을 신뢰할 수 있다는 전제 아래 처리합니다. 백업 폴더를 읽은 뒤 현재 존재하는 파일만 목록으로 삼으면, 누락된 파일을 목록에서도 지워 정상으로 바꾸는 문제가 생깁니다. 기대 목록이 백업 밖에 있어야 그 누락을 찾을 수 있습니다.

manifest_omits_file 대조에서는 백업에서 마지막 항목을 없애고 요청의 manifest SHA도 새 값으로 맞춥니다. 그럼에도 요청의 세 경로는 그대로이므로 INVENTORY_MISMATCH입니다. 이는 “manifest 참조가 맞다”와 “필요한 전체 목록을 포함한다”가 별도 조건임을 보이는 자체 입력입니다. 요청 자체까지 공격자가 함께 바꿀 수 있다면 이 검사는 원래 세대를 증명하지 못합니다. 서명·접근 제어·보호된 이력 저장은 구현하지 않았습니다.

old_generation 대조는 내용이 온전하고 요청의 manifest 참조도 해당 세대 6 문서를 가리키도록 구성합니다. 단, 요청의 원하는 세대는 계속 7입니다. accept-old-generation 변이는 마지막 세대 비교를 생략하여 이 입력을 받아들이므로 검증기가 실패합니다. 같은 바이트가 나왔다는 사실만으로 복원 시점 선택의 계약을 없애지 않습니다.

## 새 사본을 완성한 뒤 공개하는 순서

순서는 요청 읽기 → manifest 참조·schema 검사 → 전체 경로 집합 검사 → 모든 백업 payload 길이·해시 검사 → 새 staging 생성 → 실제 바이트 쓰기 → staging의 전체 경로·길이·해시 검사 → 입력 참조 재확인 → 목적지 이름으로 rename입니다. staging은 최종 결과를 준비하는 임시 디렉터리입니다. 준비가 덜 된 자료를 사용자에게 완성된 복원으로 보여 주지 않기 위해 둡니다.

이번 실행에서는 원본의 models/model.bin을 삭제하고 config.bin을 `09090909`로 바꿨습니다. 복원 자식 프로세스에는 backup·request·destination만 넘깁니다. 새 목적지에서 config.bin은 `01020304`, models/model.bin은 `1020304050`, notes/readme.txt는 `4f4b0a`였습니다. 원본은 삭제·변경된 상태 그대로이고 백업·요청 해시도 전후 같았습니다. 원본을 몰래 다시 쓰는 방식으로 성공시키지 않았습니다.

```python
expected = {"config.bin", "models/model.bin", "notes/readme.txt"}  # {}는 중복 없는 기대 경로 set입니다.
found = set(payloads)  # set(dict)는 사전의 키, 즉 실제 가진 경로를 모읍니다.
if found != expected:  # !=는 두 집합이 서로 다른지 검사합니다.
    raise ValueError("RESTORE_INCOMPLETE")  # raise는 -O에서도 남는 명시적 실패입니다.
for name, data in sorted(payloads.items()):  # items는 경로·바이트 쌍, sorted는 고정 순서입니다.
    path = stage / name  # Path의 /는 부모와 자식 경로를 결합합니다.
    path.parent.mkdir(parents=True, exist_ok=True)  # 필요한 하위 폴더를 만듭니다.
    with path.open("xb") as stream:  # with는 파일을 닫으며 xb는 기존 파일을 덮지 않습니다.
        stream.write(data)  # write는 보관한 실제 바이트를 새 파일에 기록합니다.
```

이 발췌는 전체 함수에서 경로 검사가 끝난 뒤의 목적을 요약한 읽기 예입니다. 독립 검증기는 payloads에서 기대값을 만들지 않고 세 bytes literal을 따로 가집니다. 검사 대상이 잘못된 결과를 냈을 때 기대값까지 함께 달라지지 않도록 하기 위한 구분입니다.

## 중단 결과와 정상 결과를 혼동하지 않습니다

파일은 경로 정렬 순서로 씁니다. `--cut-after 1`에서는 config.bin 4바이트를 staging에 기록한 뒤 INTERRUPTED·종료 4로 반환합니다. 목적지는 아직 없습니다. 남아 있는 `.staging/config.bin=01020304`는 중단 증거이며 성공 결과가 아닙니다. 같은 경로로 다시 실행하면 OUTPUT_EXISTS로 거부해 그 부분 결과를 자동 재사용하지 않습니다.

publish-before-complete 변이는 staging 이름을 먼저 최종 목적지로 바꿉니다. 정상적인 끝까지 쓰면 겉보기 결과는 같을 수 있습니다. 그러나 첫 파일 뒤 중단하면 목적지에 config.bin만 공개되므로 “부분 결과를 공개하지 않는다”는 고정 기대값에서 실패합니다. 파일 몇 개를 쓰는지보다 언제 완성 결과로 보이게 하는지가 원인입니다.

이 중단점은 Python 함수가 정해진 위치에서 반환하는 실험입니다. 강제 종료·정전·write tearing을 주입하지 않았습니다. flush와 fsync를 호출하고 같은 부모의 rename을 관측해도, 실제 장치가 전원 상실 후 어디까지 보존하는지는 알 수 없습니다. [Python 3.12 os.rename](https://docs.python.org/3.12/library/os.html#os.rename)의 운영체제별 대상 처리와 파일시스템 경계를 구분해서 읽어야 합니다. 사전 존재 검사는 공격적인 동시 작성자의 경합을 해결하는 no-replace 보장이 아닙니다.

## 경로와 입력 형식도 복원 계약입니다

경로 문자열을 단순히 부모 뒤에 붙이면 `../escape.bin`이나 절대 경로가 다른 위치를 가리킬 수 있습니다. [Python pathlib의 경로 결합과 순수 경로 의미](https://docs.python.org/3.12/library/pathlib.html)는 운영체제에 따라 절대 경로·대소문자 처리가 다름을 설명합니다. 이 예제는 범용 백업 형식을 흉내 내기보다 허용 문자를 좁힙니다.

이름은 ASCII 상대 경로이며 `..`, `.`, 빈 구간, 역슬래시, 드라이브·절대 경로, Windows 예약 이름을 거부합니다. config.bin과 CONFIG.bin, Models/a와 models/b 같은 충돌도 거부합니다. models가 파일이면서 models/model.bin의 부모인 입력은 PATH_PREFIX_COLLISION입니다. JSON의 같은 키 두 번도 마지막 값만 채택하지 않고 DUPLICATE_JSON_KEY로 거부합니다.

symlink와 Windows reparse 경로는 원본·부모·payload에서 지원하지 않습니다. 이번 Windows 환경에서는 새 symlink를 만드는 데 필요한 권한이 없어 WinError 1314였습니다. 해당 실행은 NOT_EXECUTED이며 실제 link 거부를 통과한 것으로 기록하지 않습니다. 코드에 검사가 있다는 사실과 이 환경에서 그 경계를 실행했다는 사실을 구분합니다.

표준 형식은 파일 최대 16개, 파일당 0~4096바이트, JSON 각각 최대 16384바이트입니다. bool은 Python에서 정수처럼 비교될 수 있지만 세대·길이는 `type(value) is int`로 검사해 True를 받지 않습니다. hard link·소유권·ACL·timestamp·sparse file은 지원하지 않습니다. 입력과 출력 경로를 다른 프로세스가 경쟁적으로 바꾸지 않는 새 실습 폴더에서 실행합니다.

## 검출한 오류와 실제 관측

| 의도한 오류 변이 | 잘못된 결정 | 기본/-O에서 관측한 실패 |
| --- | --- | --- |
| missing-file-allowed | 없는 payload를 건너뛰고 남은 목록만 완전하다고 판단합니다. | missing_payload에서 기대한 거부 대신 성공해 종료 1입니다. |
| skip-content-check | 길이가 같으면 해시 비교를 건너뜁니다. | changed_payload의 한 바이트 변경을 받아 종료 1입니다. |
| accept-old-generation | 요청 세대와 백업 세대 비교를 생략합니다. | old_generation에서 세대 6을 받아 종료 1입니다. |
| publish-before-complete | 복원이 끝나기 전에 목적지를 공개합니다. | 첫 파일 뒤 목적지가 존재해 종료 1입니다. |

정상 기본/-O는 각각 31개 사례·163개 대조·32개 자식에서 PASS·종료 0입니다. 누락 payload·같은 길이 변경·짧은 payload·선언 길이 오류·옛 세대·manifest 교체·예상 밖 파일·빈 디렉터리·목록 누락·경로 충돌·입력 범위·기존 출력·중단 후 재실행을 확인했습니다. 네 변이는 두 모드에서 모두 실패 기록을 남겼습니다. `assert`만 사용하지 않으므로 최적화에서 핵심 검사가 사라지지 않습니다.

## DB 백업으로 연결할 때

일반 파일 세 개를 복사했다고 실행 중인 DB를 일관되게 백업한 것은 아닙니다. 서로 다른 시점의 페이지와 log를 모으면 각 파일 해시는 맞아도 동일한 DB 시점이 아닐 수 있습니다. [PostgreSQL 17 SQL Dump §25.1–25.1.1](https://www.postgresql.org/docs/17/backup-dump.html)은 dump snapshot, 복원 오류 때 남을 수 있는 부분 상태와 단일 트랜잭션 복원을 구분합니다. 이번 호스트 예제는 그런 DB 명령을 실행하거나 형식을 구현하지 않습니다. 응용의 일관된 기준점, 전체 목록과 실제 복원 검증이 각각 필요하다는 연결만 다룹니다.

## 확인 문제

1. 3개 파일·총 12바이트가 맞으면 원문 복원도 증명됩니까?
2. manifest에서 누락 파일 항목도 지워 새 해시를 만들면 완전성이 확인됩니까?
3. 첫 파일 기록 뒤 staging만 남은 결과와 목적지에 첫 파일만 보이는 결과의 차이는 무엇입니까?

답: 1. 아닙니다. 경로 집합과 각 파일 원문을 따로 대조해야 합니다. 2. 현재 목록 안의 일치만 맞출 수 있습니다. 별도로 신뢰한 기대 목록·세대·manifest 참조가 필요합니다. 3. 전자는 미완료 자료를 분리한 상태이고 후자는 부분 결과를 완성 위치로 공개한 상태입니다. 어느 쪽도 이번 실험만으로 정전 내구성을 증명하지 않습니다.

## English

This case restores three real payload files from generation 7 after deleting or changing the original files. A trusted external request pins the generation, exact manifest digest and full path inventory. Backup consistency, requested-generation identity and restored completeness are separate contracts. A fresh staging directory is checked before publication. Fixed path and byte literals independently establish all three restored files and 12 logical bytes; unchanged hashes prove that the damaged originals and backup inputs were preserved. A deterministic cut after one file leaves staging evidence without a final destination. Four faults demonstrate skipped missing payload, skipped digest checks, accepted old generation and premature publication. Normal and optimized runs each pass 163 checks across 31 cases and 32 child calls. Symlink creation is not executed because Windows denies the privilege. The exercise assumes controlled single-writer directories and does not establish authenticated provenance, adversarial path-race resistance, DB consistency or physical power-loss durability.

## 출처와 판본

2026-10-21에 Python 3.12 문서의 pathlib 도입·pure path 결합/대소문자·is_symlink·rename, os.rename 본문을 읽었습니다. PostgreSQL 17 §25.1 도입과 §25.1.1 복원·오류·단일 트랜잭션 범위, AWS Well-Architected 2024-06-27 판본 REL09-BP04의 도입·anti-pattern·복원 검증 절차를 읽었습니다. 원문은 각 관련 문단에 직접 연결했습니다. BACKUP1·RESTORE-REQUEST1·고정 바이트·세대 7·중단점·오류 변이는 자체 교육 실험입니다.
