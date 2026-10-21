# 이더넷 프레임의 길이와 UDP 경계 / Ethernet, IPv4, and UDP length boundaries

패킷의 바이트 수를 하나의 길이로 취급하면 padding을 payload에 넣거나, 잘린 입력을 정상 데이터처럼 읽을 수 있습니다. 이 사례는 합성 캡처의 Ethernet·IPv4·UDP 경계를 각각 확인하고, 별도로 실제 localhost UDP 소켓의 datagram 경계를 관측합니다. NIC·PHY·케이블·Ethernet FCS·원시 프레임 송신은 시험하지 않았습니다.

[코드·입력·실행 안내](../예제_examples/실무검증_practical-validation/uart_ethernet/README.md) · [실행 기록](검증기록_evidence/UART와UDP수신경계검증_20261021.md)

## 1. 파싱할 프레임의 범위

`parse_udp_capture()`는 FCS가 제거된 untagged EthernetII 안의 IPv4·IHL 5·비단편 UDP만 해석하는 교육용 함수입니다. 주소 수신 대상·TTL 유효성·모든 MAC 규칙을 확인하는 네트워크 스택은 아닙니다. IP options·VLAN·IPv6·TCP·fragment 재조립·UDP Options는 지원하지 않으며 각각 미지원 상태로 구분합니다.

아래 필드는 RFC 791 §3.1·AppendixB와 RFC 768의 형식을 확인해 구성했습니다. IHL은 IPv4 헤더의 32비트 단어 수이므로 5는 20바이트입니다. IP total length는 IP 헤더를 포함하고 UDP length는 UDP 헤더 8바이트를 포함합니다. 다중 바이트 정수는 상위 바이트를 먼저 읽습니다. [RFC 791](https://www.rfc-editor.org/rfc/rfc791.html), [RFC 768](https://www.rfc-editor.org/rfc/rfc768.html)

| 기본 fixture | 값·직접 확인할 계산 |
| --- | --- |
| Ethernet header | 목적지 6+출발지 6+EtherType2=14바이트입니다. EtherType은 0800입니다. |
| IPv4 | `45`·total0020·DF4000·protocol17·header checksum 3C62입니다. |
| 주소 | 문서 예시 192.0.2.1→198.51.100.2입니다. 실제 송신 주소가 아닙니다. |
| UDP header | `12 34 AB CD 00 0C D1 16`입니다. |
| UDP ports |1234 hex=4660, ABCDhex=43981입니다. 1234를 little endian으로 읽으면 13330입니다. |
| 사용자 데이터 | `41 42 43 44`=ABCD, 4바이트입니다. |

## 2. padding을 데이터로 읽는 오류

IP는 `20+8+4=32`바이트입니다. 이 예의 Ethernet data field는 최소 46바이트를 맞추기 위해 14바이트를 더 붙였습니다. FCS를 제외한 합성 캡처는 `14+32+14=60`바이트입니다. IP total length32에는 Ethernet padding 14가 들어가지 않습니다. [RFC 894 Frame Format](https://www.rfc-editor.org/rfc/rfc894.html)

잘못된 `frame[42:]`는 UDP payload 시작부터 캡처 끝까지 읽어 ABCD 뒤 0을 14개 더 붙입니다. 수정 경로는 먼저 `packet=frame[14:]`, 다음 `udp=packet[20:total]`로 IP 경계를 자르고 마지막으로 UDP header를 제외합니다. 단, 고정 20바이트를 쓰기 전에 IHL 5를 확인해야 합니다. IHL 6을 지원하면서 같은 offset을 사용하면 options를 UDP header로 오인합니다.

| 구분 | 기본 입력의 값 | 경계가 뜻하는 것 |
| --- | --- | --- |
| 캡처 길이 |60 | 전달받은 bytes의 실제 길이입니다. |
| IP 끝 |Ethernet 시작에서 46 |14+IP total32입니다. |
| UDP 길이 |12 |UDP header8+payload 4입니다. |
| 응용 데이터 길이 |4 |`udp_length-8`입니다. |

기본 60바이트 입력을 0~60바이트로 잘라 61경계를 검사했습니다. 46바이트부터는 IP·UDP 해석에 필요한 데이터가 모두 있으므로 ACCEPT입니다. 이는 padding의 일부가 캡처에서 잘려도 IP payload를 해석할 수 있다는 뜻입니다. 완전한 Ethernet 프레임의 최소 길이·FCS 적합성을 판정한 결과가 아닙니다. 함수는 캡처 뒤쪽 바이트를 padding으로 보고하지만 MAC 수신기의 모든 검사를 대신하지 않습니다.

## 3. 길이·미지원·손상을 나누는 순서

바이트를 참조하기 전에 필요한 최소 길이를 확인합니다. 이 순서는 짧은 입력에서 엉뚱한 값이나 인덱스 오류가 나오는 일을 막습니다.

```python
total = int.from_bytes(packet[2:4], 'big')  # 슬라이스2:4의 두 바이트를 상위 바이트부터 정수로 읽습니다.
if total < 28:  # if는 조건문이며 이 모델의 IP20+UDP8보다 짧은지 봅니다.
    raise PacketError('IP_LENGTH')  # raise는 패킷을 수락하지 않는 이유를 예외로 보냅니다.
if total > len(packet):  # len은 실제로 캡처된 IP 쪽 바이트 수입니다.
    raise PacketError('IP_TRUNCATED')  # 선언한 길이만큼 캡처가 없으면 중단합니다.
udp = packet[20:total]  # 끝 total은 포함하지 않아 Ethernet padding을 제외합니다.
udp_length = int.from_bytes(udp[4:6], 'big')  # UDP header의 길이 필드를 읽습니다.
if udp_length < 8:  # UDP header 자체보다 작은 길이는 거부합니다.
    raise PacketError('UDP_LENGTH')  # 오류 이름을 결과 JSON에 남깁니다.
if udp_length > len(udp):  # IP 경계 안의 바이트보다 UDP가 길다고 선언했는지 봅니다.
    raise PacketError('UDP_TRUNCATED')  # IP 뒤 padding으로 부족분을 채우지 않습니다.
if udp_length < len(udp):  # UDP 끝 뒤에도 IP payload가 남는 경우입니다.
    raise PacketError('UNSUPPORTED_UDP_SURPLUS')  # 옵션 미지원과 잘못된 길이를 구분합니다.
```

UDP length가 IP payload보다 작다고 보편적인 malformed로 단정하면 안 됩니다. RFC 9868, 2025-10은 그 차이의 surplus area에 UDP Options를 정의하며 RFC 768을 갱신했습니다. 이 좁은 예제는 해당 영역을 처리하지 않으므로 `UNSUPPORTED_UDP_SURPLUS`를 반환합니다. 예제의 거부를 표준이 모든 수신기에 요구하는 폐기 정책이라고 해석하지 않습니다. [RFC 9868 §3·7·21](https://www.rfc-editor.org/rfc/rfc9868.html)

단편에서도 offset0만 확인하면 부족합니다. 첫 조각은 offset0이어도 MF가 1일 수 있습니다. `flags_offset & 0x3FFF`는 MF와 offset을 함께 살피며, 재조립을 구현하지 않은 이 함수는 둘 중 하나라도 있으면 `UNSUPPORTED_FRAGMENT`입니다. DF만 설정한 기본 패킷은 통과합니다.

## 4. 두 체크섬이 보호하는 범위

IPv4 header checksum은 헤더만 검사합니다. UDP checksum은 UDP header·payload에 출발지/목적지 IP·0·protocol17·UDP length로 만든 pseudoheader를 더해 검사합니다. Pseudoheader는 UDP 앞에 실제로 붙여 송신하는 별도 헤더가 아니라 계산용 정보입니다. [RFC 791 §3.1](https://www.rfc-editor.org/rfc/rfc791.html), [RFC 768 Fields](https://www.rfc-editor.org/rfc/rfc768.html)

Internet checksum은 16비트 단어를 더하고 넘친 carry를 아래 16비트에 더한 뒤 반전합니다. 홀수 길이면 계산용 0을 마지막에 붙입니다. `0001 F203 F4F5 F6F7`의 합은 `0x2DDF0`, 접으면 `DDF2`, 반전하면 `220D`입니다. 홀수 입력 `00 01 F2`는 `0001+F200=F201`이므로 결과 0DFE입니다. 두 리터럴을 함수 결과와 비교합니다. [RFC 1071 §1](https://www.rfc-editor.org/rfc/rfc1071.html)

IPv4 UDP의 checksum 필드 0은 checksum 생략입니다. 기본 정책은 수락하되 `omitted_ipv4`로 기록하고, 비 0을 실제 검사했을 때만 `checked`로 표시합니다. 별도 `allow_zero_udp=False`에서는 `UDP_CHECKSUM_REQUIRED`로 거부합니다. 이는 응용 정책이며 IPv6 전체에 그대로 적용하는 규칙이 아닙니다.

| 고정 입력 변경 | 기대·관측 | 분리한 원인 |
| --- | --- | --- |
| UDP length7 |UDP_LENGTH |헤더보다 짧은 길이입니다. |
| UDP length13, IP 안에는 12바이트 |UDP_TRUNCATED |Ethernet padding이 있어도 부족합니다. |
| UDP length11, IP 안에는 12바이트 |UNSUPPORTED_UDP_SURPLUS |옵션 해석은 범위 밖입니다. |
| ABCD를ABCE로 바꾸고 checksum 유지 |UDP_CHECKSUM |IP header 검사는 통과해도 데이터가 손상됐습니다. |
| 목적지 IP만 바꾸고 IP checksum은 다시 계산 |UDP_CHECKSUM |UDP pseudoheader와 맞지 않습니다. |
| IP TTL을 바꾸고 header checksum 유지 |IP_CHECKSUM |상위 UDP 이전에 거부합니다. |

22개 리터럴 캡처에는 정상 4개와 거부·미지원 18개가 있습니다. 비 0 UDP 검사를 생략하는 변이는 손상ABCE를 ACCEPT하므로 고정 기대값과 달라 종료 1입니다. checksum 알고리즘의 자기 일치만으로 정답을 정하지 않습니다.

## 5. 실제 localhost UDP에서 관측한 경계

AF_INET·SOCK_DGRAM 소켓을 127.0.0.1의 임시 포트에 bind한 뒤 별도 송신 소켓에서 4바이트ABCD, 빈 datagram, 7바이트UART 프레임을 순서대로 보냈습니다. 각 전송 직후 65535바이트 수신 버퍼로 `recvfrom()`을 호출했습니다. 세 번의 결과가 각각 4·0·7바이트이며 리터럴 payload와 같았습니다. Python의 `with`는 종료 시 소켓을 닫고, 2초 timeout의 실패를 성공으로 바꾸지 않습니다. [Python socket: bind·sendto·recvfrom·settimeout](https://docs.python.org/3.12/library/socket.html)

빈 UDP datagram의 `b''`는 수신된 0바이트 메시지입니다. TCP stream의 EOF 해석을 가져오면 안 됩니다. 이 시험은 localhost의 작은 세 datagram에서 경계를 확인한 것입니다. 손실·중복·순서 변경·원격 경로·작은 수신 버퍼의 잘림·처리량은 시험하지 않았으며 UDP의 일반적인 전달 보장을 주장하지 않습니다. 합성 Ethernet 캡처는 전송하지 않았고, 실제 UDP의 IP header는 운영체제가 만들었습니다.

## 확인 문제

1. 캡처가 60바이트인데 UDP payload가 18바이트인가요? 아닙니다. 이 입력은 4바이트이고 나머지 14바이트는 Ethernet padding입니다.
2. IP checksum을 다시 계산하면 목적지 주소 변경을 숨길 수 있나요? UDP checksum은 pseudoheader도 검사하므로 이 fixture에서는 UDP_CHECKSUM으로 검출합니다.
3. checksum 0을 수락하면 검사에 성공한 것인가요? 아닙니다. IPv4에서 생략한 상태로 표시하며 엄격 정책에서는 거부합니다.

## English

A bounded parser separates captured bytes, IPv4 total length, UDP length, and Ethernet padding. It supports only FCS-stripped untagged EthernetII carrying IHL 5 unfragmented IPv4/UDP. Unsupported options or fragments are reported separately from malformed lengths. Literal vectors cover header and pseudoheader checksums, IPv4 checksum omission, 22 captures, and 61 prefix boundaries. A separate real localhost UDP test observes 4-, 0-, and 7-byte datagrams; the synthetic raw frames are never transmitted.

## 읽은 자료와 판본

2026-10-21에 RFC 768(1980-08)의 Format·Fields·User Interface, RFC 791(1981-09) §3.1·AppendixB, RFC 1071(1988-09) §1, RFC 894(1984-04)의 Frame Format·Byte Order를 확인했습니다. RFC 894의 1500바이트를 minimum으로 쓴 원문 오기는 verified errata 5141·570의 maximum 정정과 대조했습니다. [RFC 894 원문](https://www.rfc-editor.org/rfc/rfc894.html), [정정 표시본](https://www.rfc-editor.org/rfc/inline-errata/rfc894.html)

RFC 9868(2025-10)은 §3·7·21과 surplus area의 정의를 확인했습니다. Python 문서는 3.12계열, 열람 화면은 3.12.15이며 실행 환경은 3.12.14입니다. 논리 바이트·길이·checksum의 계산은 자체 입력에 대한 결과이며 공식 장치 성능 자료가 아닙니다.
