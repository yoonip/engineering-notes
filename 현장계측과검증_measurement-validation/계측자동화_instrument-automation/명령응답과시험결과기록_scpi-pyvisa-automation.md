# 계측 명령·응답과 시험 결과 기록 | SCPI, PyVISA and measurement records

계측 자동화의 목적은 숫자를 CSV에 모으는 데서 끝나지 않습니다. 어느 장비가 어떤 설정으로 측정했는지, 응답이 없었을 때 제품 불량과 통신 실패를 어떻게 구별했는지까지 남겨야 다른 사람이 판정을 다시 확인할 수 있습니다. 이 글은 기존 [실리콘 검증 연습 프로젝트](../../프로젝트_projects/practical-silicon-lab/README.md)의 코드를 읽고, 실물 장비 없이 확인한 부분과 실제 장비 어댑터에 필요한 부분을 나눕니다.

## SCPI와 VISA는 맡은 일이 다릅니다

SCPI는 계측기의 설정·조회 등을 표현하는 명령 체계입니다. VISA는 USB·GPIB·직렬·네트워크 등의 장비 연결을 다루는 인터페이스입니다. PyVISA는 Python에서 VISA 기능을 사용하는 라이브러리입니다. 계측기 모델이 바뀌면 명령과 응답 형식도 확인해야 합니다. PyVISA가 설치됐다고 모든 장비의 전압 설정이나 파형 취득을 같은 함수로 사용할 수 있는 것은 아닙니다.

기존 [`visa_readonly.py`](../../프로젝트_projects/practical-silicon-lab/validation/visa_readonly.py)의 CLI가 보내는 것은 식별 조회 `*IDN?` 하나입니다. `*IDN?`는 IEEE 488.2 계열의 공통 조회 명령이며, 측정 시작이나 출력 설정 명령이 아닙니다. 이 예제는 장비 전체 제어기가 아니라 연결과 응답·정리 구조를 읽는 출발점입니다.

| 층 | 먼저 확인할 것 | 실패를 구분하는 관측 |
| --- | --- | --- |
| 장비·배선 | 모델, 펌웨어, 주소, 인터페이스, 연결 대상 | 전면 패널과 식별 응답이 예상 장비와 같은지 확인합니다. |
| 전송 | VISA backend, timeout, 메시지 종료 방식 | 열기 실패, 쓰기 실패, 읽기 timeout을 따로 기록합니다. |
| 명령·상태 | 해당 모델의 명령과 trigger 상태 | 응답을 반환하는 조회인지, 취득을 기다리는 상태인지 확인합니다. |
| 데이터 | 단위, 길이, 수치 형식, 범위 초과 표시 | 파싱 성공 뒤에도 데이터의 유효성을 확인합니다. |
| 시험 판정 | 사전 정의한 조건과 허용값 | 유효 측정의 FAIL과 측정 불성립을 구분합니다. |

## 기존 전송 코드에서 읽을 부분

다음은 전체 파일 중 구조를 설명하기 위한 발췌입니다. 실장비 실행 전에는 해당 모델 설명서에서 종료 문자와 통신 조건을 확인합니다. 이 글을 작성하면서 실장비를 연결하거나 명령을 보내지는 않았습니다.

```python
import pyvisa                         # VISA 연결 기능을 제공하는 모듈을 불러옵니다.
manager = pyvisa.ResourceManager()     # 설치한 VISA backend를 사용할 관리 객체입니다.
device = manager.open_resource(resource)  # 확인한 장비 주소로 세션을 엽니다.
try:                                  # 조회가 실패해도 아래 finally를 실행합니다.
    device.timeout = 2000              # I/O 제한 시간이며 단위는 밀리초입니다.
    device.read_termination = "\n"    # 이 예제의 응답 종료 조건입니다.
    device.write_termination = "\n"   # 이 예제에서 명령 끝에 붙이는 문자입니다.
    response = device.query("*IDN?")  # 명령을 쓰고 응답을 읽습니다.
finally:                              # 정상·예외 경로 모두 연결을 정리합니다.
    try:                              # 장비 세션 닫기 실패도 다음 정리를 막지 않게 합니다.
        device.close()                # 장비와의 세션을 닫는 메서드 호출입니다.
    finally:                          # 세션 닫기의 성공 여부와 무관하게 실행합니다.
        manager.close()               # VISA 관리 객체의 자원을 정리합니다.
```

발췌문은 열기 이후를 보여 줍니다. 실제 프로젝트의 클래스는 `open_resource()`나 초기 속성 설정 단계에서 실패해도 관리 객체를 닫도록 별도로 처리합니다. `finally`는 프로그램의 정리 경로이며 물리 장비의 출력이 꺼졌다는 증거와 같지 않습니다. 세션 닫기와 장비 출력 상태는 장비별로 별도 확인해야 합니다.

PyVISA의 timeout은 밀리초지만 `query_delay`는 초입니다. timeout을 2로 쓰면 2초가 아니라 2밀리초입니다. `\n`은 줄바꿈 LF이며 모든 계측기에 통용되는 필수 설정은 아닙니다. 명령은 전달됐으나 응답 끝을 인식하지 못한 경우에도 읽기 timeout이 날 수 있습니다. 공식 [통신 안내](https://pyvisa.readthedocs.io/en/1.15.0/introduction/communication.html)와 [리소스 속성](https://pyvisa.readthedocs.io/en/1.15.0/introduction/resources.html)의 단위·종료 조건을 기준으로 설명했습니다.

## 시험 순서와 상태를 기록합니다

아래 순서는 실제 장비 어댑터를 설계할 때 사용할 자체 구성 절차입니다. 프로젝트의 식별 조회 CLI가 이 전체 절차를 구현했다는 뜻은 아닙니다.

1. 실행 ID, DUT 식별자, 보드·펌웨어·시험 코드 버전을 먼저 확정합니다. DUT는 시험 대상 장치입니다.
2. 장비 식별과 교정 상태, 프로브·케이블·치구를 기록합니다. 설정값과 DUT 위치에서 측정한 값을 다른 열에 저장합니다.
3. 범위·대역폭·적분 시간·트리거·샘플 개수 등을 명시합니다. 자동 범위가 바뀌는 실험이라면 변경 여부도 남깁니다.
4. 모델 설명서의 완료 조건으로 설정·취득을 동기화합니다. 단순 `sleep()`은 경과 시간을 기다릴 뿐 완료를 확인하지 않습니다.
5. 응답 원문과 파싱 결과를 연결하고, 개수·단위·유한값·범위 초과 상태·타임스탬프를 확인합니다.
6. 유효 측정에만 제품 한계를 적용합니다. 결과·원문·조건·오류·정리 결과를 같은 실행 ID로 저장합니다.

동시에 여러 작업이 같은 장비 세션에 `query()`를 보내면 A의 응답을 B가 읽는 문제가 생길 수 있습니다. 장비별 요청·응답을 한 소유자가 직렬화하거나 명시적인 잠금으로 보호하는 설계가 필요합니다. timeout 후에는 이전 응답이 뒤늦게 도착했는지 확인하지 않고 다음 응답으로 해석하면 안 됩니다. 재동기화 방법은 모델·전송 방식에 맞게 정하고, 출력 상태를 바꾸는 명령을 무조건 재전송하지 않습니다.

`*OPC?`처럼 완료를 기다리는 공통 명령도 장비 설명서가 지정한 동작과 순서 안에서 사용해야 합니다. 트리거를 받지 않은 측정이 대기 중인데 timeout만 늘리면 설정 오류가 오래 숨겨집니다. 장비의 대기 상태, 명령 이해 여부, 전송 지연을 분리해서 조사합니다.

## 전력 숫자 하나를 만들 때도 필요한 조건이 있습니다

기존 [`bench.py`](../../프로젝트_projects/practical-silicon-lab/validation/bench.py)는 실물 전원과 무관한 `FakeBench`입니다. 0.80 V, 2 A의 합성 파형을 0~10 ms에 걸쳐 1 ms 간격으로 11개 생성하고 추론 두 번이 완료됐다고 가정합니다. 전압과 전류의 시각이 일치하는 표본에 사다리꼴 적분을 적용합니다.

```text
P = V × I = 0.80 × 2 = 1.6 W
E = P × Δt = 1.6 × 0.010 = 0.016 J
완료 1회당 에너지 = 0.016 / 2 = 0.008 J
```

이 값은 코드로 만든 예제를 계산한 결과이며 NPU나 SoC의 실측 전력은 아닙니다. `droop` 입력은 전체 파형 전압을 0.12 V 낮춰 0.68 V로 만듭니다. 순간적인 전원 과도 현상을 재현하는 모델이 아닙니다. 이 경우 에너지는 0.0136 J로 작아지지만 전압 하한 0.76 V를 위반하므로 FAIL입니다. 에너지 숫자가 작아졌다고 좋은 동작으로 판단할 수 없는 예입니다.

실제 시험에서 전류계만 다른 시각에 샘플링하면 `V[k] × I[k]`가 같은 순간의 전력이 아닐 수 있습니다. 전원 장비의 표시값을 DUT 위치 전압으로 대신하거나 호스트 실행 시간을 장비 취득 구간으로 대신하는 것도 다른 물리량을 섞는 일입니다. 측정 지점과 시각 기준을 먼저 정해야 합니다.

## FAIL과 INFRA_ERROR를 분리하는 이유

기존 모델의 종료 코드는 PASS 0, FAIL 1, INFRA_ERROR 2입니다. 낮은 전압과 데이터 불일치는 유효 입력에 대한 FAIL입니다. timeout과 숫자 파싱 실패는 제품을 판단할 측정이 성립하지 않은 INFRA_ERROR입니다. 이런 실행을 모두 불량 수에 넣으면 수율이 틀어집니다. 반대로 오류 실행을 조용히 버리면 실행률이 과장됩니다.

자체 구성한 집계 예로, 계획 12개 중 10개를 실행하고 유효 결과가 8개, 그중 통과가 7개라면 실행률은 10/12, 유효 결과 확보율은 8/12, 유효 결과 안의 통과율은 7/8입니다. 세 분모가 다릅니다. 기존 [`coverage_account.py`](../../프로젝트_projects/practical-silicon-lab/validation/coverage_account.py)도 이 구분을 다룹니다.

결과를 재검토할 때는 `run_id`, `serial`, `test_revision`, `instrument_id`, `configuration`, `raw_response`, `status`, `error_type`, `retry_of`, `cleanup_status` 같은 항목을 연결할 수 있어야 합니다. 이는 이 글에서 제시한 기록 항목입니다. 기존 `VisaTransport.log`는 성공한 query의 명령·응답·호스트 경과 시간만 담고, 실패한 query의 원문이나 장비 전체 상태는 기록하지 않습니다. 실제 어댑터에 붙일 때 채워야 할 부분입니다.

## 실제로 실행해 확인한 범위

2026-10-21에 Windows, CPython 3.12.14에서 기존 `tests/test_offline.py`의 19개 검사를 다시 실행했습니다. 모두 통과했습니다. 그중 VISA 검사는 정상 식별 조회·초기 열기 실패·조회 timeout의 세 경우이며 `pyvisa` 모듈과 장비 객체를 mock으로 바꿉니다. mock은 실제 장비 대신 정해진 응답과 실패를 내도록 만든 모의 객체입니다. 설치한 VISA backend, PyVISA-sim, 실제 USB/LAN 연결을 시험한 것이 아닙니다.

프로젝트 폴더에서 다음 명령으로 재현합니다. 보고서 경로의 상위 폴더는 미리 만들고, 과거 공개 결과를 덮어쓰지 않는 새 경로를 지정합니다.

```text
python -B tests/test_offline.py --report /existing/folder/verification.local.json
```

검사에는 JTAG 상태 전이, 모의 NPU 비교, 합성 수율·coverage 계산, Linux 파일 입출력 mock도 포함됩니다. “19개 검사 통과”를 계측기 19종 실사용으로 읽으면 안 됩니다. 프로젝트 39개 파일의 실행 전후 해시는 같았습니다. [실행 기록](../../설계와검증사례_engineering-cases/검증기록_evidence/계측자동화모의검사_20261021.md)에서 검사명과 한계를 확인할 수 있습니다.

## 확인 문제

1. timeout이 났다는 이유만으로 DUT를 불량 처리해도 됩니까?
2. 0.68 V에서 에너지가 작게 계산됐으므로 0.80 V보다 좋은 결과입니까?
3. `finally`에서 세션을 닫았으면 장비 출력 OFF도 확인한 것입니까?

답: 1번은 아닙니다. 통신·설정·트리거·장비 상태를 구분하고 측정 성립 여부를 확인해야 합니다. 2번은 예제의 전압 허용 조건을 위반해 FAIL입니다. 3번은 아닙니다. 연결 정리와 출력 상태 확인은 별개입니다.

## 출처와 관련 학습

- PyVISA 1.15.0, [Communicating with your instrument](https://pyvisa.readthedocs.io/en/1.15.0/introduction/communication.html), 통신 문제와 query 동작. [Resources](https://pyvisa.readthedocs.io/en/1.15.0/introduction/resources.html), timeout·termination·query_delay. 2026-10-21 열람했습니다.
- [검증 예제 설명과 실행 결과 형식](../../프로젝트_projects/practical-silicon-lab/validation/README.md), [offline 검사 원문](../../프로젝트_projects/practical-silicon-lab/tests/test_offline.py).
- [센서·계측의 기초](../../분야_topics/37-센서계측_sensors-instrumentation/README.md), [개별 장비의 연결과 설정](../계측기_instruments/README.md).

## English

SCPI commands, VISA transport, instrument state, data validity and DUT verdicts belong to different layers. This note reads the repository's identification-only transport and deterministic bench model, then develops an explicitly proposed measurement workflow. All 19 existing offline tests passed, including three mocked VISA paths. No physical instrument, VISA backend or output control was exercised. The synthetic energy example is 0.016 J over 10 ms, or 0.008 J per assumed completed inference; undervoltage remains a failure even if the computed energy decreases.
