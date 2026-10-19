# 자동화의 기본: 검증, 재실행과 원자적 게시

[Automation & Portfolio](../README.md) · [게시 구현](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [실패 조건 테스트](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 실행 횟수보다 결과의 조건을 먼저 정합니다

CI는 변경을 통합할 때 빌드·검증을 반복하는 체계입니다. 작업이 자동 실행되었다는 사실과 올바른 산출물이 게시되었다는 사실은 다릅니다. 입력 고정, 생성, 검사, 게시를 구분하면 어느 단계에서 잘못되었는지 찾기 쉽습니다. GitHub Actions의 `needs`는 선행 job의 성공을 의존 조건으로 두지만, 조건식이나 오류 무시 설정을 바꾸면 실패 전파도 달라질 수 있습니다. [GitHub workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

검사에서 실패했는데 게시가 계속되거나, 테스트한 파일과 다른 파일을 다시 빌드해 배포하면 검사의 의미가 줄어듭니다. 검증한 산출물의 digest와 실제 게시 대상을 연결하고, 실패한 단계의 로그·종료 상태를 남깁니다. 캐시는 성능을 위한 수단이지 누락된 입력 정의나 검증을 대체하는 증거가 아닙니다.

### 재실행해도 같은 상태가 되게 하기

idempotency는 같은 요청을 반복했을 때 의도한 최종 효과가 한 번 적용한 것과 같은 성질입니다. 로그 줄이나 실행 시간까지 모두 같다는 뜻은 아닙니다. 같은 문서의 같은 내용으로 목표 상태를 맞추는 작업과, 매번 항목을 append하는 작업은 다릅니다. 네트워크 timeout 뒤에 재시도하면 앞 요청이 이미 성공했을 수도 있으므로 효과를 기준으로 설계합니다.

파일 생성에서는 정렬된 key, 고정 인코딩·줄바꿈, 명시한 입력이 같은 바이트를 만들게 할 수 있습니다. 업무 요청의 중복 방지는 별도의 요청 식별자·저장된 처리 결과 등이 필요할 수 있습니다. 문서 파일 한 개를 같은 내용으로 다시 쓰는 예제로 결제나 외부 서비스의 exactly-once 처리가 해결되었다고 일반화하지 않습니다.

### 반쯤 쓴 파일을 보이지 않게 하기

대상 파일을 바로 열어 덮어쓰면 중간 실패에서 내용 일부만 남을 수 있습니다. 작은 파일 한 개의 게시는 먼저 같은 디렉터리의 임시 파일에 완성하고, 검증 후 이름을 교체하는 방식으로 구성할 수 있습니다. 성공한 POSIX rename의 원자성은 독자가 이름을 통해 불완전한 중간 파일을 보는 문제를 줄입니다. 다른 filesystem 사이의 이동에는 같은 보장이 적용되지 않을 수 있습니다. [Linux rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html), [Python os.replace](https://docs.python.org/3/library/os.html#os.replace)

원자적 가시성과 전원 손실 뒤의 내구성도 다른 조건입니다. 파일 `fsync`만으로 모든 filesystem의 디렉터리 메타데이터·저장장치 동작까지 보장하지 않습니다. 여러 파일을 한 번에 일관되게 게시하려면 버전별 디렉터리와 최종 참조 교체 같은 별도 설계가 필요합니다. 두 작성자가 동시에 게시할 때 오래된 작업이 최신 결과를 덮는 문제도 이름 교체만으로 막지 못합니다.

### 구현과 실패 주입

`publish_json`은 payload 검증, 결정적 JSON 인코딩, 동일 바이트이면 종료, 같은 디렉터리 임시 파일 작성·flush·fsync, `os.replace`의 순서입니다. NaN은 JSON에서 거부합니다. 작업 중 예외가 생기면 임시 파일을 정리합니다. 부모 디렉터리가 이미 있고 대상이 관리되는 일반 파일이라는 범위의 예제이며, hostile path·동시 작성자·전체 디렉터리 transaction을 구현하지 않습니다.

테스트는 같은 내용을 key 순서만 바꾸어 재실행하면 변경 없음이 반환되는지, 검증 실패와 교체 실패에서 이전 파일이 유지되는지 확인합니다. 교체 실패는 mock으로 주입하므로 실제 전원 차단·파일시스템 충돌 시험은 아닙니다. 실행 환경에서의 바이트·실패 동작 검증과 플랫폼의 원자성 규약을 구분합니다.

```bash
# 저장소 루트에서 표준 라이브러리 검증을 실행한다.
python -m unittest discover -s 예제_examples/확장기초_extended/systems -p 'test_*.py' -v
```

이 검증을 CI에서 필수 성공 조건으로 연결할 수 있습니다. 이 글은 실행되는 workflow를 저장소에 새로 설치하거나 외부 게시 작업을 수행한 기록은 아닙니다.

## English

### Define successful effects before scheduling runs

CI repeatedly builds and checks changes. An automated run is not equivalent to correct publication. Separate fixed inputs, generation, validation, and publication. GitHub Actions `needs` can require successful predecessor jobs, while conditionals and ignored errors can change failure propagation. [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

Publishing after failed checks, or rebuilding a different artifact after testing, weakens the evidence. Connect validated digests to published artifacts and preserve exit status and logs. A cache improves performance; it does not replace defined inputs or validation.

### Make retries converge

Idempotency concerns the same intended final effect after repeated requests, not identical timing or logs. Converging a document to specified content differs from appending on every run. A timeout can follow a successful request, making retry behavior important.

Stable key order, encoding, line endings, and inputs can yield identical file bytes. External operations may require request identifiers and stored outcomes. A local document example does not establish exactly-once payments or remote-service behavior.

### Avoid publishing a partial file

Direct overwriting can leave partial output after failure. A single-file strategy writes a complete temporary file in the destination directory, validates it, then replaces the name. A successful POSIX rename is atomic; cross-filesystem moves need not share the same guarantee. [rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html), [os.replace](https://docs.python.org/3/library/os.html#os.replace)

Atomic visibility differs from power-loss durability. File fsync alone does not establish all directory-metadata and storage guarantees. Consistent multi-file releases need another design, such as versioned directories plus a final reference switch. Atomic replacement also does not stop an old concurrent writer overwriting a newer result.

### Implementation and fault injection

`publish_json` validates, canonically encodes JSON, skips identical bytes, writes and syncs a same-directory temporary file, and calls `os.replace`. It rejects NaN and cleans temporary output after exceptions. Its scope is a managed ordinary file with an existing parent, not hostile paths, concurrent writers, or directory transactions.

Tests check content-order-independent repetition and preservation of old output after validation or replacement failure. A mock injects replacement failure; no power-loss or filesystem-crash experiment is claimed. Distinguish observed functional behavior from platform atomicity contracts.

The command runs portable tests that can become a required CI gate. This article does not install a live workflow or perform external publication.

## 출처 / Sources

GitHub의 작업 의존성, Python 교체 API, Linux 이름 교체 규약의 보장 범위를 나누어 대조했습니다. / Job gating, API behavior, and filesystem guarantees were cross-checked separately. 확인 / checked: 2026-10-19.
