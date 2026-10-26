# 중단된 저널의 트랜잭션 복구 / Transaction recovery from an interrupted journal

재고와 잔액을 함께 바꾸다가 기록이 중단되어도 새 재고와 옛 잔액이 섞이지 않아야 합니다. 이 사례는 DATA에 두 필드를 모으고 COMMIT을 확인한 경우에만 재생하는 자체 redo 저널입니다. 실제 호스트 파일을 기록하고 새 Python 프로세스로 복구합니다. 전원 제거·OS crash·flash fault를 실행한 결과는 아닙니다.

[코드와 고정 입력](../예제_examples/실무검증_practical-validation/storage_recovery/README.md) · [실행 기록](검증기록_evidence/저장저널중단과복구검사_20261021.md) · [부팅과 저장 데이터](../전자컴퓨터공학_ece/18-임베디드Linux_embedded-linux/해설_notes/부팅과장치트리및드라이버_boot-devicetree-driver-boundaries.md)

## 1. 파일에 값이 있다는 사실과 확정된 상태를 구분합니다

트랜잭션은 여러 변경을 하나의 묶음으로 다루는 단위입니다. 원자성은 그 묶음이 모두 반영되거나 전혀 반영되지 않은 것처럼 보이는 성질입니다. 여기서는 credit50·stock10을 credit80·stock7로 함께 바꿉니다. 두 필드는 설명용 값이며 실제 금전·재고 시스템을 구현한 것은 아닙니다.

redo는 확정한 변경을 다시 적용해 상태를 재구성하는 방식입니다. 로그의 DATA에는 변경 뒤 값이 있고, 그 뒤 COMMIT에는 어느 DATA를 확정하는지 들어갑니다. 읽는 도중 DATA를 보자마자 응용 상태를 바꾸는 경로가 의도한 오류입니다. 새 DATA만 쓰인 파일을 다시 읽으면 credit80·stock7이 보이지만, COMMIT이 없으므로 정답은 여전히 credit50·stock10입니다.

SQLite의 WAL 문서도 frame과 commit marker, 검사값을 구분합니다. 이 사례는 그 구분을 공부하는 작은 자체 형식이며 SQLite의 WAL header·page·salt·checksum 알고리즘이나 SQL 동작을 복제하지 않습니다. [SQLite Database File Format §4.1·4.5](https://www.sqlite.org/fileformat2.html#walformat)

## 2. 길이·순번·CRC·COMMIT이 맡은 일이 다릅니다

파일 맨 앞은 JNL1 4바이트입니다. 이후 frame은 다음과 같습니다. framing은 바이트 흐름에서 기록의 시작과 끝을 찾는 규칙입니다.

| 위치·크기 | 자체 규칙 | 검사의 목적 |
| --- | --- | --- |
| header 0~3·4바이트 | REC1 | 예상한 기록 경계를 확인합니다. |
| header 4·1바이트 | version1 | 해석 규칙을 고정합니다. |
| header 5·1바이트 | DATA=1, COMMIT=2 | 보류할 값과 확정 표시를 구분합니다. |
| header 6~7·2바이트 | payload 길이 | 다음 기록의 위치를 계산합니다. |
| header 8~11·4바이트 | seq | 직전 확정 번호+1인 트랜잭션인지 확인합니다. |
| payload | DATA의 정렬된 JSON 또는 DATA CRC 4바이트 | 값과 확정 대상을 담습니다. |
| 마지막 4바이트 | header+payload의 CRC32 | 완전한 frame의 우발적 변경을 검사합니다. |

`struct.Struct("<4sBBHI")`에서 `<`는 little endian, 4s는 bytes4, B는 정수1바이트, H는 정수2바이트, I는 정수4바이트입니다. CPU의 기본 byte order나 C 구조체 padding에 기대지 않습니다. seq 범위 1~65535·payload 1~128바이트·파일 65536바이트·값 0~1000은 교육용 상한입니다. 64KiB 안에 모든 seq를 담을 수 있다는 뜻은 아닙니다.

COMMIT은 같은 seq와 해당 DATA의 CRC를 함께 가리켜야 합니다. frame CRC가 맞아도 번호가 건너뛰거나 다른 DATA를 가리키는 COMMIT은 거부합니다. JSON에는 credit·stock 두 키만 허용하고 bool·중복 키·불필요한 공백 표현은 받지 않습니다. `true`가 Python에서 정수처럼 취급될 여지를 막기 위해 `type(value) is int`를 사용합니다.

```python
def transaction(seq, values):  # def는 번호와 값 묶음을 받는 함수를 정의합니다.
    data = frame(1, seq, values_bytes(values))  # 함수 호출로 DATA header·payload·CRC를 만듭니다.
    commit = frame(2, seq, data[-4:])  # [-4:]는 DATA 뒤의 CRC 4바이트를 선택합니다.
    return data, commit  # return은 두 bytes를 tuple로 반환합니다.
```

초기 seq1의 DATA payload는 24바이트여서 frame40, COMMIT20, 파일 header4와 합쳐 64바이트입니다. 갱신 seq2의 `{"credit":80,"stock":7}`은 23바이트라 DATA39·COMMIT20·합계59바이트입니다. 모두 기록하면 파일 크기는 `64+59=123`입니다. CRC32의 표준 대조 입력 `123456789` 결과는 0xCBF43926입니다. fixture에는 저널 전체 hex와 SHA-256도 리터럴로 적어 encoder를 바꿨을 때 상태 값만 우연히 맞는 경우와 구분합니다.

## 3. 수정 경로는 DATA를 보류하고 COMMIT 뒤에 게시합니다

복구 함수는 새 상태를 지역 딕셔너리에 구성합니다. complete frame의 길이·CRC와 DATA 형식을 먼저 확인한 뒤 pending에 보관합니다. 아래는 COMMIT 처리의 핵심이며, 이 전에 header·frame CRC 검사가 수행됩니다.

```python
require(pending is not None, "COMMIT_WITHOUT_DATA")  # is not None은 보류 DATA의 존재를 확인합니다.
require(seq == pending[0], "COMMIT_SEQUENCE")  # [0]은 보류 tuple의 번호이며 ==는 같은지 비교합니다.
require(payload == U32.pack(pending[2]), "COMMIT_BINDING")  # pack은 DATA CRC를 4바이트로 바꿉니다.
state.update(pending[1])  # update는 확인한 두 값을 복구 상태에 함께 반영합니다.
sequence, pending, committed_end = seq, None, end  # 여러 이름에 새 확정 상태를 대입합니다.
commits.append(seq)  # append는 확정 번호를 리스트 끝에 추가합니다.
```

정상 파일을 두 번 복구해 같은 상태·seq·SHA를 얻고 원본 파일이 변하지 않는지도 확인합니다. 복구 결과는 JSON으로 관측할 뿐 실제 데이터베이스 파일에 checkpoint를 기록하지 않습니다. 단일 writer·순차 접근 계약이며 파일 잠금·동시 읽기 snapshot·저널 회전·공간 회수는 없습니다.

미확정 꼬리를 잘라내는 작업도 하지 않습니다. `committed_end`는 마지막 확정 COMMIT 다음 위치이고, `ignored_bytes`는 그 이후 남은 양입니다. writer는 꼬리가 있는 저널을 TAIL_NEEDS_REPAIR로 거부해 그 뒤에 새 트랜잭션을 덧붙이지 않습니다. 이 코드만으로 손상 파일을 자동 수리했다고 쓰지 않습니다.

## 4. 새 프로세스가 읽은 60개 중단 지점

정상 seq1 파일을 만든 뒤 seq2 트랜잭션 59바이트 중 앞 k바이트만 추가합니다. k=0~59를 각각 별도 폴더에서 실행합니다. 자식은 선택한 prefix를 쓰고 flush·fsync 뒤 종료 23으로 끝나며, 다음 새 자식은 파일을 처음부터 읽습니다.

| 추가 prefix | 복구 상태·번호 | 꼬리 판정 |
| --- | --- | --- |
| 0바이트 | credit50·stock10·seq1 | CLEAN입니다. |
| 1~38바이트 | credit50·stock10·seq1 | DATA가 부족한 INCOMPLETE_FRAME입니다. |
| 39바이트 | credit50·stock10·seq1 | DATA만 완성된 UNCOMMITTED_DATA입니다. |
| 40~58바이트 | credit50·stock10·seq1 | COMMIT이 부족한 INCOMPLETE_FRAME입니다. |
| 59바이트 | credit80·stock7·seq2 | DATA와 COMMIT이 모두 있어 CLEAN입니다. |

cut39의 파일은 103바이트, 확정 끝은 64, 무시할 꼬리는39입니다. cut58은 파일122·꼬리58이며 cut59는 파일123·확정 끝123·꼬리0입니다. 60개 모두 직접 적은 상태·번호·tail·길이 기대값과 맞았습니다. cut59에서도 자식은 23으로 끝납니다. 호출자가 성공 응답을 받지 못했다는 사실과 기록이 확정되지 않았다는 사실은 같지 않습니다.

이 prefix 행렬은 정해진 한 트랜잭션의 모든 byte prefix를 다룬 유한 시험입니다. 임의의 여러 위치가 동시에 손상되거나 OS·장치가 쓰기를 재정렬하는 모든 경우를 열거한 것은 아닙니다.

## 5. 손상 거부와 파서가 구분하지 못하는 경우

| 직접 만든 입력 | 관측 |
| --- | --- |
| 완전한 DATA/COMMIT의 CRC trailer를 바꿉니다. | FRAME_CRC로 거부합니다. |
| 중간 DATA CRC를 바꾸고 뒤에 정상 seq3까지 둡니다. | 뒤 magic을 찾아 재동기화하지 않고 거부합니다. |
| seq1 다음에 CRC가 맞는 seq3을 붙입니다. | DATA_SEQUENCE로 거부합니다. |
| DATA보다 COMMIT을 앞에 둡니다. | COMMIT_WITHOUT_DATA로 거부합니다. |
| COMMIT 번호·DATA 결합값을 바꿉니다. | COMMIT_SEQUENCE·COMMIT_BINDING으로 구분합니다. |
| 중복 JSON 키·bool·두 DATA의 연속 | 정규 형식·정수·보류 기록 계약으로 거부합니다. |

거부한 결과에는 응용 state가 없습니다. 유효한 앞부분이 있었다는 사실을 저널 전체가 정상이라는 결론으로 바꾸지 않습니다. 반면 끝의 부족한 자료만으로 모든 손상을 알아낼 수도 없습니다. 마지막 header보다 짧은 쓰레기와 실제로 잘린 header는 이 규칙에서 같은 INCOMPLETE_FRAME이 될 수 있습니다.

별도 한계 대조에서는 DATA 길이 23을 허용 범위 안의 128로 바꿨습니다. 뒤에 온전한 COMMIT·seq3이 있어 파일은182바이트지만 parser가 계산한 해당 frame 끝은 `64+12+128+4=208`입니다. frame이 부족하다고 판단해 seq1·ignored118을 반환했습니다. header 길이 손상을 모두 검출한다는 보장은 없습니다. 고정 블록·중복 길이·더 강한 메타데이터 설계는 별도의 계약과 시험이 필요합니다. CRC는 인증이나 악의적 변경 방지를 대신하지도 않습니다.

## 6. 검증기가 오류를 놓치지 않는지 확인합니다

네 변이는 기대값을 바꾸지 않고 구현만 잘못 바꿉니다. `apply-uncommitted`는 cut39에서 새 값을 공개하고, `ignore-crc`는 CRC trailer 손상을 수락하며, `ignore-sequence`는 1→3 번호를 수락합니다. `commit-first`는 COMMIT을 먼저 써 리터럴 기록 순서부터 달라집니다. 기본/-O 모두 종료1이었으며 정상 두 실행은 종료0·검사178개·자식237개로 일치했습니다. 일반 assert 대신 명시적 예외를 사용합니다.

완전한 자료의 손상 거부 12종, 순서/형식 입력 오류, 값 경계0/1000, payload128/129, 파일 상한, 미해결 꼬리에서 추가 기록 거부를 함께 확인했습니다. 기존 출력 재사용은 종료2로 막아 이전 결과를 유지했습니다. 이는 교육용 결함 주입이며 기존 제품 결함을 발견한 기록이 아닙니다.

## 7. flush와 fsync를 호출한 범위

`flush()`는 Python 출력 버퍼를 비우고 `os.fsync()`는 호스트에 파일 동기화를 요청합니다. Python 3.12 문서는 Unix에서는 fsync, Windows에서는 MS _commit을 사용한다고 구분합니다. 실제 실행은 Windows입니다. Linux fsync 문서는 파일의 동기화와 디렉터리 항목의 동기화를 구분합니다. [Python os.fsync](https://docs.python.org/3.12/library/os.html#os.fsync), [Linux man-pages fsync](https://man7.org/linux/man-pages/man2/fsync.2.html)

여기서는 성공한 동기화 뒤 자식만 명시 종료합니다. 동기화 도중의 전원 제거·directory fsync·sector tearing·장치 volatile cache·쓰기 재정렬·flash erase 단위·wear를 시험하지 않았습니다. SQLite의 Atomic Commit 문서는 실제 crash test에서 VFS로 불완전 sector·쓰레기·순서 변경을 따로 주입한다고 설명합니다. 그 시험과 이 단순 prefix 시험의 범위를 같게 보지 않습니다. [SQLite Atomic Commit §3.7~3.11·8·9.2](https://www.sqlite.org/atomiccommit.html)

## 확인 문제

1. DATA CRC가 맞으면 새 값을 읽어도 되나요? 아닙니다. 같은 seq와 DATA CRC를 가리키는 완전한 COMMIT까지 확인해야 합니다.
2. 끝 frame의 자료가 부족하면 실제 중단이라고 확정할 수 있나요? 아닙니다. 길이 손상도 같은 모양을 만들 수 있으며 이 사례에 한계 대조가 있습니다.
3. cut59에서 자식이 종료23이면 이전 상태인가요? 아닙니다. 59바이트 전체가 남아 seq2로 복구됩니다. 응답 상실과 미확정 기록을 구분합니다.

## English

A two-key redo journal separates staged DATA from confirmed state. Fresh processes replay only matching DATA/COMMIT sequences after framing, size and CRC checks. All sixty prefixes of one 59-byte update preserve either the previous state or the fully committed new state. Complete-frame corruption is rejected without resynchronization, while a legal-range damaged length can resemble an incomplete tail; this is demonstrated explicitly. Four mutations fail under normal and optimized execution. Flushed host files and explicit child termination are not hardware power-loss or filesystem-durability validation.

## 읽은 판본과 범위

2026-10-21에 SQLite 공식 Atomic Commit 온라인 문서의 §1·3.5~3.11·4.1~4.2·8·9.2, Database File Format의 §4.1·4.3·4.5를 읽었습니다. 두 온라인 문서에 특정 SQLite 실행 버전이 붙었다고 쓰지 않으며 SQLite 라이브러리는 실행하지 않았습니다. WAL 형식의 3007000은 파일 형식 번호입니다. Linux man-pages6.19의 fsync(2), 2026-02-08 본문 DESCRIPTION·RETURN VALUE·ERRORS와 Python3.12 문서의 os.fsync·os._exit도 확인했습니다. Python 문서 화면은3.12.15이고 실제 로컬 런타임은3.12.14입니다.
