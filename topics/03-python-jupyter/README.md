# Python & Jupyter

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

Python은 자동화, 데이터 분석, 수치 계산, AI 모델 개발을 연결하기 좋은 언어다. Jupyter Notebook은 코드·설명·수식·그래프를 셀 단위로 구성하는 문서 형식이며, JupyterLab은 노트북과 파일·터미널을 함께 다루는 작업 환경이다. 실제 코드는 커널이라는 별도 실행 프로세스에서 실행된다.

## 환경을 나누는 이유

프로젝트마다 필요한 라이브러리 버전이 다르다. `venv`는 Python 패키지 환경을 분리하고, pip는 패키지를 설치한다. Conda·Mamba는 Python 외의 바이너리 의존성도 환경 단위로 관리한다. uv는 Python 프로젝트와 의존성 관리에 쓰이는 도구다.

아래는 Python 3가 설치된 Linux·Bash 환경의 예다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install jupyterlab ipykernel numpy scipy pandas matplotlib
python -m ipykernel install --user --name engineering-notes
python -m jupyterlab
```

Windows PowerShell에서는 가상환경 생성에 `py -m venv .venv`, 활성화에 `.\.venv\Scripts\Activate.ps1`을 사용한다. 노트북의 커널과 패키지를 설치한 Python이 일치하는지는 `import sys; print(sys.executable)`로 확인할 수 있다.

## 계산과 시각화

NumPy는 배열과 벡터 연산, SciPy는 최적화·적분·신호처리, pandas는 표 형태 데이터, Matplotlib·Seaborn·Plotly는 그래프에 쓰인다. 배열의 모양과 축을 이해하면 표본·채널·시간·특징 차원이 섞이는 오류를 줄일 수 있다.

```python
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0.0, 0.01, 1001)
v = 3.3 * (1.0 - np.exp(-t / 0.001))
plt.plot(t * 1000, v)
plt.xlabel("Time [ms]")
plt.ylabel("Voltage [V]")
plt.grid(True)
plt.show()
```

노트북은 셀을 실행한 순서에 따라 상태가 남는다. 커널을 재시작하고 위에서 아래로 실행했을 때도 같은 계산이 성립해야 문서의 흐름과 실행의 흐름이 일치한다. PyTorch·TensorFlow의 GPU 설치는 프레임워크별 설치 문서에서 운영체제와 드라이버 지원을 확인하는 별도 단계다.

## 관련 기술

Python, pip, uv, venv, Conda/Mamba, Jupyter Notebook/Lab, IPython, NumPy, SciPy, pandas, Matplotlib, Seaborn, Plotly

## 참고 자료

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Installing Jupyter](https://jupyter.org/install)
- [NumPy documentation](https://numpy.org/doc/)
