# DFT · Test · Manufacturing

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

DFT는 제조 후 칩 내부의 오류를 관찰하고 제어하기 쉬운 구조를 설계에 넣는 접근이다. 기능 검증이 RTL의 의도된 동작을 다룬다면 제조 테스트는 제작 과정의 결함을 검출하는 목적을 가진다.

## Scan과 pattern

Scan은 내부 register를 shift 가능한 경로로 연결해 상태를 넣고 읽게 한다. ATPG는 정해진 fault model을 검출하는 입력 pattern을 생성한다. Stuck-at·transition 같은 모델은 실제 결함을 추상화하며 coverage의 의미는 사용한 모델에 달려 있다.

## 내장 테스트와 양산

BIST는 칩 안에서 테스트를 수행하는 구조다. MBIST는 메모리, LBIST는 논리 회로의 테스트에 사용된다. JTAG·boundary scan은 외부 연결과 테스트 접근에도 쓰인다. Tessent·TestMAX·Modus는 관련 상용 도구 생태계다.

ATE는 테스트 장비이고 wafer·package·system 단계는 관측 조건과 비용이 다르다. Yield는 검사 기준을 통과하는 비율이며 공정·설계·테스트 조건과 연결된다. Test time·pattern volume·coverage·전력은 양산 테스트의 선택을 좌우한다. 수명과 환경 스트레스에 대한 신뢰성 평가는 순간적인 기능 통과와 다른 축이다.

## 관련 기술

DFT, Scan, ATPG, MBIST/LBIST, ATE, JTAG/Boundary Scan, Tessent, TestMAX, Modus

## 참고 자료

- [Siemens Tessent](https://eda.sw.siemens.com/en-US/ic/tessent/)
