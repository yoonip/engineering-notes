# 현업 언어 예제의 실행 기록 | Execution records for industry-language examples

[예제 목차](README.md) · [언어의 역할과 공식 출처](언어별역할과출처_language-roles.md)

## 2026-10-26에 직접 실행한 범위

| 예제와 기록 | 실제 도구·실행 | 정상 결과 | 별도 오류 입력·결함 대조 |
| --- | --- | --- | --- |
| [SystemRDL](01-레지스터명세_systemrdl/example.json) | systemrdl-compiler 1.33.0의 compile·elaborate, PeakRDL-CHeader 1.1.0의 헤더 생성, Zig/Clang의 호스트 C 컴파일·실행입니다. | AST 속성 비교 50개, C 정적 단언 21개를 통과했고 헤더 두 번의 생성 결과가 같은 바이트였습니다. | 잘못된 RDL 4종을 실제 컴파일러가 거절했고 생성 헤더의 모드 마스크를 바꾼 대조 1종이 정적 단언에서 실패했습니다. |
| [MATLAB 계열 수치 코드](02-수치계산_matlab-octave/example.json) | GNU Octave 11.3.0에서 `.m` 파일을 실행했습니다. | 검사 496개, 행렬 표본 153개, ode45 설정 3개와 RK4 격자 3개를 확인했습니다. | 입력 거절 8건과 영평형·무감쇠 등 정한 조건을 비교했습니다. |
| [Ada·계약](03-계약과범위_ada-spark/example.json) | GNAT 16.1.0으로 컴파일·바인드·링크하고 호스트에서 실행했습니다. | 비교 3,098개에서 정상 입력 2,063개와 사전조건 거절 1,034개를 확인했습니다. 별도 CLI 11건도 기대 출력·종료 코드와 같았습니다. | 경계·형 변환·범위·사전조건의 예외를 구분했습니다. GNATprove는 실행하지 않았습니다. |
| [PLC Structured Text](04-PLC스캔_structured-text/example.json) | Beremiz 1.6.0 번들의 실제 matiec로 ST→C 번역 후 Zig/Clang으로 생성 코드를 컴파일·실행했습니다. | 8,000개 길이3 입력 순서와 고정 흐름에서 상태 비교 32,008개를 통과했습니다. | 복사본의 `<=250`을 `<250`으로 바꾼 경계 결함이 실제 실행의 비교에서 실패했습니다. |

표의 단위가 서로 다르므로 비교 수·입력 순서·생성 횟수를 합쳐 성능 수치나 전체 커버리지로 표시하지 않습니다. 각 `example.json`에 정상·오류 결과의 실제 명령·종료 코드·stdout·stderr와 소스 해시가 있습니다. C·Python으로 작성한 호스트 검사와 원래 검사 대상인 RDL·ST·Ada·`.m`의 역할도 구분합니다.

## 실제 완료 출력

```text
PASS systemrdl ast_checks=50 header_assertions=21 rejected=4 header_negative_controls=1 deterministic_exports=2
PASS matlab-octave checks=496 matrix_cases=153 ode_cases=3 rk4_grids=3 rejected_inputs=8
PASS ada checks= 3098 accepted= 2063 precondition_rejections= 1034
PASS structured-text normal_checks=32008 negative_boundary=detected
```

Ada 출력의 공백은 실제 정수 `Image` 출력에 따른 것입니다. ST의 바깥 완료 출력은 정상 호스트 검사와 의도한 결함 검출이 각각 기대대로 끝났다는 뜻입니다. 잘못된 명세·계약 호출의 거절, 생성 헤더의 컴파일 실패, 실행 중 기능 불일치를 같은 종류의 결과로 합치지 않습니다.

## 결과를 해석하는 조건

SystemRDL 예제는 명세 속성과 생성된 헤더를 비교했습니다. RO·RW·W1C를 명세에 썼다는 사실과 실제 버스의 읽기·쓰기·동시 사건이 그 속성을 지킨다는 사실은 다릅니다. 이 작업에서 RTL을 생성하거나 버스·MMIO를 실행하지 않았습니다.

Octave 예제는 정한 질량·스프링 계통에서 행렬 계산·ODE 해석기·고정 간격 적분을 해석해와 비교했습니다. 수치 오차는 모형·계산 사이의 차이이며 실물 장치의 오차·제어 성능이 아닙니다. MATLAB 상용 런타임·Simulink·Stateflow·코드 생성기는 실행하지 않았습니다.

Ada의 `-gnata`와 런타임 범위 검사를 사용한 호스트 실행은 지정한 입력의 계약 위반을 관측한 결과입니다. 소스의 `SPARK_Mode`와 계약을 작성했다는 사실만으로 정적 증명을 마쳤다고 표시하지 않습니다. GNATprove를 설치·실행하지 않았고 `bench.gpr`은 프로젝트 사용 예시로 제공하며 이번 실제 빌드에는 사용하지 않았습니다.

ST 예제는 함수 블록의 입력을 고정하고 생성된 body 함수를 순서대로 호출했습니다. PLC의 태스크 스케줄러·실시간 주기·입력 및 출력 이미지·실물 I/O는 실행하지 않았습니다. 표시 상태의 교육용 모형이며 장비 제어나 기능 안전을 검증한 코드가 아닙니다.

## 공식 자료를 읽은 외부 환경

CAPL·CANoe, SKILL·Virtuoso, LabVIEW·G, SCADE·Swan, Chisel, Verilog-AMS, Modelica, FPP는 [언어별 역할](언어별역할과출처_language-roles.md)에 학습 경로와 역할을 연결했습니다. 이 작업에서 해당 언어·상용 도구의 코드를 실행한 결과로 세지 않습니다. CAPL 연습의 토큰 발급·온라인 채점도 수행하지 않았습니다.

## 게시 자료의 정적 대조

[check_sources.py](check_sources.py)는 현재 소스 바이트·카탈로그 해시·README에 실은 전체 코드·저장된 완료 줄·로컬 파일 링크를 대조합니다. `tools_reexecuted: false`이므로 이 결과를 새 컴파일·수치 계산·증명 결과로 읽지 않습니다. 실행을 다시 하려면 각 예제의 명령·의존성·입력 조건을 사용합니다.

[게시 소스·문서 대조 결과](source-check.json)에 검사 시각과 예제별 일치 결과를 보존합니다.

```bash
python -B 하드웨어코딩_hardware-coding/현업언어_industry-languages/check_sources.py --report /path/to/current-source-check.json
```

생성된 C·헤더·실행 파일은 별도 작업 폴더에서 만들었습니다. 원본 코드를 바꾸면 기존 실행 해시와 대조가 실패하므로, 변경한 소스로 다시 실행하고 결과를 검토해야 합니다. 문체를 고치는 과정에서 과거 측정값·검사 수·출처를 바꾸지 않습니다.
