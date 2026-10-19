# 개발 환경의 구성

개발 환경은 운영체제, 도구, 의존성, 실행 자원으로 이루어진다. Editor가 소스를 다루고 compiler·interpreter가 실행을 준비하며, package manager가 라이브러리를 관리한다.

## 환경의 층

Linux·WSL은 운영체제 환경, GCC·Clang은 compiler, Python은 interpreter, venv·Conda는 프로젝트 의존성을 나누는 환경이다. Jupyter의 kernel은 실제 코드를 실행하는 프로세스다. GPU 계산에는 driver·runtime·framework 사이의 지원 조건도 추가된다.

- [Linux & Bash](../topics/01-linux-bash/README.md)
- [Git과 빌드 도구](../topics/02-git-development-tools/README.md)
- [Python 가상환경과 Jupyter 설치](../topics/03-python-jupyter/README.md)
- [CUDA 실행 구조](../topics/25-cuda-performance/README.md)

## 재현에 필요한 정보

소스 revision은 코드의 기준을, package version은 라이브러리의 기준을, configuration은 실행 선택을 나타낸다. 같은 코드도 운영체제·CPU/GPU·입력 데이터·random seed에 따라 다른 결과를 낼 수 있다. 환경 정보는 이 차이를 해석하는 근거다.
