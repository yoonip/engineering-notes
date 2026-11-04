# BGP 경로 보안과 RPKI 원점 검증 | BGP route security and RPKI origin validation

자료 확인일: 2026-11-04

## 이 장에서 다루는 범위

인터넷 사업자와 대형 네트워크는 BGP(Border Gateway Protocol)로 서로 도달 가능한 IP 경로를 알립니다. BGP가 잘못된 경로를 받아들이거나 내보내면 트래픽이 엉뚱한 네트워크로 향하거나 일부 서비스에 도달하지 못할 수 있습니다. 원인은 고의적인 경로 탈취만이 아니라 주소·AS 설정 오류, 정책 누락, 경로 누출일 수도 있습니다.

이 장은 주소 블록 보유자가 특정 AS가 해당 prefix를 원점(origin)으로 알리도록 허용했는지 확인하는 RPKI 기반 원점 검증(ROV)을 설명합니다. ROV가 AS 경로 전체를 인증하거나 모든 경로 누출을 막는 기능은 아니라는 점도 구분합니다.

## BGP 경로에서 확인할 것

BGP UPDATE는 목적지 prefix와 AS_PATH 등 경로 속성을 전달합니다. AS_PATH는 경로가 거쳐 온 자율 시스템(AS)을 나타내며, 원점 AS는 BGP 규격이 정한 방식으로 이 경로 속성에서 도출합니다. 기본 BGP만으로는 이 정보가 주소 자원 보유자의 허가를 받았는지 암호학적으로 확인하지 않습니다.

| 문제 | 뜻 | 예시 |
| --- | --- | --- |
| 원점 오류·원점 탈취 | prefix를 허가받지 않은 AS가 원점이라고 광고합니다. | AS가 다른 조직의 주소 블록을 자기 경로로 발표합니다. |
| 경로 누출 | 이웃 관계상 전달하면 안 되는 경로를 다른 peer나 provider에 광고합니다. | 고객에게서 배운 transit 경로를 다른 transit 사업자에게 전달합니다. |
| 정책 누락 | import·export 조건이 없거나 잘못되어 예상보다 많은 경로를 받아들이거나 내보냅니다. | 신규 eBGP 세션에 고객 prefix 제한을 설정하지 않습니다. |

ROV는 첫 번째 문제의 일부를 줄입니다. 경로 누출과 과도한 광고는 별도 경로 정책과 BGP 관계 통제가 필요합니다.

## RPKI에서 라우터의 경로 판정까지

RPKI(Resource Public Key Infrastructure)는 인터넷 주소와 AS 번호의 할당 관계를 공개키 인증서와 서명된 객체로 표현하는 체계입니다. 주소 보유자는 ROA(Route Origin Authorization)를 만들어 자신의 prefix를 원점으로 광고할 수 있는 AS 번호와 허용할 prefix 길이를 지정합니다.

ROA는 검증된 경로 자체가 아니라 허용 정책을 표현합니다. 검증 소프트웨어는 RPKI 저장소의 인증서·서명된 객체를 확인해 VRP(Validated ROA Payload) 자료를 만듭니다. 라우터는 대개 RPKI-RTR 프로토콜로 신뢰하도록 구성한 cache에서 검증된 prefix·origin AS·maxLength 자료를 받고 BGP 경로에 로컬 검증 상태를 붙입니다.

    주소 보유자 → ROA 생성·게시 → RPKI 저장소
                                  ↓ 서명·인증서 검증
                         검증 cache / VRP 집합
                                  ↓ RPKI-RTR
    BGP UPDATE → 라우터가 prefix·origin AS 대조 → Valid / Invalid / NotFound
                                                ↓
                                         운영자가 정한 정책

RPKI-RTR cache와 라우터 사이의 신뢰 관계도 보호 경계입니다. 라우터는 어느 cache를 신뢰할지 정하고, cache의 갱신 상태와 연결 상태를 확인해야 합니다. 규격과 구현에 따라 전송 보호 방식은 다르므로 운영자는 해당 장비의 버전·설정 문서에서 cache 인증과 전송 보호 조건을 확인해야 합니다.

## Valid, Invalid, NotFound 판정

VRP는 허용 prefix, 허용 원점 AS 번호, 최대 prefix 길이로 구성됩니다. VRP의 prefix가 BGP 경로 prefix를 포함하고, 경로 길이가 maxLength 이하이며, 원점 AS가 같으면 해당 VRP와 경로가 일치합니다. 하나라도 일치하는 VRP가 있으면 Valid입니다. 어떤 VRP가 prefix를 포함하지만 일치하는 항목이 하나도 없으면 Invalid입니다. prefix를 포함하는 VRP가 전혀 없으면 NotFound입니다.

| 상태 | 판정 | 해석 |
| --- | --- | --- |
| Valid | 최소 한 VRP가 prefix·길이·원점 AS 모두와 일치합니다. | 게시된 ROA 중 경로를 허용하는 항목이 있습니다. |
| Invalid | prefix를 포함하는 VRP가 있지만 어떤 항목도 경로와 일치하지 않습니다. | AS 번호가 다르거나 maxLength보다 더 구체적인 경로입니다. 실제 공격과 ROA 오설정을 모두 의심합니다. |
| NotFound | 경로 prefix를 포함하는 VRP가 없습니다. | 이 경로에 적용할 ROA 근거가 없습니다. 정당성 또는 악성 여부를 판정한 상태가 아닙니다. |

예시에서는 문서용 IPv4 prefix 198.51.100.0/24와 문서용 AS 번호 64500을 사용합니다. 가정한 VRP는 prefix 198.51.100.0/24, maxLength 24, 원점 AS 64500입니다.

| BGP에서 관측한 경로 | 상태 | 이유 |
| --- | --- | --- |
| 198.51.100.0/24, AS64500 | Valid | prefix·길이·원점 AS가 VRP와 일치합니다. |
| 198.51.100.0/25, AS64500 | Invalid | /25는 /24보다 구체적이고 maxLength 24를 넘습니다. |
| 198.51.100.0/24, AS64501 | Invalid | prefix는 포함되지만 원점 AS가 허용값과 다릅니다. |
| 203.0.113.0/24, AS64500 | NotFound | 이 prefix를 포함하는 VRP가 없습니다. |

이 prefix와 AS 번호는 RFC 문서에서 예시에 쓰도록 예약한 값입니다. 실제 인터넷 광고나 운영 설정에 사용하면 안 됩니다. 표는 RFC 6811 판정 규칙을 손으로 적용한 예시이며, 공개 라우터나 RPKI cache에 질의한 결과가 아닙니다.

## 판정 로직을 읽는 Python 예제

다음 코드는 RFC 6811의 세 상태 분류를 이해하기 위한 교육용 구현입니다. 입력은 이미 RPKI 서명 검증을 마친 VRP 목록이라고 가정합니다. 인증서·manifest·ROA 서명 검증, cache 동기화, BGP 정책 결정, 운영 장애 처리는 구현하지 않습니다. 실제 RPKI 검증기나 라우터 기능을 대신하지 않습니다.

    import ipaddress  # Python 표준 라이브러리로 IPv4·IPv6 network를 해석합니다.
    
    def origin_state(route_prefix, origin_asn, vrps):  # 경로와 검증된 VRP 목록을 받아 상태를 계산합니다.
        route = ipaddress.ip_network(route_prefix)  # BGP 경로 prefix를 network 객체로 바꿉니다.
        covered = False  # prefix를 포함하는 VRP가 있었는지 기록합니다.
        for vrp in vrps:  # 이미 서명 검증된 VRP를 하나씩 확인합니다.
            authorized = ipaddress.ip_network(vrp["prefix"])  # VRP의 허용 prefix를 읽습니다.
            if route.version != authorized.version or not route.subnet_of(authorized):  # 주소 계열이 다르거나 허용 prefix 밖이면 건너뜁니다.
                continue  # 현재 VRP는 이 경로를 허용할 수 없습니다.
            covered = True  # 허용 prefix가 경로를 포함하므로 Invalid 가능성이 있습니다.
            length_ok = route.prefixlen <= vrp["max_length"]  # 광고 길이가 VRP의 최대 길이를 넘지 않는지 확인합니다.
            asn_ok = origin_asn == vrp["asn"]  # 경로의 원점 AS가 VRP에서 허용한 AS인지 확인합니다.
            if length_ok and asn_ok:  # 두 조건이 모두 맞으면 일치하는 VRP가 있습니다.
                return "Valid"  # RFC 6811 규칙에 따라 Valid를 반환합니다.
        return "Invalid" if covered else "NotFound"  # 포함 VRP가 있으면 Invalid, 없으면 NotFound입니다.

가정한 VRP가 하나이고 위 표와 같은 경로를 넣으면 첫 번째 경로는 Valid, 더 긴 /25 경로와 다른 AS의 /24 경로는 Invalid, 별도 prefix 203.0.113.0/24는 NotFound가 됩니다. 이 결과는 예제 로직으로 계산한 것이며 로컬 실행·라우터 판정·운영 환경 검증 결과는 아닙니다.

코드는 prefix 포함 관계에 Python의 ipaddress 네트워크 객체와 subnet_of 메서드를 사용합니다. VRP의 AS 번호와 maxLength가 올바른 형식인지, prefix가 정규화되어 있는지 검사는 생략했습니다. 실제 검증기에서 입력 파싱·서명 검증·정책 검사는 별도 필수 단계입니다.

## maxLength는 범위를 좁혀 설정합니다

ROA의 maxLength는 해당 AS가 광고할 수 있는 더 구체적인 prefix 길이의 상한입니다. 예를 들어 /16 주소 블록을 /24까지 세분해 광고할 계획이 있다고 해서, 언제나 /16 ROA 하나에 maxLength 24를 붙이는 것이 적절한 것은 아닙니다. 넓은 허용 길이는 운영상 편리할 수 있지만 실제 광고하지 않는 하위 prefix까지 해당 AS가 원점으로 주장할 수 있게 하여, 잘못된 하위 prefix 광고를 Valid로 만들 수 있습니다.

RFC 9319는 필요하지 않은 maxLength 확장을 피하고 실제 광고 구조에 맞춘 ROA를 만들도록 설명합니다. 주소 보유자는 실제 운용 prefix와 원점 AS를 먼저 목록화하고, 이중 연결·DDoS 우회·사업자 변경 같은 예외 경로를 포함할지 네트워크 사업자와 확인해야 합니다. 다중 사업자 환경에서는 각 prefix를 실제로 원점 광고하는 AS를 ROA에 정확히 반영합니다. AS_PATH 안에 경유 AS가 있다는 이유만으로 그 AS를 ROA에 추가하지 않습니다.

운영 중 원점 AS나 prefix 길이가 바뀌면 ROA도 갱신해야 합니다. 기존 광고를 먼저 막거나 제거하기 전에 새 ROA가 공개되고 검증 cache에 전달되는 순서를 계획합니다. ROA 변경 뒤에는 authoritative 경로 데이터, 주요 공개 관측 지점, 내부 cache의 VRP 상태가 예상과 같은지 확인합니다.

## ROV와 다른 BGP 방어 수단

| 방어 수단 | 주로 다루는 문제 | ROV와의 관계 |
| --- | --- | --- |
| RPKI ROV | prefix를 허가된 원점 AS가 광고하는지 확인합니다. | prefix·원점 AS·maxLength를 비교합니다. |
| import/export prefix filter | 이웃별 허용 prefix와 경로 수를 제한합니다. | ROA가 없거나 잘못된 상태의 피해를 줄이는 별도 경계입니다. |
| RFC 8212 기본 거부 정책 | 명시적 정책 없이 eBGP 경로를 받아들이거나 내보내지 않게 합니다. | ROV 결과만 믿지 않고 세션별 경로 정책을 구성합니다. |
| BGP Roles와 OTC | 이웃 관계에 어긋나는 경로 누출을 감지·방지합니다. | ROV와 다른 위협을 대상으로 하며 함께 사용할 수 있습니다. |
| BGP 세션·제어면 보호 | BGP 세션 접근과 라우터 자체의 관리면을 보호합니다. | 공격자가 이웃 세션이나 장비 설정을 바꾸는 경로를 줄입니다. |

ROV가 확인하는 것은 광고된 prefix의 원점 AS입니다. 중간 AS_PATH의 모든 AS가 실제 경로와 일치하는지, 경로가 고객·peer·provider 관계에 맞게 전달됐는지는 확인하지 않습니다. 합법적인 원점 AS가 다른 사업자에서 배운 경로를 잘못 내보내면 원점 검증은 Valid인데도 route leak일 수 있습니다. RFC 9234의 BGP Role과 Only-to-Customer(OTC) 속성은 이웃 관계에 따른 전파 규칙을 별도로 다룹니다.

Invalid 경로를 거부할지 선호도를 낮출지는 운영 정책의 결정입니다. 잘못된 ROA 하나가 정당한 경로를 Invalid로 만들 수 있으므로, 적용 전 route collector·RPKI cache·고객의 실제 광고를 대조합니다. NotFound를 Invalid와 동일하게 차단하는 정책은 별도로 정당화해야 합니다. 검증 상태만 저장하고 자동 폐기하지 않는 동작과 상태를 정책으로 적용하는 동작을 구별합니다.

## 배포와 점검 순서

1. 주소 블록, 실제 원점 AS, 정상·예비 prefix 길이, 상위 사업자의 경로 재광고 방식을 확인합니다.
2. 기존 공개 ROA와 현재 BGP 광고를 대조해 누락·충돌·불필요하게 긴 maxLength를 찾습니다.
3. 신규·변경 ROA가 검증 cache에 도달하는 시간과 회수 절차를 확인합니다.
4. 라우터의 cache 연결·갱신 시간·세션 상태와 VRP 수 변화를 감시합니다. 모든 VRP 수가 0이 되는 상태를 정상적인 전체 withdrawal로 오인하지 않도록 경보를 둡니다.
5. 처음에는 검증 상태를 관측하고, 고객·peer·예비 경로를 포함한 경로 표본과 비교합니다.
6. Invalid 처리 정책을 적용할 때에는 잘못된 ROA가 정당한 경로를 차단했을 때 되돌릴 담당자와 절차를 마련합니다.
7. import·export filter, 최대 prefix 수, BGP 세션 보호, BGP Roles·OTC를 별도로 검토합니다.
8. 변경 후 RIB와 실제 광고를 비교하고, 외부 경로 관측 결과 및 서비스 도달성으로 정상 경로를 확인합니다.

RPKI-RTR cache 연결이 끊기거나 자료가 갱신되지 않으면 라우터가 오래된 검증 자료로 경로를 분류할 수 있습니다. cache를 이중화하고 마지막 성공 갱신 시각, serial, session reset, cache별 데이터 차이를 감시합니다. cache가 새 자료를 제공할 수 없는 상황에서 경로를 모두 허용할지, 기존 상태를 유지할지, 일부 경로에만 fail closed할지는 구현과 정책에 따라 달라지므로 장비별 동작을 확인하고 사전에 정해야 합니다.

## 경로 이상이 생겼을 때

경로 이상을 보았다고 곧바로 공격으로 단정하지 않습니다. 먼저 영향을 받는 prefix와 관측 시각, AS_PATH, 원점 AS를 보존합니다. 내부 라우터의 ROV 상태, RPKI cache의 VRP와 갱신 시각, 공개 route collector의 광고를 비교합니다.

- Invalid이면 ROA의 원점 AS·maxLength가 실제 광고 계획과 맞는지 먼저 확인합니다. 정당한 운영 변경으로 생긴 오류인지, 허가받지 않은 원점 광고인지 추가 근거를 확인합니다.
- NotFound이면 이 prefix에 ROA가 없는지 확인합니다. NotFound만으로 침해를 증명하거나 정당성을 보장할 수 없습니다.
- Valid이지만 경로가 비정상적이면 AS_PATH와 이웃 관계를 살핍니다. origin validation은 경로 누출을 검출하지 못할 수 있습니다.
- 잘못된 ROA가 원인이라면 주소 보유자와 registry/RIR 절차를 통해 수정하고 cache 반영을 확인합니다. 정상 경로가 돌아오기 전까지 검증을 무조건 끄는 조치를 피합니다.
- 실제 원점 탈취나 경로 누출이 의심되면 transit 사업자·peer·주소 보유자와 연락해 광고 철회와 정책 적용을 조정합니다. 변경 전후 상태와 승인 기록을 남깁니다.

## English summary

RPKI Route Origin Validation checks whether a BGP route’s prefix, prefix length, and origin AS match at least one validated ROA payload. The result is Valid, Invalid, or NotFound; these are local route attributes whose treatment depends on configured policy. ROV validates the origin AS, not every AS_PATH hop, and therefore does not by itself prevent route leaks. Accurate ROAs, carefully scoped maxLength values, healthy and trusted RPKI caches, explicit eBGP import/export filters, and separate route-leak controls are needed for an operational defense.

## 출처

- [RFC 6480, An Infrastructure to Support Secure Internet Routing](https://www.rfc-editor.org/rfc/rfc6480.html), §2·§3·§6: RPKI 구조, route origination authorization, repository와 cache 운영입니다.
- [RFC 6482, A Profile for Route Origin Authorizations (ROAs)](https://www.rfc-editor.org/rfc/rfc6482.html), §3·§4: ROA의 prefix·AS 번호·maxLength 구조입니다.
- [RFC 6811, BGP Prefix Origin Validation](https://www.rfc-editor.org/rfc/rfc6811.html), §2·§3·§5: Valid·Invalid·NotFound 판정, 검증 상태와 로컬 정책의 분리입니다.
- [RFC 8481, Clarifications to BGP Origin Validation Based on RPKI](https://www.rfc-editor.org/rfc/rfc8481.html), §4·§5: 경로 상태를 설정하는 동작과 별도 운영 정책입니다.
- [RFC 8210, The RPKI to Router Protocol, Version 1](https://www.rfc-editor.org/rfc/rfc8210.html), §3·§4·§8·§9: cache와 라우터 간 VRP 전달, session·갱신·전송 보호 고려사항입니다.
- [RFC 9319, The Use of maxLength in the RPKI](https://www.rfc-editor.org/rfc/rfc9319.html), §2·§3: maxLength 선택과 더 구체적인 경로 허용 범위의 위험입니다.
- [RFC 7454, BGP Operations and Security](https://www.rfc-editor.org/rfc/rfc7454.html), §4·§5·§6·§8·§9: BGP 세션·제어면·prefix filter·최대 prefix·AS_PATH 운영 보안입니다.
- [RFC 8212, Default External BGP Route Propagation Behavior without Policies](https://www.rfc-editor.org/rfc/rfc8212.html), §1·§3: eBGP import·export 정책이 명시되지 않았을 때의 기본 거부 동작입니다.
- [RFC 7908, Problem Definition and Classification of BGP Route Leaks](https://www.rfc-editor.org/rfc/rfc7908.html), §2·§3: route leak의 작업 정의와 분류입니다.
- [RFC 9234, Route Leak Prevention and Detection Using Roles in UPDATE and OPEN Messages](https://www.rfc-editor.org/rfc/rfc9234.html), §3·§4·§5: BGP Role과 OTC를 사용한 route leak 예방·탐지입니다.
- [RFC 8893, RPKI Origin Validation for BGP Export](https://www.rfc-editor.org/rfc/rfc8893.html), §3·§4: export policy 적용 시 effective origin AS를 검증하는 조건입니다.
- [RFC 5398, Autonomous System Number Reservation for Documentation Use](https://www.rfc-editor.org/rfc/rfc5398.html), §2·§4: 문서 예시용 AS 번호 64496–64511입니다.
- [RFC 5737, IPv4 Address Blocks Reserved for Documentation](https://www.rfc-editor.org/rfc/rfc5737.html), §3·§4: 문서 예시용 IPv4 prefix입니다.
- [Python ipaddress documentation](https://docs.python.org/3/library/ipaddress.html), IP network·subnet_of API: 교육 예제의 주소 prefix 판독입니다.

출처는 2026-11-04에 확인했습니다. 코드는 RFC의 판정 개념을 설명하려고 직접 작성한 축약 예제입니다. 실행 결과나 상용 라우터 설정·RPKI 검증기 구현으로 제시하지 않습니다.
