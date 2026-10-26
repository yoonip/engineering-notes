# 개발 환경의 구성

개발 환경은 운영체제, 도구, 의존성, 실행 자원으로 이루어집니다. Editor가 소스를 다루고 compiler·interpreter가 실행을 준비하며, package manager가 라이브러리를 관리합니다.

## 환경의 층

Linux·WSL은 운영체제 환경, GCC·Clang은 compiler, Python은 interpreter, venv·Conda는 프로젝트 의존성을 나누는 환경입니다. Jupyter의 kernel은 실제 코드를 실행하는 프로세스입니다. GPU 계산에는 driver·runtime·framework 사이의 지원 조건도 추가됩니다.

- [Linux & Bash](../전자컴퓨터공학_ece/01-linux-bash/README.md)
- [Git과 빌드 도구](../전자컴퓨터공학_ece/02-개발도구_git-development-tools/README.md)
- [Python 가상환경과 Jupyter 설치](../전자컴퓨터공학_ece/03-python-jupyter/README.md)
- [CUDA 실행 구조](../전자컴퓨터공학_ece/25-CUDA성능최적화_cuda-performance/README.md)

## 재현에 필요한 정보

소스 revision은 코드의 기준을, package version은 라이브러리의 기준을, configuration은 실행 선택을 나타냅니다. 같은 코드도 운영체제·CPU/GPU·입력 데이터·random seed에 따라 다른 결과를 낼 수 있습니다. 환경 정보는 이 차이를 해석하는 근거입니다.

## Python 프로젝트를 따라 설정하기

가상환경은 프로젝트가 사용할 Python 실행 파일과 라이브러리를 구분하는 디렉터리입니다. 운영체제를 새로 만드는 가상 머신과는 다릅니다. 아래 명령은 Python이 설치되어 있고 `python` 명령으로 실행되는 경우의 예입니다. 작업할 프로젝트 디렉터리에서 한 줄씩 실행합니다.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
.\.venv\Scripts\python.exe -m pip --version
```

`--version`은 버전을 표시하는 옵션입니다. `-m venv`는 선택한 Python으로 표준 라이브러리의 venv 모듈을 실행합니다. `.venv`는 생성할 디렉터리 이름입니다. `-c` 뒤의 문자열은 짧게 실행할 Python 코드입니다. `import sys`는 실행 환경 정보를 제공하는 표준 모듈을 불러오고, `sys.executable`은 현재 실행 파일의 경로를 나타냅니다.

macOS·Linux에서는 마지막 두 줄의 실행 파일을 `.venv/bin/python`으로 바꿉니다. 가상환경을 활성화하지 않아도 실행 파일 경로를 직접 지정하면 사용할 수 있습니다. 이 방식은 PowerShell의 활성화 스크립트 실행 정책을 바꾸지 않고도 어느 Python을 쓰는지 분명히 할 수 있습니다. [Python의 venv 설명](https://docs.python.org/3/library/venv.html)에 생성과 활성화 방식이 정리되어 있습니다.

라이브러리가 필요한 프로젝트라면 해당 환경의 `python -m pip install -r requirements.txt`로 요구 사항을 설치합니다. 이 파일이 실제로 있는지와 그 프로젝트가 지정한 설치법을 먼저 확인합니다. 프로젝트가 다른 패키지 관리 도구나 잠금 파일을 사용한다면 그 방식을 따릅니다. 위 명령을 이유 없이 관리자 권한으로 실행할 필요는 없습니다.

## 설치했는데 import가 실패할 때

| 관찰 | 확인할 것 | 이유 |
|---|---|---|
| 터미널에서는 되는데 편집기에서 실패합니다. | 편집기가 선택한 인터프리터 경로 | 서로 다른 Python일 수 있습니다. |
| 설치 성공 뒤에도 모듈을 찾지 못합니다. | `python -m pip --version`의 경로 | 설치 대상과 실행 대상이 다를 수 있습니다. |
| 노트북에서만 예전 결과가 나옵니다. | 커널의 실행 파일과 이전 셀 상태 | 화면의 노트북과 실제 실행 프로세스는 별개입니다. |
| 실행 위치에 따라 파일을 찾지 못합니다. | 현재 작업 디렉터리와 상대 경로 | 소스 파일 위치와 작업 디렉터리가 항상 같지는 않습니다. |

패키지 이름과 `import`에 쓰는 모듈 이름이 다른 경우도 있습니다. 오류 문구만 보고 비슷한 이름의 패키지를 임의로 설치하기보다 프로젝트 문서와 공식 배포 정보를 확인합니다. 패키지를 설치한 사실만으로 버전 호환성과 실행 성공이 보장되지는 않습니다. [pip 사용 안내](https://pip.pypa.io/en/stable/user_guide/)도 설치 대상을 확인할 때 참고하실 수 있습니다.

## 재현 기록의 작은 예

실행 기록에는 코드 커밋, Python 버전, 패키지 목록, 실행 명령, 입력 식별자, 필요한 하드웨어를 함께 남깁니다. `pip freeze`는 설치된 Python 패키지 버전을 보여 주지만 운영체제 라이브러리·GPU 드라이버·데이터를 모두 기록하는 도구는 아닙니다. 비밀 키나 계정 토큰을 기록 파일에 넣지 않습니다.

직접 작성한 소스는 `.venv` 밖에 두고, 다른 컴퓨터에서는 환경을 통째로 복사하기보다 같은 조건으로 다시 만듭니다. 환경 폴더에 절대 경로가 포함될 수 있기 때문입니다.

## 확인 문제

1. 편집기와 터미널의 Python 버전이 같으면 실행 파일도 반드시 같나요?
2. `python -m pip`에서 `python`을 지정하는 이유는 무엇인가요?
3. 패키지 버전 목록만 있으면 입력 데이터와 GPU 드라이버 정보가 없어도 모든 실험이 재현되나요?

<details>
<summary>답과 풀이</summary>

1. 아닙니다. 같은 버전의 서로 다른 가상환경일 수 있으므로 경로도 확인합니다.
2. 선택한 Python에 연결된 pip를 실행해 설치 대상을 분명히 하려는 목적입니다.
3. 아닙니다. 데이터·실행 선택·외부 라이브러리·하드웨어 등 결과에 영향을 주는 조건이 더 있습니다.

</details>

## English

A development environment combines an operating system, tools, dependencies, and computing resources. An editor handles source files, a compiler or interpreter prepares or runs them, and a package manager manages libraries.

### How the layers fit together

Linux and WSL provide operating environments. GCC and Clang are compilers; Python is an interpreter. venv and Conda separate project dependencies. A Jupyter kernel is the process that actually runs notebook code. GPU work adds compatibility requirements between the driver, runtime, and framework.

- [Linux and Bash](../전자컴퓨터공학_ece/01-linux-bash/README.md)
- [Git and build tools](../전자컴퓨터공학_ece/02-개발도구_git-development-tools/README.md)
- [Python environments and Jupyter](../전자컴퓨터공학_ece/03-python-jupyter/README.md)
- [CUDA execution](../전자컴퓨터공학_ece/25-CUDA성능최적화_cuda-performance/README.md)

### What makes a run reproducible

The source revision identifies the code, package versions identify the libraries, and the configuration records execution choices. The same code can produce different results with a different operating system, CPU or GPU, input dataset, or random seed. Recording these details makes those differences easier to understand.
