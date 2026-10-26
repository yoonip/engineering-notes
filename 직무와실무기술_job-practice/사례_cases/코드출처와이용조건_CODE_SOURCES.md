# 코드의 출처·수정 범위와 이용 조건 | Code provenance, changes and licenses

[사례 목차](README.md) · [직무별 연결](06-직무별사례와담당범위_role-case-map.md)

이 사례의 코드 블록은 아래 원문에서 발췌했습니다. 원본의 실행문·설정값을 유지한 범위와 설명을 위해 일부 구간을 선택한 범위를 각 본문에 표시했습니다. 한국어 주석과 원인 분석·업무 적용 설명은 이 자료에서 추가했습니다.

## 원문 코드의 성격

| 구분 | 이 자료에서 뜻하는 것 | 해당 자료 |
| --- | --- | --- |
| 제조사 공식 예제 | 특정 장비를 제어하는 방법을 제조사가 공개한 예제입니다. | Tektronix Keithley 2450의 Python 코드입니다. |
| 공개 프로젝트의 구현 | 장치·도구·라이브러리에 실제로 포함된 구현입니다. | ADI no-OS 드라이버, U-Boot `mtest`, SciPy `levene`입니다. |
| 프로젝트 공식 예제·시험 | 프로젝트가 제공한 API 사용 예제나 시험 코드입니다. | Zephyr의 UART·CAN·Python 시험, cocotb adder, PyEpics·scikit-learn 예제, fio job입니다. |
| 공식 SQL 예제 | 데이터베이스 기능을 설명하는 원문의 문장입니다. | PostgreSQL `INSERT ... ON CONFLICT`입니다. |
| 자체 구성한 설명 | JD와 공개 코드를 연결하는 업무 상황·불량 가설·판정 절차·단위 계산입니다. | 각 본문에서 가정 또는 학습용 예로 표시한 부분입니다. |

공개 구현과 공식 예제라는 근거로 해당 코드의 출처를 확인합니다. 삼성전자·SK하이닉스 내부에서 이 파일을 그대로 사용한다는 채택 정보는 확인하지 않았습니다. 예제의 통신·오류 처리·범위를 검토하는 설명도 함께 두어, 공개 예제를 완성된 양산 시험 프로그램과 혼동하지 않도록 했습니다.

## 원본 판본과 라이선스

고정 링크의 commit은 파일 내용의 판본을 식별합니다. 읽기 편한 tag·version과 실제 commit을 함께 적었으며, 브랜치가 나중에 바뀌어도 같은 원문을 찾을 수 있습니다. 구체적인 원본 줄 범위와 함수명은 각 발췌 바로 위에 있습니다.

| 원문과 고정 판본 | 이 자료에서 발췌한 대상 | 라이선스·고지 |
| --- | --- | --- |
| [Tektronix/keithley `96f209329a4c0a995cc4f0a57d9e3d301a640d17`](https://github.com/tektronix/keithley/tree/96f209329a4c0a995cc4f0a57d9e3d301a640d17) | 2450의 전류 인가·전압 측정과 저저항 측정 예제입니다. | [Tektronix Sample Source Code License](licenses/Tektronix-Sample-License.txt). Tektronix 제품과 함께 사용하는 범위이며 저작권 고지를 유지합니다. |
| [ADI no-OS `d173657d7fc186e398cc6292276daad25a63eb22`](https://github.com/analogdevicesinc/no-OS/tree/d173657d7fc186e398cc6292276daad25a63eb22) | `drivers/adc/ad7124/ad7124.c`의 준비 상태 대기 함수입니다. | [BSD-3-Clause](licenses/ADI-ad7124-BSD-3-Clause.txt). 원본 고지: `Copyright 2015-2019, 2023, 2026(c) Analog Devices, Inc.` |
| [Zephyr v4.2.0, `413b789deb391d3a37d06b463288a5fe765ee57e`](https://github.com/zephyrproject-rtos/zephyr/tree/413b789deb391d3a37d06b463288a5fe765ee57e) | UART echo_bot·CAN counter·pytest shell의 C/Python 예제입니다. | [Apache-2.0](licenses/Apache-2.0.txt). 각 원본 파일의 저작권을 해당 본문에 보존했습니다. |
| [cocotb v2.0.0, `5de5ec5149f768f9624a400edd508935e9669d51`](https://github.com/cocotb/cocotb/tree/5de5ec5149f768f9624a400edd508935e9669d51) | `examples/adder/tests/test_adder.py`의 선택한 시험 함수입니다. | 예제 파일의 [CC0-1.0](licenses/CC0-1.0.txt) 고지를 기준으로 합니다. cocotb 프레임워크 전체의 라이선스와 예제 파일의 고지를 구분합니다. |
| [U-Boot v2025.01, `6d41f0a39d6423c8e57e92ebbe9f8c0333a63f72`](https://github.com/u-boot/u-boot/tree/6d41f0a39d6423c8e57e92ebbe9f8c0333a63f72) | `cmd/mem.c`의 실제 메모리 패턴 비교 부분입니다. | [GPL-2.0 전문](licenses/GPL-2.0.txt), 원본 `GPL-2.0+` 고지에 따라 발췌와 추가 주석은 GPL-2.0-or-later 범위입니다. |
| [fio 3.39, `a6e474c9e896e4ba1eb40066a03402afb040710a`](https://github.com/axboe/fio/tree/a6e474c9e896e4ba1eb40066a03402afb040710a) | `examples/basic-verify.fio`의 검증 설정 일부입니다. | 프로젝트의 [GPL-2.0](licenses/GPL-2.0.txt) 조건을 따릅니다. 장치 경로를 포함한 전체 job을 실행한 기록은 아닙니다. |
| [PyEpics 3.5.8, `4a4caebd92b75ee21c774cfc33c05ae77f4d1f97`](https://github.com/pyepics/pyepics/tree/4a4caebd92b75ee21c774cfc33c05ae77f4d1f97) | 공식 문서의 PV monitor·정리 예제입니다. | [PyEpics 원문 라이선스](licenses/pyepics-3.5.8-LICENSE.txt)를 보존했습니다. |
| [SciPy 1.15.3, `e29dcb65a2040f04819b426a04b60d44a8f69c04`](https://github.com/scipy/scipy/tree/e29dcb65a2040f04819b426a04b60d44a8f69c04) | `scipy/stats/_morestats.py`의 Levene 통계량 계산 부분입니다. | [BSD-3-Clause 원문](licenses/scipy-1.15.3-LICENSE.txt)을 보존했습니다. |
| [scikit-learn 1.7.2, `25dee604bae18205b01548348388baf7a1cdfe0e`](https://github.com/scikit-learn/scikit-learn/tree/25dee604bae18205b01548348388baf7a1cdfe0e) | `doc/common_pitfalls.rst`의 전처리·평가 누출·Pipeline 예제입니다. | [BSD-3-Clause 원문](licenses/scikit-learn-1.7.2-COPYING.txt)을 보존했습니다. |
| [PostgreSQL 17.6, `7885b94dd81b98bbab9ed878680d156df7bf857f`](https://github.com/postgres/postgres/tree/7885b94dd81b98bbab9ed878680d156df7bf857f) | `doc/src/sgml/ref/insert.sgml`의 충돌 처리 SQL입니다. | [PostgreSQL COPYRIGHT](licenses/postgresql-17.6-COPYRIGHT.txt)를 보존했습니다. |

각 코드 발췌와 그에 붙인 주석의 이용 조건은 해당 원문의 조건을 따릅니다. 이 표는 저장소의 다른 코드·글 전체에 새로운 라이선스를 부여하는 문서가 아닙니다.

## 원문과 대조한 방법

- Python은 들여쓰기와 실행문을 파싱한 AST를 비교했습니다. AST는 프로그램의 문법 구조로, 한국어 설명 주석과 빈 줄은 포함하지 않습니다.
- C는 주석·공백을 제외한 실행 토큰을 대조했습니다. 이는 원문과의 일치 검사이며 보드 빌드나 장치 동작 시험을 대신하지 않습니다.
- fio 설정은 선택한 원본 항목과 값의 일치를 대조했습니다. 생략한 장치 경로와 초기화 문맥은 본문에 밝혔습니다.
- SciPy 계산 부분과 PyEpics 예제는 원본 구간을 대조했습니다. 문서의 공식 데이터 예제 재계산과 실제 장비·서버 실행 여부는 해당 본문에 구분했습니다.

초기 [언어 사용 위치 설명](../10-C와Python이쓰이는위치_languages-in-the-workflow.md)의 `status = 0x5u` 비트 연산 코드는 설명을 위해 직접 작성한 예입니다. 그 코드에는 자체 작성 표시를 두었습니다. 위 제조사·프로젝트 코드 발췌와 출처가 다릅니다.

확인 기준일은 2026-10-26입니다. 사용한 원문 구간과 입력 데이터·라이선스·대조 기록을 근거로 본문을 확인했습니다. 각 원본의 측정 환경·입력 조건·의존성을 함께 읽으실 수 있도록 링크를 남겼습니다. CC0 전문 사본은 [SPDX license-list-data v3.27.0의 표준 텍스트](https://github.com/spdx/license-list-data/blob/v3.27.0/text/CC0-1.0.txt)를 사용했습니다.

## English

This register distinguishes vendor examples, production project implementations, official tests and SQL examples from authored work scenarios. Fixed commits, source locations, modifications and license texts accompany the excerpts. Comment-only changes are checked separately from hardware execution. Published code provenance does not establish adoption by Samsung or SK hynix.
