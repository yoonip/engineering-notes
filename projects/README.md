# 프로젝트와 코드

회로·소프트웨어·AI 시스템은 문제 정의에서 설계, 구현, 검증으로 이어진다. 구현물의 기능을 설명하는 문서와 실제 실행 파일·설정·측정 데이터는 서로 연결된다.

## 구현의 단위

RTL은 회로 구조를, firmware는 장치의 실행 동작을, Python·MATLAB 코드는 계산과 분석을 표현한다. 여러 언어가 함께 쓰이는 시스템에서는 인터페이스와 데이터 형식이 각 구현을 잇는다.

현재 저장소의 계산·언어·RTL 예제는 [examples](../examples/README.md)에 모았다. RC 응답은 [수식 구현](../topics/06-math-to-code/README.md), 언어별 평균 계산은 [C·C++·Python](../topics/04-c-cpp-python/README.md), 카운터는 [RTL](../topics/13-verilog-systemverilog/README.md) 설명과 연결된다.

## 설계와 결과

요구사항은 어떤 입력과 조건에서 어떤 동작을 기대하는지 정한다. 설계는 그 동작을 만드는 구조를, 검증은 기대와 실제의 관계를 다룬다. Code·schematic·configuration·log·waveform·graph는 구현 단계마다 다른 정보를 담는다.
