# Git 이력과 다시 만들 수 있는 결과물

[Git & Development Tools](../README.md) · [실행 모형](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [검증 코드](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 커밋은 저장 버튼보다 많은 것을 담는다

Git 커밋은 프로젝트의 스냅샷을 가리키는 tree, 부모 커밋, 작성·커밋 정보와 메시지를 연결한다. 파일 내용은 blob, 디렉터리 구조와 파일 이름·모드 등은 tree로 표현된다. 커밋이 이전 커밋 전체를 매번 복사하는 것은 아니다. 내용이 같은 객체를 다시 참조할 수 있다. [Git 공식 교재: Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

부모를 따라가면 방향성 비순환 그래프, DAG가 된다. 최초 커밋은 부모가 없고, 일반 커밋은 보통 하나, merge 커밋은 둘 이상일 수 있다. 브랜치 이름은 이 그래프의 한 커밋을 가리키는 이동 가능한 참조다. 파일 스냅샷이 같아도 부모·메시지·시각이 다르면 커밋 식별자는 달라질 수 있다. rebase가 부모 관계를 바꾸며 새 커밋을 만드는 이유다. [Git 브랜치](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)

그래프를 읽는 불변식은 간단하다. 커밋의 부모는 그 커밋이 기록하는 과거이고, 브랜치를 이동했다고 기존 객체의 내용이 수정되지는 않는다. 작업 디렉터리, 다음 커밋의 준비 상태인 index, 현재 커밋인 HEAD를 나누어야 “저장했는데 왜 커밋에 없지?”라는 혼동도 줄어든다.

```bash
# 저장소 루트에서 현재 상태와 스냅샷의 근거를 읽는다.
git status --short
git log --graph --oneline --decorate -12
git show --no-patch --format=fuller HEAD
git ls-tree HEAD
```

이 명령은 조회 절차다. 실제 출력은 저장소마다 다르며, 짧은 식별자를 영구 기록에 사용할 때는 충돌하지 않는지와 전체 식별자를 함께 보관할 필요가 있다.

### 같은 소스와 같은 결과물은 다른 주장이다

커밋 번호만 같아도 컴파일러, 의존성, 빌드 옵션, 환경 변수, 생성 시각과 입력 데이터가 다르면 결과가 달라질 수 있다. 재현 가능한 빌드는 정해진 소스·환경·절차로 지정한 산출물의 바이트가 다시 같아지는 것을 뜻한다. 과학 실험의 통계적 결과가 허용 오차 안에서 일치한다는 주장과도 구분한다. [Reproducible Builds 정의](https://reproducible-builds.org/docs/definition/)

| 기록 | 필요한 이유 |
| --- | --- |
| 전체 커밋과 변경 여부 | 실제 사용한 소스 구분 |
| 도구·의존성 버전, 옵션 | 번역·실행 조건 구분 |
| 데이터·설정의 digest | 입력이 바뀌었는지 확인 |
| 산출물 목록과 digest | 비교할 결과를 명확히 지정 |

검증은 서로 깨끗한 두 디렉터리에서 같은 입력을 빌드하고 지정 산출물의 바이트나 digest를 비교하는 방식으로 시작한다. 차이가 나면 시간·경로·파일 순서·locale 같은 변동 요인을 분리한다. 같다는 결과도 배포 파일의 작성자 신원이나 프로그램의 안전성을 자동 입증하지 않는다. digest 비교와 서명 검증은 목적이 다르다.

### 작은 구현으로 확인하기

`dependency_order`는 부모 의존성을 가진 모형 그래프를 정렬하고, 정의되지 않은 부모나 순환을 거부한다. 실제 Git 객체를 파싱하는 함수는 아니지만 모든 부모가 자식보다 먼저 나오는 불변식을 확인할 수 있다. 다이아몬드 모양의 분기·병합도 테스트한다.

`snapshot_digest`는 파일명을 정렬하고 이름·내용의 길이를 포함해 SHA-256을 계산한다. `a`+`bc`와 `ab`+`c`처럼 경계가 모호해지는 연결을 피한다. 파일 순서에는 영향받지 않고 내용 변경에는 반응하는지 테스트한다. 이 교육용 형식은 Git 객체 해시 형식이 아니며 파일 모드·심볼릭 링크·외부 의존성을 포함하지 않는다. 실제 재현성 기록은 필요한 입력 범위를 먼저 정의해야 한다.

## English

### A commit contains relationships as well as content

A Git commit connects a snapshot tree, parent commits, author/committer information, and a message. Blobs store content; trees describe names, modes, and directory relationships. Objects can be reused rather than copying all history for every commit. [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)

Following parents gives a directed acyclic graph. A root has no parents, an ordinary commit commonly has one, and a merge can have several. A branch is a movable reference to a commit. Identical file snapshots need not mean identical commits because parents and metadata matter. Rebase creates new commits by changing these relationships. [Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)

Moving a reference does not modify an existing object's content. Distinguish the working directory, the index prepared for the next commit, and HEAD. The read-only commands above inspect those states and the recorded snapshot. Output depends on the repository; preserve a full identifier when a durable unambiguous reference is needed.

### Same source is not yet the same artifact

A commit alone does not fix compilers, dependencies, options, environment variables, timestamps, or data. A reproducible build recreates bit-identical specified artifacts from defined source, environment, and instructions. Agreement of a scientific estimate within a tolerance is a different reproducibility claim. [Reproducible Builds](https://reproducible-builds.org/docs/definition/)

Record the full commit and local changes, tool/dependency versions, options, input and configuration digests, and exactly which output files are compared. Build in two clean directories, then compare artifact bytes or digests. Investigate timestamps, paths, ordering, and locale when they differ. Equality does not by itself authenticate the publisher or prove software safety; signatures and content comparison serve different purposes.

### Executable checks

`dependency_order` checks a model DAG, requiring parents to precede children and rejecting missing dependencies or cycles. Tests cover a branch/merge diamond. It does not parse Git objects.

`snapshot_digest` sorts file names and includes name/content lengths before hashing with SHA-256, avoiding ambiguous concatenations. Tests check ordering independence and sensitivity to changed names or bytes. The format is not Git's object-hash format, and it excludes modes, symlinks, and external dependencies. Define the required input scope before making a real build-reproducibility claim.

## 출처 / Sources

Git 객체·브랜치 규약과 Reproducible Builds의 산출물 정의를 나누어 대조했다. / Git object/reference semantics were separated from artifact reproducibility. 확인 / checked: 2026-10-19.
