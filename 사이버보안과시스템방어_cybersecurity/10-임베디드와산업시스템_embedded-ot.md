# 임베디드와 산업 시스템 | Embedded and OT security

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 칩부터 업데이트 서버까지 연결합니다

임베디드 시스템에는 ROM 부트 코드, 부트로더, firmware, 주변장치, 디버그 인터페이스, 통신·업데이트 경로가 있습니다. secure boot는 허용한 이미지인지 확인하는 시작 경계입니다. 서명 검증이 있어도 유효한 옛 취약 버전으로 되돌릴 수 있다면 rollback 정책이 필요합니다.

측정 부팅(measured boot)은 부팅 구성의 측정값을 남겨 후속 검증에 쓰는 방식입니다. 측정했다는 사실과 실행을 차단했다는 사실을 구분합니다. TrustZone·TPM·secure element도 각각 분리·측정·키 보호의 역할과 공격 가정이 다릅니다. [NIST SP 800-193 공식 개요의 보호·탐지·복구](https://csrc.nist.gov/pubs/sp/800/193/final)

## 전원 차단과 공격 상황을 함께 봅니다

서명된 새 firmware를 절반만 쓴 뒤 전원이 꺼지면 유효한 이미지가 사라질 수 있습니다. A/B 슬롯·검증 후 활성화·시도 횟수·상태 원자성·복구 이미지·버전 하한을 연결해야 합니다. ‘부팅 실패하면 무조건 이전 버전’은 보안상의 rollback 제한과 충돌할 수 있습니다. 복구 가능한 승인 버전과 금지 버전을 구분합니다.

| 접점 | 공격·고장 가정 | 확인할 설계 |
| --- | --- | --- |
| UART·JTAG·SWD | 개발용 관리자 기능이 현장에 남습니다. | 생산 상태의 디버그 정책·잠금·복구 권한을 정합니다. |
| 통신 프레임 | 길이·형식·순서를 신뢰한 처리가 있습니다. | 경계 검사·인증·재전송·상태 전이를 검사합니다. |
| 키 저장 | firmware 전체에서 키를 추출할 수 있습니다. | 장치별 키·보호 저장소·교체·폐기를 검토합니다. |
| 업데이트 | 유효한 서명·지원 모델·버전이 서로 다릅니다. | 대상·이미지 해시·버전·길이를 인증 범위에 연결합니다. |
| 물리 접근 | 전압·시간·전력 관측이나 fault가 가능합니다. | 필요한 공격 모델에 따라 부채널·fault 시험을 별도로 설계합니다. |

CAN의 CRC나 Ethernet의 FCS는 우발적 전송 오류를 검사하는 장치이며 송신자의 암호학적 인증과 같지 않습니다. 해당 버스의 오류 검출 기능이 있다는 이유로 위조 명령이 막힌다고 판단하지 않습니다.

## 발전·제조·운송 설비의 제약

OT는 물리 공정을 감시·제어하는 시스템을 포함합니다. 일반 IT처럼 즉시 재부팅하거나 전체 능동 스캔을 해도 되는 환경은 아닙니다. 안전·운영 연속성·제어 주기·제품 수명을 고려해 자산 파악, 구역·통신 경계, 원격 정비 접근, 시험 환경, 패치 창과 복구 절차를 설계합니다. [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final)은 이 글에서 사용하는 최종판입니다. 공식 페이지가 안내하는 Rev. 4 초안은 별도 판본입니다.

기존 [부트로더·통신·저장장치 검증 사례](../설계와검증사례_engineering-cases/README.md)는 전원 중단·상태 오류의 실행 근거로 이어 읽습니다. 고장 모델에서 통과한 결과를 보안 인증이나 실제 산업 설비 침투 시험으로 바꾸어 표시하지 않습니다.

## 원문에서 이어 읽기

- [NIST SP 800-193](https://csrc.nist.gov/pubs/sp/800/193/final): 공식 초록의 보호·탐지·복구 목적입니다.
- [NIST SP 800-82 Rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final): 공식 초록·OT의 성능·신뢰성·안전 제약입니다.
- [SEI CERT C ARR30-C](https://wiki.sei.cmu.edu/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts): 배열·포인터 범위의 규칙과 예제입니다.

## English

Embedded protection connects trusted boot, version policy, debug access and recoverable updates. OT security also depends on operational and safety constraints.
