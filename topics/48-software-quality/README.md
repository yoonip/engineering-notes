# Software Design & Quality

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

소프트웨어 품질은 코드를 짧게 쓰는 것보다 요구한 동작이 유지되고 변경의 영향을 이해할 수 있는가에 가깝다. 모듈 경계, 데이터 소유권, 오류 처리, 테스트 가능성이 유지보수와 연결된다.

## 테스트의 범위

단위 테스트는 작은 구성요소, 통합 테스트는 연결, 시스템 테스트는 전체 동작을 다룬다. Property-based test는 특정 예시 대신 항상 성립해야 하는 성질과 입력 생성을 이용한다. 회귀 테스트는 이전에 해결한 문제나 유지할 동작을 확인한다. 구현을 그대로 복제한 테스트는 같은 오류를 함께 가질 수 있다.

## 분석과 진단

pytest·unittest는 Python, GoogleTest·Catch2·CTest는 C/C++ 테스트 생태계다. Hypothesis는 속성 기반 입력 생성에 쓰인다. ASan·UBSan·TSan·Valgrind는 메모리·정의되지 않은 동작·동시성 등의 진단에, clang-tidy·Ruff는 정적 검사와 코드 정리에 사용된다.

Profiler는 시간을 쓰는 위치, 메모리 도구는 할당·수명과 접근, log는 실행 중 사건을 보여준다. 코드 리뷰에서는 API의 계약과 경계 입력, 실패 시 상태, 변경 범위를 함께 읽는다. 주석은 코드가 이미 말하는 동작을 반복하기보다 선택의 이유와 제약을 남길 때 유용하다.

## 관련 기술

pytest, unittest, GoogleTest, Catch2, CTest, Hypothesis, Valgrind, ASan/UBSan/TSan, clang-tidy, Ruff

## 참고 자료

- [pytest documentation](https://docs.pytest.org/en/stable/)
