# 중단된 A/B 업데이트와 재시작 / Interrupted A/B updates and restart

서로 다른 Python 프로세스가 실제 이미지 파일·메타데이터 파일을 다시 읽으며 업데이트 중단과 재선택을 비교합니다. 이미지는 실행 파일이 아닌 자체 바이트열입니다. `BOOT`는 파일 선택 결과이며 실제 CPU가 firmware로 분기하거나 MCUboot를 실행한 결과가 아닙니다.

| 파일 | 역할 |
| --- | --- |
| [models.py](models.py) | A/B 파일 기록, 길이·SHA-256 검사, 두 CRC 기록의 세대 선택, trial·confirm·rollback을 수행합니다. |
| [fixtures.json](fixtures.json) | 8/12바이트 이미지·해시와 손으로 정한 슬롯·모드·세대 기대값입니다. |
| [verify.py](verify.py) | 자식 프로세스의 중단·재시작, 34개 cut, 손상·오류 주입과 결과 보존을 검사합니다. |

## 실행

Python 3.10 이상 표준 라이브러리를 사용합니다. 이 폴더에서 아직 없는 결과 경로를 지정합니다. 이번 실행 환경은 CPython 3.12.14·Windows 11입니다.

```powershell
python -X utf8 -B verify.py --output C:/temp/update-run-new
python -X utf8 -B -O verify.py --output C:/temp/update-optimized-new
python -X utf8 -B verify.py --mutation erase-active --output C:/temp/update-active-fault-new
python -X utf8 -B verify.py --mutation confirm-early --output C:/temp/update-confirm-fault-new
python -X utf8 -B verify.py --mutation skip-hash --output C:/temp/update-hash-fault-new
python -X utf8 -B verify.py --mutation single-record --output C:/temp/update-record-fault-new
```

정상 기본/`-O` 실행은 종료 0, 네 mutation은 각각 종료 1입니다. 같은 출력 경로는 종료 2로 거부하며 이전 파일을 지우지 않습니다. 자식 모델의 종료 3은 의도한 입력·상태 거부일 수 있고 종료 23은 명시적인 cut입니다. 부모는 각각 기대한 종료와 결과를 따로 비교합니다.

`results.json`에는 부모 환경·명령·최적화 수준·소스/입력 SHA-256·검사값·중단 목록과 모든 자식 명령/종료/결과가 있습니다. 사례별 `input.json`, `store/slotA.bin`, `store/slotB.bin`, `record0.json`, `record1.json`도 남깁니다. 시험은 새 결과 폴더 안의 파일만 쓰며 저장장치·시스템 설정·기존 결과를 변경하지 않습니다.

## 상태 계약

초기 확정 슬롯은 A입니다. inactive B에 기록한 뒤 길이·해시를 확인하고 pending을 게시합니다. 첫 선택 전에 attempted=true를 별도 세대로 기록하며, confirm이 없으면 다음 재시작에서 A로 돌아갑니다. `--application-ok`는 외부에서 완료했다고 선언한 모형 checkpoint일 뿐 실제 자가진단 프로그램이 아닙니다.

| generation | active | pending | attempted | 의미 |
| ---: | --- | --- | --- | --- |
| 0 | A | 없음 | false | 기존 확정 이미지입니다. |
| 1 | A | B | false | 검증한 후보가 있습니다. |
| 2 | A | B | true | B를 한 번 선택했다고 기록합니다. |
| 3, confirm | B | 없음 | false | checkpoint 뒤 B를 확정합니다. |
| 3, rollback | A | 없음 | false | 확인되지 않은 B에서 A로 돌아갑니다. |

모형은 slot당 최대 32바이트, generation 0~1,000,000을 지원합니다. 고정 fixture는 old 8바이트·new 12바이트이며 이미지 cut은 0~12바이트 prefix 13개입니다. generation 순환, 실제 firmware 크기·vector table·명령어·DTB/rootfs 호환성·다중 이미지 묶음은 구현하지 않습니다.

두 JSON 기록은 CRC32와 상태 schema를 확인하고 가장 큰 유효 generation을 선택합니다. 새 기록을 반대 부에 써서 이전 유효 기록을 보존합니다. 같은 최대 generation에 다른 상태가 둘 있거나 유효 기록이 하나도 없으면 복구가 필요하다고 거부합니다. CRC는 악의적인 변경을 인증하지 않습니다.

## 중단의 의미

선택한 prefix를 실제 파일에 쓴 뒤 `flush()`·`os.fsync()`를 호출하고 `os._exit(23)`으로 자식 프로세스를 끝냅니다. 새 프로세스는 파일을 다시 읽습니다. 실제 flash에 임의 시각의 전원 오류를 넣은 시험이나 OS 전원 상실의 재현이 아닙니다. 디렉터리 fsync, erase/program 단위·비트 방향·ECC·wear·컨트롤러 전원 캐시는 검증하지 않았습니다.

유한 집합은 이미지 prefix 13개, 검증 직후 1개, pending/trial/confirm/rollback 기록의 0·1·절반·마지막 바이트 직전·전체 5개씩으로 총 34개입니다. 선택한 집합을 모두 실행했으며 모든 메타데이터 바이트 위치나 모든 전원 오류를 포괄했다는 뜻은 아닙니다. 기록 전체를 마친 뒤의 cut도 넣어 완료 전·후 선택을 구분합니다.

## 해시만으로 보장하지 않는 것

길이와 SHA-256은 입력으로 받은 manifest와 실제 바이트의 일치를 확인합니다. 이 모형에는 서명·신뢰 키·권한·신뢰된 security counter가 없습니다. 공격자가 이미지와 manifest 해시를 함께 바꾸면 수락하며, 이전 이미지로의 재업데이트도 허용합니다. 이 두 결과를 정상 검사 안의 한계 대조로 명시합니다. production secure boot나 anti-rollback 구현으로 사용하지 않습니다.

- [원리·오류·관측 결과](../../../설계와검증사례_engineering-cases/중단된업데이트의슬롯선택과롤백_firmware-ab-update.md)
- [2026-10-21 실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/펌웨어업데이트중단과복구검사_20261021.md)
- [부팅·Device Tree·드라이버의 경계](../../../전자컴퓨터공학_ece/18-임베디드Linux_embedded-linux/해설_notes/boot-devicetree-driver-boundaries.md)

## English

Separate Python processes write and reopen real disk files representing two image slots and two CRC-protected metadata records. The suite covers 34 declared interruption checkpoints, corrupt images/metadata, trial confirmation and rollback. Files are educational byte arrays, not executable firmware. Flushed prefixes plus explicit process exits do not model arbitrary flash or OS power loss. Hash matching supplies neither authorization nor anti-rollback.
