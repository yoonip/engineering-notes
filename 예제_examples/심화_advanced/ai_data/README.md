# AI·데이터 심화 실행 예제

Python 표준 라이브러리로 수식을 직접 계산하고 독립 기준과 비교합니다. 외부 패키지 설치는 필요하지 않습니다. 저장소 최상위에서 실행합니다.

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" all
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

| 명령 | 실제 계산 |
|---|---|
| mlp | tanh MLP의 역전파와 XOR 600회 학습 |
| tile | 경계 타일의 입력 load 수와 shared-memory bank 모델 |
| matrix | 직사각 행렬의 CPU 타일 곱과 독립 기준 비교 |
| decode | 고정 전이확률의 greedy·beam 탐색과 KV 저장 크기 |
| database | 두 SQLite 연결의 WAL snapshot과 version 충돌 |
| clocks | 송신·수신 사건의 Lamport 논리시계 |
| scan | Blelloch exclusive scan과 작업량 |
| warp | 역방향 affine 매핑과 쌍선형 보간 |
| attention | 단일 query의 attention 출력·미분·prefix cache |
| adam | clipping, Adam 상태와 이차함수 최적화 |
| metrics | macro·micro F1과 Wilson 정답률 구간 |
| quantization | 출력 채널별 scale을 쓰는 정수 내적 |
| raster | 화면 보간과 원근 보정 보간 비교 |

한 명령만 실행할 때는 all 대신 표의 명령을 사용합니다. `--output 결과.json` 옵션은 실행 결과를 JSON 파일에 저장합니다. SQLite는 임시 폴더의 파일을 사용하고 연결을 닫은 뒤 정리합니다. 타이밍은 실행한 환경의 값이며 보편적인 성능 수치가 아닙니다.

CUDA 예제 `tiled_matmul.cu`는 별도 소스입니다. CUDA Toolkit과 호환되는 host compiler가 있는 환경에서 컴파일할 수 있습니다.

```bash
nvcc -O2 -std=c++17 "예제_examples/심화_advanced/ai_data/tiled_matmul.cu" -o tiled_matmul
```

Windows 실행 파일은 `.\tiled_matmul.exe 37 45 29`로 실행합니다. Kernel은 16×16 타일을 사용하고 경계 load는 0으로 채웁니다. 실행 파일 자체가 double CPU 기준과 전 출력을 비교하고, 실패 수·오차·CUDA event 시간을 JSON으로 출력합니다. Kernel 시간에는 전송을 포함하지 않습니다. Python CLI의 matrix 결과는 CPU 계산이며 `cuda_executed: false`를 명시합니다. 이 저장소의 Python 검증 통과가 CUDA 컴파일·장치 실행을 뜻하지는 않습니다.

## English

These examples calculate the equations with the Python standard library and compare them with independent references. No external Python package is required. Run the commands from the repository root. Use one command from the table instead of all to run a single calculation, or `--output result.json` to save its JSON report.

The commands cover executed MLP backpropagation and XOR training, tile-load/bank models, CPU tiled matrix multiplication, finite beam search and cache size, real SQLite WAL snapshots/version conflicts, Lamport clocks, exclusive scan, bilinear warping, attention derivatives and prefix cache, Adam state, classification metrics/intervals, per-channel integer dot products, and perspective interpolation. SQLite uses temporary on-disk files and closes connections before cleanup. Timings belong to the measured environment.

The separate CUDA source can be compiled with a CUDA Toolkit and supported host compiler. On Windows, run `.\tiled_matmul.exe 37 45 29`. It uses 16×16 tiles, zero-fills boundary loads and compares every GPU output with a double-precision CPU reference. Its own JSON includes numeric failures, error and CUDA-event kernel time excluding transfers. The Python matrix command runs on the CPU and reports `cuda_executed: false`. Passing Python tests does not establish CUDA compilation or device execution.
