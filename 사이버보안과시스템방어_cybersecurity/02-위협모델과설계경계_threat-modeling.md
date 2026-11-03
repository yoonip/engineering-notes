# 위협 모델과 설계 경계 | Threat modeling

[분야 목차](README.md) · [용어](용어_glossary.md) · [출처와 판본](출처_sources.md)

## 시스템을 그린 뒤 공격 가정을 정합니다

위협 모델은 누가 어떤 입력·권한을 갖고 어떤 자산을 해칠 수 있는지 정리한 설계 모델입니다. 모든 것을 공격할 수 있다고 가정하면 설계 결정을 할 수 없습니다. 외부 사용자, 다른 고객 계정, 내부 운영자, 탈취된 CI 토큰처럼 서로 다른 출발 권한을 구분합니다.

문서 검색 서비스를 예로 들면 브라우저→API→인증 계층→검색 인덱스→원문 저장소의 흐름을 먼저 적습니다. 검색 인덱스가 문서의 조직 ID를 잃어버렸다면 최종 화면에서 숨기기 전에 이미 다른 조직의 내용이 모델 입력으로 들어갈 수 있습니다. 데이터 흐름 그림은 화면보다 먼저 자료가 노출되는 지점을 찾는 데 도움이 됩니다. [OWASP Threat Modeling의 시스템 모델·위협 식별 절](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)

```mermaid
flowchart LR
 U["외부 사용자"] --> A["API: 인증·입력 제한"]
 A --> P["권한 정책"]
 P --> R["조직별 검색·원문 저장소"]
 R --> M["AI: 자료를 읽고 응답 제안"]
 M --> G["도구 게이트: 다시 권한 검사"]
 G --> R
```

## STRIDE는 질문을 빠뜨리지 않는 도구입니다

| 범주 | 의미 | 자체 설계 질문과 대응 |
| --- | --- | --- |
| Spoofing | 신원 위조입니다. | 요청의 user 필드를 신뢰하지 않고 검증된 세션에서 주체를 정합니다. |
| Tampering | 자료 변조입니다. | 서명·인증 태그의 범위에 대상·버전·본문을 함께 넣습니다. |
| Repudiation | 행위 부인입니다. | 누구의 어떤 권한으로 무엇을 했는지 감사 기록을 남깁니다. |
| Information disclosure | 정보 노출입니다. | 결과뿐 아니라 로그·캐시·모델 입력의 권한도 확인합니다. |
| Denial of service | 서비스 거부입니다. | 입력 크기·실행 시간·동시 요청·비용에 한도를 둡니다. |
| Elevation of privilege | 권한 상승입니다. | 일반 작업과 관리 작업의 자격증명을 분리합니다. |

STRIDE의 범주를 모두 채웠다고 안전성이 증명되지는 않습니다. 사업 규칙도 살펴야 합니다. ‘환불은 구매액 이하’라는 규칙은 메모리 오류가 없어도 동시에 두 요청이 승인되면 깨질 수 있습니다. DB 트랜잭션·고유 제약·중복 키를 사용해 여러 실행이 합쳐졌을 때의 결과를 검토합니다.

## 요구사항을 시험 가능한 문장으로 바꿉니다

‘자료를 안전하게 보호합니다’ 대신 ‘다른 tenant의 문서 ID를 보낸 요청은 본문을 반환하지 않습니다’라고 적습니다. 정상·권한 없음·없는 ID·삭제된 계정·권한 변경 뒤의 캐시를 시험합니다. 위험 기록에는 자산, 공격자 권한, 입력 경로, 영향, 대응 담당자, 완료 판정과 남은 가정을 붙입니다.

신뢰 경계는 ‘외부망과 내부망 사이’만이 아닙니다. 같은 프로세스 안의 모델 출력과 실행기 사이, 고객 A와 B의 인덱스 사이에도 있습니다. 기능이나 연결 도구가 추가되면 모델을 다시 읽습니다. [OWASP ASVS의 검증 요구사항 안내](https://owasp.org/www-project-application-security-verification-standard/)

## 원문에서 이어 읽기

- [OWASP Threat Modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html): 시스템 모델·위협 식별·완화·검토의 절입니다.
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 검증 요구사항·판본·프로젝트 목적입니다.

## English

Threat modeling follows data and authority across components. Concrete requirements need negative tests and explicit assumptions.
