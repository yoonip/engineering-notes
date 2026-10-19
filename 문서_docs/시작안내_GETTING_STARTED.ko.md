# 개발 환경의 구성

개발 환경은 운영체제, 도구, 의존성, 실행 자원으로 이루어진다. Editor가 소스를 다루고 compiler·interpreter가 실행을 준비하며, package manager가 라이브러리를 관리한다.

## 환경의 층

Linux·WSL은 운영체제 환경, GCC·Clang은 compiler, Python은 interpreter, venv·Conda는 프로젝트 의존성을 나누는 환경이다. Jupyter의 kernel은 실제 코드를 실행하는 프로세스다. GPU 계산에는 driver·runtime·framework 사이의 지원 조건도 추가된다.

- [Linux & Bash](../분야_topics/01-linux-bash/README.md)
- [Git과 빌드 도구](../분야_topics/02-개발도구_git-development-tools/README.md)
- [Python 가상환경과 Jupyter 설치](../분야_topics/03-python-jupyter/README.md)
- [CUDA 실행 구조](../분야_topics/25-CUDA성능최적화_cuda-performance/README.md)

## 재현에 필요한 정보

소스 revision은 코드의 기준을, package version은 라이브러리의 기준을, configuration은 실행 선택을 나타낸다. 같은 코드도 운영체제·CPU/GPU·입력 데이터·random seed에 따라 다른 결과를 낼 수 있다. 환경 정보는 이 차이를 해석하는 근거다.

## English

A development environment combines an operating system, tools, dependencies, and computing resources. An editor handles source files, a compiler or interpreter prepares or runs them, and a package manager manages libraries.

### How the layers fit together

Linux and WSL provide operating environments. GCC and Clang are compilers; Python is an interpreter. venv and Conda separate project dependencies. A Jupyter kernel is the process that actually runs notebook code. GPU work adds compatibility requirements between the driver, runtime, and framework.

- [Linux and Bash](../분야_topics/01-linux-bash/README.md)
- [Git and build tools](../분야_topics/02-개발도구_git-development-tools/README.md)
- [Python environments and Jupyter](../분야_topics/03-python-jupyter/README.md)
- [CUDA execution](../분야_topics/25-CUDA성능최적화_cuda-performance/README.md)

### What makes a run reproducible

The source revision identifies the code, package versions identify the libraries, and the configuration records execution choices. The same code can produce different results with a different operating system, CPU or GPU, input dataset, or random seed. Recording these details makes those differences easier to understand.
