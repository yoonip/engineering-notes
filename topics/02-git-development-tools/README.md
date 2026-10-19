# Git & Development Tools

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

Git은 파일 변경을 커밋 단위로 관리하는 분산 버전 관리 도구다. 각 커밋은 파일 상태와 이전 커밋의 관계를 기록한다. GitHub와 GitLab은 Git 저장소에 이슈, 코드 리뷰, CI, 권한 관리 같은 협업 기능을 더한 서비스다.

## 작업에서 공유까지

작업 디렉터리에서 수정한 파일을 `git add`로 스테이징하고 `git commit`으로 기록한다. `git push`는 로컬 커밋을 원격 저장소에 전송한다. 파일 저장과 커밋, 원격 전송은 서로 다른 단계다.

```bash
git status
git diff
git add README.md
git diff --staged
git commit -m "Linux 파일 권한 설명 추가"
git push
```

브랜치는 특정 커밋을 가리키는 이름이다. 병합은 갈라진 변경 이력을 합치는 작업이며, 같은 부분의 수정이 충돌하면 최종 내용을 결정해야 한다. Pull Request는 변경을 제안하고 검토하는 GitHub의 기능이다. GitHub CLI는 이런 작업을 명령으로 수행하고, GitHub Desktop은 GUI로 저장소를 관리한다.

## 편집, 빌드, 실행 환경

VS Code·Vim·Neovim은 소스 편집에, GCC·Clang은 C/C++ 컴파일에 쓰인다. Make·Ninja는 빌드 작업을 실행하고, CMake·Meson은 프로젝트의 빌드 구성을 생성한다. 편집기와 컴파일러, 빌드 시스템은 역할이 다르다.

Docker·Podman의 컨테이너는 애플리케이션과 사용자 공간 의존성을 묶는다. 호스트 커널과 GPU 드라이버까지 독립적으로 복제하는 것은 아니므로 컨테이너 이미지와 호스트 조건을 함께 보아야 한다.

## 관련 기술

Git, GitHub, GitLab, GitHub CLI/Desktop, VS Code, Vim/Neovim, GCC, Clang/LLVM, Make, CMake, Meson, Ninja, Docker, Podman

## 참고 자료

- [Pro Git](https://git-scm.com/book/en/v2)
- [GCC language standards](https://gcc.gnu.org/onlinedocs/gcc/Standards.html)
