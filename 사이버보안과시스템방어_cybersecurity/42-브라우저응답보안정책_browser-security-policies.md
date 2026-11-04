# 브라우저 응답 보안 정책 | Browser Response Security Policies

자료 확인일: 2026-11-04

HTTP 응답 보안 정책은 서버가 브라우저에 어떤 콘텐츠를 불러오고 실행할지, 다른 출처의 응답을 읽거나 페이지를 frame에 넣을 수 있는지, 이후 접속을 HTTPS로 제한할지 알려 줍니다. 대표 정책은 Content Security Policy(CSP), Cross-Origin Resource Sharing(CORS), HTTP Strict Transport Security(HSTS)입니다. 이들은 서로 다른 질문에 답하며, 브라우저 밖의 client나 서버의 인증·권한 검사를 대신하지 않습니다.

이 장은 정책의 목적과 배포 순서를 설명합니다. 아래 헤더는 서비스 요구에 맞춰 수정해야 하는 예시이며, 어떤 사이트에 그대로 적용하면 정상 기능이 끊길 수 있습니다. 실제 웹 서비스에 설정을 배포하거나 브라우저 호환성을 시험한 결과는 아닙니다.

## 브라우저가 판단하는 보안 경계

`origin`은 scheme, host, port 조합으로 페이지의 출처를 구분합니다. Same-Origin Policy는 한 origin에서 실행되는 script가 다른 origin의 데이터를 마음대로 읽지 못하게 하는 브라우저의 기본 경계입니다. CORS는 서버가 응답을 특정 다른 origin의 script와 공유해도 된다고 선언하는 예외 정책입니다. 따라서 CORS는 `서버에 요청을 보낼 수 있는가`보다 `브라우저 script가 응답을 읽을 수 있는가`에 초점을 둡니다. HTML form이 보낼 수 있는 일부 요청은 preflight 없이 전송될 수 있으므로 CORS를 CSRF 방어로 사용하지 않습니다. [Fetch Standard §3.3](https://fetch.spec.whatwg.org/#cors-protocol) · [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)

| 제어 | 브라우저에 알리는 내용 | 해결하지 않는 문제 |
| --- | --- | --- |
| CSP | 현재 문서가 script, image, style, frame, form 목적지 등 어떤 콘텐츠를 허용할지 정합니다. | 입력 검증·출력 인코딩·권한 검사를 대신하지 않습니다. XSS가 발생한 원인을 수정하지도 않습니다. |
| CORS | 어떤 origin의 브라우저 script가 응답을 읽을 수 있는지 정합니다. | API 인증·인가를 하지 않습니다. `curl`, 서버 간 통신 등 브라우저 밖의 요청자를 막지 않습니다. |
| HSTS | 브라우저가 이후 해당 host에 HTTPS로만 연결하고, 잘못된 TLS 인증서 오류를 사용자가 우회하지 못하게 합니다. | 최초 방문의 HTTP 요청을 기본적으로 보호하지 않고, 애플리케이션의 접근 권한도 검사하지 않습니다. |
| `frame-ancestors` | 어떤 origin이 현재 문서를 frame·iframe에 포함할 수 있는지 정합니다. | 비밀번호 재사용·인증 우회 등 clickjacking 이외의 문제를 해결하지 않습니다. |
| `X-Content-Type-Options: nosniff` | 브라우저가 선언된 MIME type과 다른 형식으로 응답을 추측해 해석하지 않게 합니다. | 잘못된 MIME type이나 안전하지 않은 파일 처리 자체를 고치지는 않습니다. |
| `Referrer-Policy` | 다른 요청에 `Referer`로 어느 정도의 페이지 주소 정보를 보낼지 정합니다. | URL query에 비밀을 넣는 잘못된 설계를 바로잡지 않습니다. |
| `Permissions-Policy` | 페이지와 iframe이 카메라, 위치, microphone 같은 browser 기능을 사용할 수 있는 범위를 정합니다. | 사용자 계정 권한, 기기 OS 권한, 서버 API 권한을 대신하지 않습니다. |

## CORS는 응답 공유 정책입니다

API가 한정된 웹 앱 origin에만 응답을 공유해야 한다면 요청의 `Origin` 값이 정확히 허용 목록에 있는지 비교하고, 그때만 `Access-Control-Allow-Origin`을 돌려줍니다. 자격 증명 cookie를 쓰는 경우에는 허용된 origin을 구체적으로 지정하고 `Access-Control-Allow-Credentials: true`를 함께 사용할 수 있습니다. 자격 증명 요청에서 `Access-Control-Allow-Origin: *`는 브라우저가 허용하지 않습니다. 요청 origin에 따라 응답 헤더가 달라지는 서버는 cache가 한 origin의 응답 정책을 다른 origin에 재사용하지 않도록 `Vary: Origin`을 설정해야 합니다. [Fetch Standard §3.3](https://fetch.spec.whatwg.org/#cors-protocol)

다음은 하나의 정해진 웹 앱 출처에 cookie 기반 응답을 허용하는 형식 예입니다. 여러 origin을 무조건 반사하는 동적 설정이 아니며, 해당 서비스에 다른 출처 공유가 필요하지 않으면 CORS를 열지 않는 편이 낫습니다.

```http
Access-Control-Allow-Origin: https://app.example
Access-Control-Allow-Credentials: true
Vary: Origin
```

`Access-Control-Allow-Origin`에 요청의 `Origin`을 검증 없이 그대로 복사하거나, 사용자 입력을 기준으로 허용 출처를 만들어서는 안 됩니다. preflight는 브라우저가 실제 요청 전에 method·header 사용 가능 여부를 묻는 절차이지 로그인·권한 검사 절차가 아닙니다. 서버는 모든 요청에 대해 사용자 인증, 객체별 권한 확인, CSRF 방어를 별도로 수행합니다. 특히 state-changing 요청은 CORS가 응답을 숨겨 주리라 기대하지 말고 CSRF token, 적절한 cookie `SameSite`, `Origin` 검증 등 서비스에 맞는 방어를 구성합니다. [MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) · [MDN CSRF](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF)

## CSP는 리소스 출처와 script 실행을 제한합니다

CSP(Content Security Policy)는 브라우저가 페이지에 불러올 수 있는 리소스와 script 실행 조건을 적용합니다. CSP를 `script-src https:`처럼 넓은 허용 목록으로 만들면 의도치 않은 script 출처도 허용할 수 있습니다. OWASP는 nonce 기반 또는 hash 기반 strict CSP를 설명하며, nonce는 매 HTTP 응답마다 새로 만든 예측하기 어려운 값이어야 합니다. 공통 middleware가 모든 script tag에 nonce를 일괄 추가하면 주입된 script까지 허용할 수 있으므로, 신뢰된 template 요소에만 nonce를 넣어야 합니다. [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)

아래는 정책 후보를 관찰하기 위한 형식 예입니다. `{PER_RESPONSE_RANDOM}`은 모든 응답마다 새로 생성해야 하는 nonce 자리표시자이며 실제 값이나 고정 문자열로 사용하지 않습니다. Report-Only 모드는 위반을 보고하지만 차단하지 않으므로 운영 정책 그 자체로 남겨 두어서는 안 됩니다.

```http
Reporting-Endpoints: csp-endpoint="https://app.example/csp-reports"
Content-Security-Policy-Report-Only: default-src 'self'; script-src 'nonce-{PER_RESPONSE_RANDOM}' 'strict-dynamic'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'; report-to csp-endpoint
```

서버 endpoint로 위반 보고를 보내려면 `Reporting-Endpoints`에 목적지를 정의하고 CSP에 `report-to`를 지정해야 합니다. 브라우저별 지원 차이가 있어 기존 `report-uri` 호환성이 필요한지도 확인합니다. 보고 전송을 구성하지 않으면 서버 endpoint로 보고가 전달되지 않습니다. [MDN Report-Only 헤더 안내](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy-Report-Only)

| 지시자 | 이 예에서 하는 일 |
| --- | --- |
| `default-src 'self'` | 다른 리소스별 지시자가 없을 때 같은 origin을 기본 출처로 삼습니다. 외부 CDN, 이미지, font 등 서비스 의존성을 확인해야 합니다. |
| `script-src 'nonce-…' 'strict-dynamic'` | 응답 nonce가 붙은 script를 신뢰 대상으로 지정합니다. `strict-dynamic`은 신뢰된 script가 동적으로 추가한 script에도 신뢰를 이어 줄 수 있어 loader 구조를 점검해야 합니다. |
| `object-src 'none'` | Flash와 같은 plugin object 콘텐츠를 차단합니다. |
| `base-uri 'none'` | 문서의 base URL을 바꿔 상대 URL 해석을 바꾸는 `<base>` 요소를 허용하지 않습니다. |
| `form-action 'self'` | 문서 form이 제출될 목적지를 같은 origin으로 제한합니다. |
| `frame-ancestors 'none'` | 다른 문서가 현재 페이지를 frame으로 포함하지 못하게 합니다. 외부 embedding이 필요한 서비스는 실제 신뢰 origin으로 제한합니다. 이 지시자는 HTTP 응답 헤더로 보내야 하며 `<meta>`에 넣으면 적용되지 않습니다. |

Report-Only 단계에서는 정상 페이지 흐름을 충분히 관찰합니다. 서버로 전송되는 위반 보고에는 URL, 리소스 주소, 브라우저 정보가 포함될 수 있으므로 보고 endpoint 접근·보관·개인정보를 관리합니다. 외부 분석 script, 결제 창, OAuth popup, CDN, inline code를 목록화한 뒤 실제 enforcement 정책을 정하고, 위반 보고가 줄었다고 XSS가 사라진 것으로 해석하지 않습니다. CSP는 출력 인코딩·템플릿 자동 escaping과 함께 쓰는 방어 계층입니다. [MDN CSP 배포 안내](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/CSP)

## HSTS와 HTTPS 전환

HSTS는 HTTPS 응답으로 전달된 정책을 브라우저가 저장해 다음 방문부터 같은 host를 HTTPS로 강제하도록 합니다. HTTP 응답에 실린 HSTS 헤더는 무시됩니다. 따라서 첫 방문부터 HTTP를 막으려면 HSTS preload와 같은 별도 경로를 검토해야 하며, preload는 RFC 6797 자체의 기능과 구별되는 브라우저 목록 운영입니다. [RFC 6797 §5.1–§5.4](https://datatracker.ietf.org/doc/html/rfc6797)

```http
Strict-Transport-Security: max-age=86400
```

`max-age=86400`은 하루 동안 정책을 기억하는 형식을 보여 주는 예시이며, 모든 서비스에 권하는 기간은 아닙니다. 실제 기간은 HTTPS 전환 범위와 하위 도메인 구성을 확인해 정합니다. `includeSubDomains`는 하위 도메인도 HTTPS로만 동작하도록 브라우저에 알립니다. 운영 중인 하위 도메인 전체, 구형 장비, 외부 SaaS, 인증·메일·개발·테스트 도메인이 HTTPS를 지원하는지 확인한 뒤 적용합니다. `preload`는 제출·목록 반영·제거에도 시간이 걸릴 수 있으므로 구성된 모든 하위 도메인이 지속적으로 HTTPS를 제공할 수 있는 경우에만 검토합니다. HSTS 정책의 저장 기간을 늘리면 잘못된 설정을 되돌리기 어려워집니다. [OWASP Secure Headers Project](https://secure-headers-project.owasp.org/best-practices/) · [MDN HSTS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security)

## 교차 출처 격리 정책은 목적에 맞게 적용합니다

`Cross-Origin-Opener-Policy`(COOP)는 최상위 browsing context가 다른 출처의 창과 연결되는 관계를 제한합니다. `Cross-Origin-Embedder-Policy`(COEP)는 문서가 cross-origin 리소스를 embed하는 조건을 정합니다. 일부 고급 웹 기능에서 cross-origin isolation이 필요할 수 있지만, COOP/COEP를 켜면 외부 이미지, font, iframe, OAuth popup, 결제·로그인 창이 차단되거나 동작이 바뀔 수 있습니다. 해당 기능이 필요한 페이지와 외부 리소스 제공자가 CORS 또는 CORP로 동의하는지 확인한 뒤 적용합니다. COEP는 인증·인가나 CSP를 대체하는 범용 공격 차단 헤더가 아닙니다. [MDN COOP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy) · [MDN COEP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy)

## 배포 전후 점검

1. 페이지별로 필요한 외부 script·API·image·font·iframe·form·popup을 기록합니다.
2. CORS에서는 요청 origin, credentials, method, custom header, cache key를 별도로 검토합니다. 허용할 origin이 없으면 CORS 응답을 추가하지 않습니다.
3. CSP는 Report-Only로 정상 페이지 흐름을 관찰하고, 동적으로 생성하는 nonce가 응답마다 새로 생기는지 확인한 뒤 enforcement 정책으로 전환합니다.
4. HSTS는 인증서, HTTPS redirect, 하위 도메인 의존성을 확인하고 우선 제한된 기간으로 운영한 뒤 단계적으로 늘립니다. 하위 도메인 전체를 점검하기 전 `includeSubDomains`를 적용하지 않습니다.
5. clickjacking 방어가 필요한 페이지에 `frame-ancestors`를 지정하고, 의도된 embedding flow와 OAuth popup 동작을 회귀 확인합니다.
6. `nosniff`를 켜기 전에 서버와 CDN이 CSS·JavaScript·다운로드 파일에 정확한 `Content-Type`을 보내는지 확인합니다.
7. 자동 header scanner가 값의 존재만 확인하는지, CSP와 CORS의 실제 의미도 검증하는지 구분합니다. 보안 헤더가 보인다는 결과만으로 서비스가 안전하다고 판단하지 않습니다.

| 시험 | 관찰할 결과 | 통과 기준 |
| --- | --- | --- |
| 허용 origin에서 API 응답 조회 | 브라우저 console/network와 서버의 권한 로그 | 로그인·권한 검사가 정상 작동하고 필요한 응답만 허용 origin에 공유됩니다. |
| 허용되지 않은 origin | response headers와 browser JavaScript가 읽을 수 있는지 | 서버 인증은 유지되며 browser script에는 응답이 공유되지 않습니다. |
| credential 요청 | wildcard, `Access-Control-Allow-Credentials`, cookie 정책 | 자격 증명이 필요한 origin만 명시적으로 허용됩니다. |
| CSP Report-Only | 위반 보고와 정상 리소스 목록 | 외부 리소스와 popup이 확인되고 보고 값에 민감 정보가 과도하게 포함되지 않습니다. |
| HSTS와 하위 도메인 | HTTPS redirect, 인증서, 하위 서비스 연결 | 의도한 host 전체가 HTTPS로 접속 가능하고 업무 흐름이 유지됩니다. |
| iframe·popup | frame 거부 여부와 로그인·결제 window 연결 | 정책상 막을 frame은 차단하고 명시적으로 필요한 popup 흐름은 작동합니다. |

이 시험표는 배포 전 점검 기준이며 이 문서 작성 과정에서 실제 사이트나 브라우저에 실행하지 않았습니다. 서비스별 CSP·CORS 허용 목록은 코드 리뷰, 구성 검증, 승인된 브라우저 회귀 테스트를 함께 기록합니다.

## 앞 장과의 연결

[웹과 API의 입출력](05-웹과API의입출력_web-api.md)은 XSS·CSRF와 브라우저 출력 경계를 소개합니다. 이 장은 브라우저가 응답 헤더를 어떻게 처리하는지 더 자세히 구분합니다. CORS는 로그인·API 권한 검사를 대체하지 않고, CSP는 안전한 템플릿 렌더링을 대신하지 않으며, HSTS는 서버 인증서를 올바르게 구성하는 일을 대신하지 않습니다.

## English summary

Browser response policies solve different problems. CSP controls resource loading and script execution; CORS controls whether browser scripts may read cross-origin responses; HSTS remembers HTTPS-only access; and COOP/COEP support specific cross-origin isolation requirements. None replaces server authentication, authorization, CSRF defenses, or output encoding. Roll policies out through inventory, report-only observation where available, and authorized browser regression tests. The header examples are templates, not tested production settings.

## 출처와 확인 범위

- [Content Security Policy Level 3](https://www.w3.org/TR/CSP3/), W3C Working Draft, 2026년 10월 27일. CSP 지시자와 정책 처리 구조를 대조했습니다. Working Draft임을 유지하고 최종 W3C Recommendation과 혼동하지 않았습니다.
- [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html), OWASP 공식 지침, 2026년 11월 4일 확인. nonce·hash 기반 strict CSP와 `strict-dynamic` 사용 시 주의점을 확인했습니다.
- [Fetch Standard §3.3: CORS protocol](https://fetch.spec.whatwg.org/#cors-protocol), WHATWG Living Standard, 2026년 10월 19일 갱신판을 2026년 11월 4일 확인. preflight·origin response-sharing·credentials 요구를 확인했습니다.
- [RFC 6797: HTTP Strict Transport Security](https://datatracker.ietf.org/doc/html/rfc6797), IETF Standards Track, 2012년 11월. HTTPS 응답에 의한 HSTS 저장과 하위 도메인 처리 §5·§6을 확인했습니다.
- [OWASP Secure Headers Project: Best Practices](https://secure-headers-project.owasp.org/best-practices/) 및 [Response Headers](https://secure-headers-project.owasp.org/response-headers/), OWASP 공식 프로젝트 자료, 2026년 11월 4일 확인. CSP·HSTS·frame 제한·`nosniff`·Referrer-Policy의 역할을 대조했습니다. 제안 예시는 서비스 요구 검토 없이 그대로 적용하지 않습니다.
- [MDN: CSP implementation guide](https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/CSP), 2026년 11월 4일 확인. Report-Only 관찰, nonce/hash 선택과 script 의존성 점검을 확인했습니다.
- [MDN: Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) 및 [CSRF](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/CSRF), 2026년 11월 4일 확인. form형 요청, credential CORS, preflight와 CSRF의 경계를 대조했습니다.
- [MDN: HSTS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security) 및 [Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy), 2026년 11월 4일 확인. 하위 도메인 정책, 최초 방문 한계와 referrer 정보 범위를 확인했습니다.
- [MDN: COOP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy) 및 [COEP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy), 2026년 11월 4일 확인. opener 분리, cross-origin embedding 허용과 cross-origin isolation 조건을 확인했습니다.
- [W3C Permissions Policy](https://www.w3.org/TR/permissions-policy-1/), W3C Working Draft, 2026년 10월 26일. 문서와 iframe에서 브라우저 기능 사용을 제한하는 표준의 현재 판본을 확인했습니다.

헤더 예시는 설명을 위해 구성한 템플릿이며 사이트에 배포하거나 실행하지 않았습니다. CSP·HSTS·COOP/COEP의 실제 영향은 해당 사이트의 resource, origin, subdomain, popup 구성에 따라 시험해야 합니다.
