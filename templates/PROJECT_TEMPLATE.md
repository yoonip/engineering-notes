# 설계 산출물의 관계

요구사항은 목표와 동작 조건을, 설계 문서는 구성요소와 인터페이스를 설명한다. 소스·회로도·설정 파일에는 구현이 담기고, 테스트·로그·파형·측정 데이터에는 실제로 관찰한 동작이 담긴다.

| 구분 | 포함되는 정보 |
| --- | --- |
| 문제 | 입력, 출력, 제한 조건 |
| 구조 | 모듈, 인터페이스, 데이터 흐름 |
| 구현 | 소스 revision, 설정, 의존성 |
| 검증 | 기대 동작, 입력 조건, 비교 기준 |
| 결과 | 관찰값, 단위, 오차, 적용 범위 |

하나의 결과에는 여러 설계 선택이 영향을 줄 수 있다. 변경 이력을 남기면 각 선택이 결과에 어떤 영향을 주었는지 추적할 수 있다.

## English

Requirements describe goals and operating conditions. Design documents describe components and interfaces. Source code, schematics, and configuration files capture the implementation; tests, logs, waveforms, and measurements capture the behavior that was observed.

| Category | Information |
| --- | --- |
| Problem | Inputs, outputs, constraints |
| Architecture | Modules, interfaces, data flow |
| Implementation | Source revision, configuration, dependencies |
| Verification | Expected behavior, input conditions, comparison criteria |
| Results | Observations, units, errors, applicable scope |

Several design choices can contribute to one result. A change history helps trace how each choice affected the outcome.
