# Security · Cryptography · Hardware Trust

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

보안은 보호할 자산, 가능한 공격, 신뢰하는 구성요소를 정의하는 데서 시작한다. 암호 알고리즘이 강해도 키 관리·권한·업데이트·메모리 처리에 문제가 있으면 시스템이 취약해질 수 있다.

## 암호의 역할

AES 같은 대칭키 암호는 공유된 비밀키로 데이터를 보호한다. RSA·ECC 계열은 공개키 암호와 서명 등에 사용된다. Hash는 입력을 고정 길이 값에 대응시키며 암호화와 목적이 다르다. TLS는 네트워크 연결의 인증과 기밀성·무결성을 구성한다.

## 부팅과 실행의 신뢰

Secure boot는 실행할 코드의 신뢰성을 확인하는 부팅 체계다. 안전한 업데이트에는 서명 검증·버전 정책·실패 시 복구가 연결된다. TrustZone은 보안 상태 분리, TPM은 키와 신뢰 측정에 관련된 하드웨어 기능이다. 인증은 누군지 확인하는 일, 권한 부여는 무엇을 할 수 있는지 결정하는 일이다.

메모리 범위 오류·해제 후 사용·경쟁 상태는 구현 취약점으로 이어질 수 있다. Sanitizer는 실행 중 오류 탐지, 정적 분석은 실행 전 코드 검사, fuzzing은 다양한 입력에 대한 동작 탐색에 쓰인다. CodeQL도 코드 분석 도구다. 전력·시간·전자파 같은 부채널은 소프트웨어 인터페이스 밖의 정보 노출 경로다.

## 관련 기술

TLS, AES, RSA, ECC, Secure Boot, TrustZone, TPM, Sanitizers, Fuzzing, CodeQL

## 참고 자료

- [OpenSSL documentation](https://docs.openssl.org/)
- [Linux Kernel documentation](https://docs.kernel.org/)
