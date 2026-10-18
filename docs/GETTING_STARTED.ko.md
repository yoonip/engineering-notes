# GitHub 처음 올리기 — 파일을 하나씩 만들 필요 없습니다

이 묶음은 로컬 파일만 준비합니다. GitHub 계정이나 기존 저장소는 변경하지 않았습니다.

## 가장 쉬운 방법: 브라우저로 한 번에 업로드
1. ZIP을 압축 해제합니다.
2. GitHub 화면 오른쪽 위 **+ → New repository**를 누릅니다.
3. Owner는 본인 계정, Repository name은 **engineering-notes**로 설정합니다.
4. 채용용 공개 저장소라면 Public을 고릅니다. 아직 비공개로 준비하고 싶으면 Private도 가능합니다.
5. README, .gitignore, license 자동 생성 옵션은 선택하지 않고 **Create repository**를 누릅니다.
6. 빈 저장소 안내의 **uploading an existing file**을 누릅니다. 이미 파일이 있다면 **Add file → Upload files**입니다.
7. 압축 해제한 `engineering-notes` 폴더 **안으로 들어가서** 파일과 폴더를 모두 선택해 업로드 영역으로 끌어 놓습니다.
8. README.md와 topics/ 등이 저장소 최상위에 들어가는지 확인합니다. 바깥쪽 engineering-notes 폴더 자체를 넣어 한 단계 더 중첩시키지 마세요.
9. 커밋 메시지 예: `Add engineering learning catalog and templates`.
10. **Commit changes** 또는 새 브랜치로 올리는 경우 **Propose changes**를 눌러 완료합니다.

ZIP 파일 자체만 올리면 GitHub가 목차 폴더로 풀어주지 않습니다. 압축 해제한 내용물을 올려야 합니다.
GitHub 공식 안내의 브라우저 동시 업로드 한도는 100개 파일입니다. 이 묶음의 저장소 파일은 그보다 적습니다.

## 자동화 방법: Git + GitHub CLI
사전 준비: Git과 GitHub CLI(gh)가 설치되어 있어야 합니다.
- Git: https://git-scm.com/downloads/win
- GitHub CLI: https://cli.github.com/

GitHub CLI의 로그인은 사용자가 본인 브라우저에서 완료합니다. ZIP을 푼 최상위 폴더에서 터미널을 열고 다음을 실행합니다.

```powershell
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
```

같은 폴더의 `Publish-ToGitHub.ps1`은 기본 실행 시 예정 작업만 표시합니다. 실제 생성/업로드는 `-Publish`를 붙여 실행합니다.
Windows PowerShell의 실행 정책 때문에 필요한 경우, 아래 명령의 Bypass는 이 프로세스에만 적용됩니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Publish-ToGitHub.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Publish-ToGitHub.ps1 -Publish -Visibility public
```

이 스크립트는 gh에 로그인된 실제 계정을 확인하고, 바로 옆의 engineering-notes 폴더만 Git 저장소로 만듭니다.
본인 계정에 engineering-notes를 생성하고 초기 커밋을 올립니다. 이후 같은 폴더에서 다시 실행하면 변경분을 커밋하고 일반 push합니다.
다른 폴더를 스테이징하거나 기존 원격 저장소를 지우거나 강제 push하지 않습니다.
웹에서 이미 같은 이름의 저장소를 만들었다면 새 저장소 생성 방식과 중복되므로 브라우저 방식으로 업로드하거나 기존 저장소를 clone해서 사용하세요.

## 왼쪽 NNbich2511/trans_sysc는 무엇인가
표기는 `소유자 ID / 저장소 이름`입니다. NNbich2511은 소유자, trans_sysc는 저장소 이름입니다.
스크린샷만으로 이 소유자가 본인인지, 협업자로 접근한 것인지 판단할 수 없습니다.
홈의 Top repositories는 활동을 바탕으로 자동 생성되고, 공개 프로필의 대표 저장소 목록과 다릅니다.
공식 안내상 이 목록은 직접 편집할 수 없으며 마지막 상호작용으로부터 1년이 지나면 목록에서 빠집니다.
공개 프로필과 자신이 만든 저장소는 오른쪽 위 프로필 아이콘에서 Your profile / Your repositories로 확인합니다.
협업 관계를 끝내려는 경우 Settings → Repositories에서 해당 저장소의 Leave를 사용할 수 있지만, 홈 목록이 즉시 사라진다는 보장은 없습니다.
소유권과 내용 확인 없이 기존 저장소를 삭제하지 마세요.
