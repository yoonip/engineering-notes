# 기초 모델과 검증 예제

[개념 문서 24편](../../공학기초_foundations/README.md) · [검토 범위와 출처](../../공학기초_foundations/검증기록_VERIFICATION.md) · [English](#english)

개념을 식으로 옮기고, 식을 프로그램으로 만들고, 별도의 기준과 비교하는 예제입니다. 계산에는 Python 표준 라이브러리만 사용합니다. 도표를 다시 그릴 때만 Matplotlib이 추가로 필요합니다.

## 전체 검사

저장소 루트에서 실행합니다. Python 3.12 이상을 기준으로 작성했습니다.

```bash
python 예제_examples/공학기초_foundations/run_checks.py
```

결과를 JSON으로 남기려면 다음 명령을 씁니다.

```bash
python 예제_examples/공학기초_foundations/run_checks.py --report build/foundation-checks.json
```

실행기는 도메인마다 별도의 Python 프로세스를 사용합니다. 각 폴더의 같은 이름을 가진 작은 모델들이 서로 섞이지 않게 하기 위한 구성입니다. 검사는 [VERIFICATION.json](VERIFICATION.json)에 기록한 76개입니다.

| 폴더 | 다루는 모델 | 비교 기준 |
| --- | --- | --- |
| [math_physics](math_physics/README.md) | 불확도, QR 최소제곱, 통계, Euler, 진동, 열확산 | 손계산, 직교 조건, 해석해, 수렴률, 보존·경계 조건 |
| [circuits_hardware](circuits_hardware/README.md) | RC/RLC, MOS, FIFO, cache, 전송선, probe | 해석해, 적분, 독립 상태 모델, 전력·DC 극한 |
| [systems](systems/README.md) | 수 표현, 부트 메모리, DMA, framing, CRC, 주소 변환, 인증 | 정확한 유리수, RFC 벡터, 표준 라이브러리, 상태·접근 규약 |
| [signals_ai](signals_ai/models.py) | 샘플링, ADC, 피드백, gradient, attention, Roofline | 동일 표본 반례, 오차 적분, 해석 수열, 중심 차분, 불변 조건 |

## 신호·제어·AI 예제 실행

이 문서와 연결된 짧은 코드의 `from signals_ai.models import ...`는 아래 폴더에서 Python을 실행하면 사용할 수 있습니다.

```bash
cd 예제_examples/foundations
python -c "from signals_ai.models import alias_frequency; print(alias_frequency(900, 1000))"
```

PowerShell에서 저장소 루트에 머물러 실행하려면 이 프로세스의 모듈 경로를 지정합니다.

```powershell
$env:PYTHONPATH = (Resolve-Path 예제_examples/foundations).Path
python -c "from signals_ai.models import alias_frequency; print(alias_frequency(900, 1000))"
```

다른 그룹의 문서 예제는 해당 그룹의 README에 적힌 폴더에서 실행합니다. FPGA RTL은 [별도 시뮬레이션 명령과 규약](circuits_hardware/README.md)을 갖습니다. Python 상태 모델 검사와 RTL 실행은 별개의 검사입니다.

## 도표 다시 만들기

```bash
python -m pip install matplotlib==3.10.0
python 예제_examples/공학기초_foundations/make_figures.py
```

[figures](figures)의 PNG·SVG는 이 저장소의 수치 모델에서 직접 그렸습니다. 그래프 생성은 Matplotlib 3.10.0에서 확인했습니다. 축의 영문 기술 표기는 본문의 한국어·영어 캡션과 함께 읽을 수 있습니다. 대학·기업 자료의 그림을 복사하지 않았습니다.

계산 검사는 명시한 수학 모델과 상태 규약을 확인합니다. 실제 회로 측정, 공정 모델 검증, 합성·타이밍 확인, MCU 보드 시험이나 GPU benchmark는 각 환경에서 별도로 기록해야 하는 결과입니다.

## English

These examples connect concepts to equations, executable models, and independent checks. Numerical checks use only Python's standard library; regenerating plots additionally requires Matplotlib. The linked articles explain the assumptions and derivations.

Run `python 예제_examples/공학기초_foundations/run_checks.py` from the repository root with Python 3.12 or later. Add `--report build/foundation-checks.json` to save a report. Each domain runs in its own process to keep identically named local models independent. The recorded suite contains 76 tests in [VERIFICATION.json](VERIFICATION.json).

| Directory | Models | Independent checks |
| --- | --- | --- |
| [math_physics](math_physics/README.md) | Uncertainty, QR, statistics, Euler, oscillation, diffusion | Hand calculations, orthogonality, exact solutions, convergence, conservation and boundaries |
| [circuits_hardware](circuits_hardware/README.md) | RC/RLC, MOS, FIFO, cache, transmission lines, probes | Exact solutions, integration, independent state models, power and DC limits |
| [systems](systems/README.md) | Representations, boot memory, DMA, framing, CRC, translation, authentication | Exact rationals, RFC vectors, standard libraries, state and access contracts |
| [signals_ai](signals_ai/models.py) | Sampling, ADC, feedback, gradients, attention, Roofline | Identical-sample counterexamples, error integration, exact sequences, centered differences, invariants |

For `from signals_ai.models import ...`, change into `예제_examples/foundations` before starting Python, or set `PYTHONPATH` as shown in the PowerShell example above. Other groups describe their working directories in their own README files. [RTL simulation commands](circuits_hardware/README.md) are separate from the Python behavioral checks.

To recreate plots, install Matplotlib 3.10.0 and run `python 예제_examples/공학기초_foundations/make_figures.py`. The PNG/SVG files in [figures](figures) were calculated and plotted from this repository's models. English axis labels have Korean and English captions in the articles. No university or company figure was copied.

These checks verify the stated mathematical models and state contracts. Physical circuit measurements, process-model validation, synthesis and timing checks, MCU board tests, and GPU benchmarks are distinct results that require their respective environments.
