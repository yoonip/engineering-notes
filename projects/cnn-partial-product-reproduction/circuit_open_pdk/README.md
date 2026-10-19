# 외부 SKY130 모델 어댑터

이 폴더는 외부 로컬 SKY130 모델을 준비하고 CMOS MAC netlist에 연결하는 자체 코드만 포함한다. PDK, 공급사 모델 계수, 실행 파일은 포함하지 않으며 자동으로 내려받지 않는다.

참조 저장소는 [skywater-pdk-libs-sky130_fd_pr](https://github.com/google/skywater-pdk-libs-sky130_fd_pr), 기존 실험의 참조 commit은 `f62031a1be9aefe902d6d54cddd6f59b57627436`이다. 준비 명령은 입력 checkout의 commit을 자동으로 확인하지 않고 실제 입력 파일의 SHA256을 기록한다.

## 모델 준비

`--model-root` 아래에 다음 파일들이 있는 기존 로컬 모델을 사용한다.

```text
cells/nfet_01v8/sky130_fd_pr__nfet_01v8__tt.pm3.spice
cells/nfet_01v8/sky130_fd_pr__nfet_01v8__tt.corner.spice
cells/nfet_01v8/sky130_fd_pr__nfet_01v8__mismatch.corner.spice
cells/pfet_01v8/sky130_fd_pr__pfet_01v8__tt.pm3.spice
cells/pfet_01v8/sky130_fd_pr__pfet_01v8__tt.corner.spice
cells/pfet_01v8/sky130_fd_pr__pfet_01v8__mismatch.corner.spice
models/parameters/lod.spice
```

LOD 파일은 `parameters/lod.spice` 위치도 지원한다. 모델 준비 결과는 공급사 계수를 포함하므로 소스 checkout 바깥에만 생성한다. 외부 모델의 이용·재배포 조건은 해당 모델 배포물에 따른다.

아래 예시는 저장소와 나란히 있는 `external-models/sky130_fd_pr`을 입력으로 사용한다. 모델 자체를 받거나 설치하는 명령은 아니다.

```sh
python circuit_open_pdk/prepare_models.py --model-root ../external-models/sky130_fd_pr --output-dir ../private-models/sky130
python circuit_open_pdk/run_sky130.py --model-wrapper ../private-models/sky130/sky130_tt_reduced.spice --generate-only --cases 6:0 6:5 8:0 8:7 --samples 12 --output-dir results/sky130
```

선택기는 L=0.15µm에서 nfet W=0.42/0.84/1.26µm, pfet W=1.26µm에 해당하는 bin을 남긴다. 수치 계수를 변경하지 않는다. 준비 결과에 입력 파일 해시와 선택 블록 해시를 기록한다. 다른 모델 버전은 bin 구성과 동작이 달라질 수 있다.

## 실제 실행

별도 설치한 ngspice가 필요하다. 실행 파일은 `--ngspice`, `NGSPICE_EXECUTABLE`, PATH 순서로 찾는다. `--model-wrapper` 대신 `SKY130_MODEL_WRAPPER` 환경변수도 지원한다.

```sh
python circuit_open_pdk/run_sky130.py --model-wrapper ../private-models/sky130/sky130_tt_reduced.spice --cases 6:0 6:1 6:5 8:0 8:1 8:7 --samples 12 --jobs 2 --output-dir results/sky130
python circuit_open_pdk/plot_results.py --output-dir results/sky130
```

회로는 1.8V, TT, 25°C, 10MHz, 32bit 피드백 누산기다. 각 bit width 안에서 같은 topology와 입력열을 사용한다. 기능 불일치가 있는 실행은 전력 비교에 채택하지 않는다. 공급전력에 이상적 외부 입력·클록·EN·비중첩 클록 발생기의 비용과 추출 배선 기생은 포함하지 않는다. 45nm 공정의 전력 재현이나 제조 검증 결과가 아니다.

`--vectors-csv`는 별도 로컬 CSV의 정수 `a,b` 열을 읽는다. 행 수는 `--samples`와 같아야 한다. 실제 CNN 입력을 새로 만들 때는 `cnn/run_cifar.py export_stimulus`에 학습된 로컬 checkpoint를 전달한다. dataset·checkpoint·과거 입력 CSV는 배포하지 않는다.

이번 공개 사본 검증에서는 외부 모델 bin 준비·hash 일치와 netlist 생성을 확인했다. SKY130 전체 MAC transient sweep은 다시 실행하지 않았다.
