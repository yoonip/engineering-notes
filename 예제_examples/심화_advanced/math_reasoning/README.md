# 수학·물리·추론의 심화 구현 | Advanced mathematics, physics and reasoning

핵심 계산은 Python 3 표준 라이브러리로 실행합니다. 아래 명령은 저장소 루트 기준입니다. `--output`을 생략하면 요약만 출력하며, 지정하면 JSON과 세 개의 시계열·격자 CSV를 저장합니다.

```bash
python 예제_examples/심화_advanced/math_reasoning/demo.py --output results/advanced-math
python -m unittest discover -s 예제_examples/심화_advanced/math_reasoning -p "test_*.py" -v
```

| 구현 / Implementation | 독립 확인 / Independent check |
| --- | --- |
| `ridge2` | 유리수 해·대각 SVD 축소·수치 기울기 / Rational solution, spectral filter, numerical gradient |
| `simulate_pi` | ZOH 해석해·특성근·포화 복귀 / ZOH solution, roots, saturation recovery |
| `heat_fem` | 열저항 해·제조해·격자 수렴 / Resistance, manufactured solution, mesh convergence |
| `coupled_exact`, `coupled_verlet` | 독립 모드 해·시간 수렴·에너지 / Modal solution, time convergence, energy |
| `sat_dpll` | 420개 CNF의 전수 진리표 / Exhaustive oracle on 420 CNFs |
| `bayes_coin_models` | 정확한 적분 likelihood·사전확률·극한 / Rational evidence, priors and limits |
| `leontief_fixed_point` | 유리수 선형계·잔차 오차 상계 / Rational solve and residual certificate |
| `standardized_rates` | 모집단 복제·층별 비율 / Replicated population and strata |
| `VersionTimeline` | 361개 날짜의 선형 탐색 / Linear oracle over 361 dates |

`results/`에는 본문의 기본 입력으로 실제 실행한 CSV와 요약을 보관했습니다. 물리량은 각 글에 정한 선형 모델과 단위를 따릅니다. 사회·경제·법령 예제의 자료는 계산 구조를 설명하는 구성 데이터이며 실제 기관의 통계나 법률 결론을 나타내지 않습니다.

`make_figures.py`는 같은 계산에서 PNG·SVG를 생성합니다. 도표 생성에는 Matplotlib이 추가로 필요합니다. SVG에는 확대 가능한 글자 윤곽과 선을 저장하며, 외부의 그림을 복사하지 않았습니다.

```bash
python -m pip install -r 예제_examples/심화_advanced/math_reasoning/requirements-figures.txt
python 예제_examples/심화_advanced/math_reasoning/make_figures.py
```

## English

Core computations and tests use the Python 3 standard library. Run from the repository root. Without `--output`, the demo prints a summary; with it, the demo writes JSON plus three trajectory/grid CSV files. The table maps each implementation to independent verification. `results/` preserves a run using the articles' default inputs.

Physical variables follow the explicit linear models and units in each article. Social, economic and temporal examples use constructed data to explain computation, rather than representing institutional statistics or legal conclusions. Figure generation additionally needs Matplotlib, as declared in `requirements-figures.txt`. `make_figures.py` generates original PNG/SVG plots from the same models, with scalable text outlines and lines in SVG.
