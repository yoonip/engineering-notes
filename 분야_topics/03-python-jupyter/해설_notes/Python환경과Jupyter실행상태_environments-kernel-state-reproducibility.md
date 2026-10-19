# Python 환경과 Jupyter 실행 상태를 구분하기

[Python & Jupyter](../README.md) · [실행 모형](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [검증 코드](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 설치한 Python과 노트북의 Python이 같을까

Python 인터프리터는 코드를 실행하고, 패키지는 그 인터프리터가 찾는 경로에 설치된다. Jupyter의 화면과 코드를 실행하는 kernel은 별개다. 브라우저에서 같은 노트북을 열었어도 선택된 kernel이 다른 환경을 가리키면 import 결과와 패키지 버전이 달라진다. IPython은 Jupyter에서 Python 실행을 맡는 kernel 구현이다. [IPython kernel 설치](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)

`venv`는 Python 설치를 바탕으로 별도 패키지 경로를 갖는 가상환경을 만든다. 활성화는 보통 그 환경의 실행 파일 경로를 PATH 앞에 놓는 편의 기능이다. 활성화 없이도 환경의 Python을 직접 실행할 수 있다. 환경 폴더를 다른 PC에 복사하기보다 같은 입력 목록으로 다시 만드는 편이 맞다. 절대 경로를 사용하는 스크립트 등이 있어 일반적으로 이동 가능한 묶음이 아니기 때문이다. 가상환경은 보안 격리 장치나 GPU 드라이버까지 포함한 운영체제 복제본도 아니다. [Python venv](https://docs.python.org/3/library/venv.html)

### 실행 파일을 기준으로 연결하기

다음은 POSIX 셸에서 새 환경을 만드는 절차다. `requirements.txt`에는 프로젝트에 맞게 검토한 의존성 목록이 있어야 한다.

```bash
# 환경의 실행 파일을 직접 지정해 설치 대상을 분명히 한다.
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install ipykernel
.venv/bin/python -m ipykernel install --user --name engineering-local --display-name "Engineering local"
```

Windows PowerShell에서는 `.venv/bin/python` 대신 `.venv\Scripts\python.exe`를 사용한다. 노트북에서 `sys.executable`, `sys.version`, 주요 패키지 버전을 읽어 선택한 kernel을 확인한다. 표시 이름만 믿지 않는다. `python -m pip`의 장점은 pip가 어느 Python에 속하는지 명시하는 데 있으며, 버전 고정·의존성 잠금·다운로드 파일의 검증까지 자동 해결하는 것은 아니다. kernel 등록 이름이 같으면 기존 등록을 덮어쓸 수 있다는 점도 구분한다. [IPython 등록 규칙](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)

### 셀의 위치와 실행 순서는 다르다

첫 셀에서 `x = 1`, 다음 셀에서 `x += 2`를 실행하면 3이다. 두 번째 셀만 다시 실행하면 5가 된다. 파일에 표시된 코드가 같아도 kernel에 남은 상태가 달라 결과가 바뀐다. 삭제한 셀이 만든 변수도 kernel을 재시작하기 전까지 남을 수 있다.

이를 막는 기본 조건은 깨끗한 kernel에서 위에서 아래로 한 번 실행했을 때 필요한 입력과 결과가 모두 생기는 것이다. 긴 계산은 `result = analyze(data, config)`처럼 입력·출력을 드러내는 함수로 옮기면 상태 의존성을 줄일 수 있다. 데이터 경로, 난수 seed, 시간대와 라이브러리 버전도 기록한다. seed 하나만 같다고 병렬 연산·GPU·서로 다른 라이브러리에서 비트 단위 일치가 보장되지는 않는다. JupyterLab의 연결된 콘솔은 kernel에서 실제로 실행된 순서를 확인하는 데도 쓰인다. [JupyterLab 노트북과 실행 이력](https://jupyterlab.readthedocs.io/en/stable/user/notebook.html)

### 무엇을 검증했는지 남기기

예제 `run_cells`는 변수 설정과 더하기만 가진 작은 상태 모형이다. 순서를 바꾸면 정의되지 않은 이름이 나타나고, 추가 셀을 반복하면 결과가 달라지는지 테스트한다. Python이나 Jupyter 전체를 구현한 모형은 아니다.

실제 노트북의 재현성은 새 환경·새 kernel에서 실행하고, 입력 digest와 결과의 허용 오차·형태를 대조해야 한다. HTML에 출력이 보인다는 사실만으로 현재 코드의 실행 성공이라고 판단하지 않는다. 이 묶음에서 실행한 것은 표준 라이브러리 모형 테스트이며, 위 설치 명령이나 별도 노트북 실행의 성공을 주장하지 않는다.

## English

### The notebook's Python can differ from the installed one

An interpreter executes code and searches its own package paths. The Jupyter interface and execution kernel are separate. Opening the same notebook with a different kernel can change imports and versions. IPython implements a Python kernel for Jupyter. [IPython kernel installation](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)

`venv` creates separate package paths based on an existing Python installation. Activation mainly adjusts PATH; directly calling the environment's interpreter also works. Recreate an environment from its inputs instead of assuming its directory can be copied between computers: installed scripts can contain absolute paths. A virtual environment is neither a security sandbox nor an operating-system image containing GPU drivers. [venv](https://docs.python.org/3/library/venv.html)

### Connect tools through the interpreter

The POSIX commands create `.venv`, install reviewed dependencies and `ipykernel`, then register that interpreter. In Windows PowerShell, replace `.venv/bin/python` with `.venv\Scripts\python.exe`. Inspect `sys.executable`, `sys.version`, and relevant package versions inside the notebook rather than trusting a display name. `python -m pip` clarifies the installation target; it does not itself lock dependency resolution or validate downloads. Reusing a kernel registration name can overwrite its existing entry. [Registration rules](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)

### Cell position is not execution history

Running `x = 1` and then `x += 2` gives three. Rerunning only the second cell gives five. A deleted cell's variables can also remain until the kernel restarts. Identical visible code therefore need not imply identical hidden state.

A basic reproducibility condition is that a clean kernel can execute the notebook once from top to bottom with explicit inputs. Moving substantial work into functions such as `analyze(data, config)` makes dependencies clearer. Record data paths, seeds, time zones, and library versions. A shared seed alone does not guarantee bit-identical parallel or GPU computation across implementations. JupyterLab's attached console can show the kernel's actual execution history. [JupyterLab notebooks and history](https://jupyterlab.readthedocs.io/en/stable/user/notebook.html)

### Verification scope

`run_cells` models only assignment and addition. Tests expose undefined names after reordering and changed results after repeating a cell. It is not a Python or Jupyter implementation.

A real notebook check needs a recreated environment and fresh kernel, followed by comparison of input digests and specified output shapes and tolerances. Saved HTML output does not prove the current code runs. This package executes portable model tests; it makes no claim that the installation commands or an external notebook were run successfully.

## 출처 / Sources

Python의 환경 규칙, IPython의 kernel 등록, Jupyter의 실행 절차를 대조했다. / Environment, kernel registration, and notebook execution were checked separately. 확인 / checked: 2026-10-19.
