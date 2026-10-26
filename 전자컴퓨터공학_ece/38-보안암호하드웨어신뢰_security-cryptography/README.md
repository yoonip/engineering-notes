# 보안·암호·하드웨어 신뢰 | Security, Cryptography & Hardware Trust

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

보안은 보호할 자산, 가능한 공격, 신뢰할 구성요소를 정하는 데서 시작합니다. 암호 알고리즘이 강해도 키 관리·권한·업데이트·메모리 처리에 문제가 있으면 시스템이 취약해질 수 있습니다.

## 암호의 역할

AES 같은 대칭키 암호는 공유된 비밀키로 데이터를 보호합니다. RSA·ECC 계열은 공개키 암호와 서명 등에 사용됩니다. Hash는 입력을 고정 길이 값에 대응시키며 암호화와 목적이 다릅니다. TLS는 네트워크 연결에서 인증과 기밀성·무결성을 제공합니다.

## 부팅과 실행의 신뢰

Secure boot는 실행할 코드의 신뢰성을 확인하는 부팅 체계입니다. 안전한 업데이트에는 서명 검증·버전 정책·실패 시 복구가 연결됩니다. TrustZone은 보안 상태 분리, TPM은 키와 신뢰 측정에 관련된 하드웨어 기능입니다. 인증은 신원을 확인하고, 권한 부여는 허용할 작업을 정합니다.

메모리 범위 오류·해제 후 사용·경쟁 상태는 구현 취약점으로 이어질 수 있습니다. Sanitizer는 실행 중 오류 탐지, 정적 분석은 실행 전 코드 검사, fuzzing은 다양한 입력에 대한 동작 탐색에 쓰입니다. CodeQL도 코드 분석 도구입니다. 전력·시간·전자파 같은 부채널은 소프트웨어 인터페이스 밖의 정보 노출 경로입니다.

## 관련 기술

TLS, AES, RSA, ECC, Secure Boot, TrustZone, TPM, Sanitizers, Fuzzing, CodeQL

## 참고 자료

- [OpenSSL documentation](https://docs.openssl.org/)
- [Linux Kernel documentation](https://docs.kernel.org/)


## 개념·유도·모델·검증

[기초부터 읽기](../../공학기초_foundations/README.md)

- [오류를 찾는 것과 공격을 막는 것: 신뢰성·보안의 경계](해설_notes/오류를찾는것과공격을막는것_security-and-reliability-boundaries.md)

## 저장 데이터의 주소와 버전까지 확인합니다

저장 블록의 자료와 checksum이 함께 다른 위치에서 왔다면 자료만의 검사는 맞을 수 있습니다. 파일시스템의 구조를 일관되게 만들었다는 사실도 원래의 자료를 되찾았다는 증거는 아닙니다. 검사에 어떤 주소·버전·자료를 포함하고 그 기준을 어디서 신뢰하는지 정해야 합니다.

여기서 쓰는 HMAC은 비밀 키를 이용한 메시지 인증 코드입니다. [Python hmac](https://docs.python.org/3.12/library/hmac.html)은 표준 HMAC 구현을 제공하며 외부 태그 비교에는 compare_digest를 안내합니다. 다음은 고정 길이 주소·버전 뒤에 자료를 붙여 인증 범위를 확인하는 자체 메시지 예입니다. 키는 공개된 학습용 값이며 실제 비밀이나 운영용 키가 아닙니다.

```python
import hmac  # import는 표준 HMAC 계산과 태그 비교 기능을 불러옵니다.
key = b"public-example-key"  # b는 bytes이며 이 값은 누구나 아는 예제 키입니다.
def tag(lpn, version, payload):  # def는 논리 페이지 번호·버전·자료를 받는 함수를 정의합니다.
    header = lpn.to_bytes(4, "big") + version.to_bytes(4, "big")  # 정수를 각 4바이트로 고정해 경계를 구분합니다.
    return hmac.digest(key, b"store-v1\x00" + header + payload, "sha256")  # 예제 구분자와 세 필드를 함께 인증합니다.
payload = b"DATA"  # 네 바이트 자료를 저장합니다.
old_tag = tag(1, 1, payload)  # 주소1·버전1의 유효한 이전 기록을 만듭니다.
print(hmac.compare_digest(old_tag, tag(1, 1, payload)))  # 같은 기록의 비교는 True입니다.
print(hmac.compare_digest(old_tag, tag(0, 1, payload)))  # 주소를 0으로 바꾼 비교는 False입니다.
print(hmac.compare_digest(old_tag, tag(1, 2, payload)))  # 버전을 2로 바꾼 비교는 False입니다.
expected_version, received_version = 2, 1  # 신뢰하는 최신 버전과 다시 온 이전 버전을 가정합니다.
authenticated = hmac.compare_digest(old_tag, tag(1, received_version, payload))  # 이전 기록 자체의 인증은 맞습니다.
print(authenticated, received_version == expected_version)  # True False이므로 인증과 최신성은 다릅니다.
```

주소를 바꿔치기한 메시지와 유효한 옛 메시지의 재전송은 다릅니다. HMAC이 맞아도 이미 승인한 옛 자료일 수 있습니다. 버전 하한이나 최신 버전의 기준까지 공격자가 함께 바꿀 수 있다면 단순 비교는 rollback을 막지 못합니다. 예제의 expected_version은 신뢰할 기준이 있다고 가정한 값이며, 그 기준을 안전하게 보존하는 장치는 구현하지 않습니다.

Linux [fs-verity](https://docs.kernel.org/filesystems/fsverity.html)는 읽기 전용 파일을 Merkle tree로 검증합니다. Merkle tree는 작은 자료 조각의 해시를 다시 묶어 전체를 확인하는 구조입니다. 읽는 자료의 일관성을 검사하는 기능과 파일의 기준 digest를 신뢰하는 정책은 별개입니다. 이 HMAC 예제가 fs-verity나 저장장치 암호화·secure boot를 구현한 것은 아닙니다.

이 분류의 ECC는 elliptic-curve cryptography, 타원곡선 암호를 가리킵니다. 저장장치 글의 error-correcting code도 ECC라고 줄이지만, 우발적 오류의 정정과 암호학적 인증은 목적과 전제가 다릅니다. [FTL 매핑 게시](../../설계와검증사례_engineering-cases/FTL의매핑게시와전원중단_ftl-map-publication.md)와 [주소 재사용](../../설계와검증사례_engineering-cases/FTL의GC와폐기된주소재사용_ftl-gc-trim-reuse.md)은 정상 부품에서도 잘못된 주소·세대가 자료를 바꿀 수 있는 경우를 별도 모형으로 다룹니다.

## English

### Security, cryptography, and hardware trust

Security starts with the assets to protect, possible attacks, and the components being trusted. Strong cryptographic algorithms cannot compensate for flaws in key management, permissions, updates, or memory handling.

### Roles of cryptography

Symmetric ciphers such as AES protect data with a shared secret key. RSA and elliptic-curve methods support public-key cryptography and signatures. A hash maps an input to a fixed-length value and serves a different purpose from encryption. TLS provides authentication, confidentiality, and integrity for network connections.

### Trust during boot and execution

Secure boot checks the trustworthiness of code before execution. A secure update process combines signature verification, version policy, and recovery from failure. TrustZone separates security states; TPM hardware supports keys and measurements of trust. Authentication establishes identity, while authorization determines permitted actions.

Out-of-bounds accesses, use-after-free, and race conditions can become implementation vulnerabilities. Sanitizers detect errors during execution, static analysis checks code without running it, and fuzzing explores behavior across varied inputs. CodeQL is another code-analysis tool. Power consumption, timing, and electromagnetic emissions can expose information through side channels outside the software interface.


### Concepts, derivations, models, and verification

[Foundations reading guide](../../공학기초_foundations/README.md#english)

- [Security and reliability boundaries](해설_notes/오류를찾는것과공격을막는것_security-and-reliability-boundaries.md#english)


### Address binding, authentication and freshness

The HMAC example authenticates a fixed-width logical address and version together with the payload. Changing an authenticated field fails comparison, but replaying the complete valid older record still authenticates. Freshness therefore needs an independently trusted version policy. The public teaching key supplies no real secrecy, and the example implements no protected counter or storage encryption.

Likewise, fs-verity's file-block integrity and trust in its reference digest are separate concerns. Error-correcting codes in storage are different from elliptic-curve cryptography despite the shared ECC abbreviation. The linked FTL cases separately examine address, version and physical-location mistakes under declared host models.


## 심화 해설 | Advanced article

- [인증된 메시지의 재전송: replay window](해설_notes/인증후재전송검사_authenticated-replay-window.md) · [English](해설_notes/인증후재전송검사_authenticated-replay-window.md#english)
