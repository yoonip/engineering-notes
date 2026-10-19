# SQLite WAL의 동시 접근 | Reviewing SQLite WAL behavior

SQLite는 프로그램 안에서 사용하는 관계형 데이터베이스 엔진입니다. 별도 DB 서버 없이 파일을 사용할 수 있어 로컬 분석 도구와 장치 기록에 적합한 경우가 있습니다. 여기서는 제품의 동시 접근 동작을 두 연결로 확인합니다. Python 3.12.14에 연결된 SQLite 3.53.1을 2026-10-19에 실행했습니다.

## 비교할 동작

공식 [WAL 안내](https://www.sqlite.org/wal.html#concurrency)는 읽기와 쓰기가 겹쳐 진행될 수 있다고 설명합니다. 동시에 진행할 수 있는 쓰기 트랜잭션은 하나입니다. WAL은 수정 내용을 로그에 추가하므로 독자는 자신이 읽기 시작한 시점의 내용을 계속 볼 수 있습니다. [격리 설명](https://www.sqlite.org/isolation.html)은 이러한 snapshot과 새 트랜잭션의 차이를 설명합니다.

직접 만든 실험에서는 값 10을 저장하고 A 연결이 읽기 트랜잭션을 시작합니다. 이어 B 연결에서 값을 20으로 바꿔 commit을 시도합니다. A는 같은 트랜잭션에서 다시 읽고, 이를 끝낸 뒤 새로 읽습니다. 대기 시간을 0으로 두어 잠금 충돌을 즉시 관찰합니다.

| 관찰 | DELETE journal | WAL |
| --- | --- | --- |
| A의 첫 읽기 | 10 | 10 |
| A가 읽는 동안 B의 commit | `SQLITE_BUSY`, B를 rollback합니다. | 성공합니다. |
| A의 같은 트랜잭션 읽기 | 10 | 10 |
| A가 끝낸 뒤 새로 읽기 | 10 | 20 |

DELETE 모드의 마지막 값이 10인 이유는 실패한 B의 변경을 실험에서 rollback했기 때문입니다. WAL에서 같은 읽기가 계속 10인 것은 갱신 실패가 아니라 snapshot 유지입니다. A가 트랜잭션을 끝내고 다시 읽으면 B가 commit한 20을 확인합니다.

## 사용 판단

읽기와 쓰기를 겹치게 해야 하는 로컬 도구라면 WAL을 검토할 이유가 있습니다. 다만 동시 작성자 수를 무제한으로 늘려 주지는 않습니다. 긴 읽기 트랜잭션은 checkpoint 진행을 지연시킬 수 있으므로 처리 후 트랜잭션을 오래 열어 두지 않는 것이 중요합니다. WAL의 공유 메모리 조건 때문에 네트워크 파일시스템을 여러 호스트가 공유하는 구성에도 맞지 않습니다. 이 조건들은 [공식 WAL 문서](https://www.sqlite.org/wal.html)에 명시되어 있습니다.

단순히 journal 모드를 바꾸는 일과 애플리케이션의 오류 처리는 별도입니다. `SQLITE_BUSY`를 만났을 때 재시도할지, 사용자에게 알릴지, 작업을 취소할지는 트랜잭션의 의미에 맞춰 정해야 합니다. 한 건을 두 번 기록해도 되는지 같은 질문은 DB 설정만으로 해결되지 않습니다.

## 재실행과 범위

저장소 루트에서 `python 제품리뷰_reviews/sqlite_concurrency.py`를 실행합니다. [코드](sqlite_concurrency.py)는 임시 파일을 만들고 두 모드의 관찰값을 검사한 뒤 파일을 정리합니다. [원시 결과](sqlite_result.json)에는 실제 Python·SQLite 버전과 설정이 있습니다. Python API의 동작은 해당 실행 버전의 [sqlite3 문서](https://docs.python.org/3.12/library/sqlite3.html)를 함께 확인하실 수 있습니다.

이 실험은 연결 두 개의 동작 확인입니다. 처리량, 전원 차단 내구성, 여러 프로세스의 장시간 부하는 측정하지 않았으므로 그 성능을 비교하는 자료로 사용하지 않습니다. 더 자세한 상태 분석은 [WAL snapshot 해설](../분야_topics/40-데이터베이스데이터공학_databases-data-engineering/해설_notes/WAL스냅샷과버전충돌_wal-snapshots.md)에 있습니다.

## commit과 checkpoint는 다른 일입니다

commit은 트랜잭션을 확정하는 일이고, checkpoint는 로그의 내용을 본 데이터베이스 파일에 옮기는 일입니다. WAL에서는 확정된 변경이 아직 로그에 있어도 새 독자가 그 변경을 읽을 수 있습니다. 따라서 본 파일이 바로 바뀌지 않았다는 사실만 보고 저장 실패로 판단하지 않습니다.

설명용으로 본 파일에 값 10이 있고, 로그에 값 20의 확정 기록과 값 30의 확정 기록이 이어졌다고 하겠습니다. 20 시점에 시작한 독자는 계속 20을 볼 수 있고, 30 이후 새로 시작한 독자는 30을 볼 수 있습니다. 독자의 기준 시점을 보존하는 것과 최신 데이터를 보여 주는 것은 서로 다른 요구입니다.

로그 파일과 공유 메모리 파일의 역할도 다릅니다. `-wal`은 변경 기록을 담고, `-shm`은 WAL 인덱스 등의 공유 상태를 관리하는 데 사용됩니다. 열린 데이터베이스의 본 파일만 임의로 복사해서 완전한 백업이라고 판단하지 않습니다. 실제 백업에는 일관성을 보존하는 공식 API와 해당 버전의 절차를 사용하셔야 합니다.

## 잠금 오류를 재시도할 때의 질문

가상의 주문 기록 프로그램에서 ‘주문 17을 기록합니다’라는 작업이 잠금 때문에 지연됐다고 하겠습니다. 전체 요청을 다시 실행할 때 같은 주문이 중복 저장되면 안 됩니다. 작업을 식별하는 키와 중복 처리 규칙은 데이터베이스의 동시 접근 설정과 함께 설계해야 합니다.

| 질문 | 확인할 이유 |
|---|---|
| 어느 단계에서 실패했나요? | 읽기·쓰기·commit의 실패는 처리 의미가 다를 수 있습니다. |
| 재시도 범위는 어디까지인가요? | 일부 문장만 다시 할지 트랜잭션 전체를 다시 할지 정해야 합니다. |
| 오래 열린 독자가 있나요? | 읽기가 이어져 checkpoint 진행을 제한할 수 있습니다. |
| 동일 작업의 중복을 구분할 수 있나요? | 애플리케이션 요청 재실행과 데이터 중복을 연결해야 합니다. |

`busy_timeout`을 늘리면 일부 일시적인 잠금 충돌을 기다릴 수 있지만, 긴 트랜잭션이나 잘못된 요청 구조를 없애 주지는 않습니다. 서비스 응답 제한과 취소 조건을 함께 고려합니다. 이 글의 timeout 0은 충돌을 즉시 관찰하기 위한 실험 선택이며 운영 환경에 대한 일괄 권장값이 아닙니다.

## 처리량을 비교하려면 더 필요한 것

이번 실험은 10과 20이라는 값의 관찰에 관한 것입니다. 성능 비교를 추가한다면 같은 저장장치와 동기화 설정에서 트랜잭션 크기, 읽기/쓰기 비율, 연결 수, 지속 시간과 지연시간 분포를 맞춰야 합니다. 평균이 같아도 일부 commit이 checkpoint와 겹쳐 늦어지는 현상은 다를 수 있습니다.

예를 들어 가상의 요청 100개 가운데 99개가 1 ms, 하나가 101 ms라면 평균은 2 ms입니다. 평균만 보면 모든 요청이 약 2 ms였다고 오해하기 쉽습니다. 이 예의 수치는 실제 SQLite 측정이 아니라 긴 꼬리 지연을 설명하기 위한 계산입니다.

## 확인 문제

1. WAL의 commit이 성공하면 checkpoint도 반드시 끝났나요?
2. 같은 읽기 트랜잭션이 계속 10을 보는 것은 쓰기가 실패했다는 증거인가요?
3. 위의 가상 100개 요청의 총 시간과 평균은 얼마인가요?

<details>
<summary>답과 풀이</summary>

1. 아닙니다. 확정과 본 파일 반영은 다른 단계입니다.
2. 아닙니다. 기존 읽기의 snapshot이 유지됐을 수 있으므로 새 트랜잭션의 관찰도 확인합니다.
3. 합은 200 ms, 산술평균은 2 ms입니다. 이를 연결을 겹쳐 실행한 실제 전체 처리시간으로 읽으면 안 됩니다.

</details>

## English

Two connections observe a single stored value. A reader holds a transaction while a writer changes 10 to 20. With a zero timeout, DELETE mode returns SQLITE_BUSY and the writer is rolled back. WAL commits successfully, while the existing reader still sees 10 and a new read transaction sees 20. This is a behavioral check on SQLite 3.53.1, not a throughput or crash-durability benchmark. WAL allows reader/writer overlap but retains a single writer and checkpoint considerations.
