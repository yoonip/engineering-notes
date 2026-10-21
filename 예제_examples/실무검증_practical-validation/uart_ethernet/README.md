# UART 수신 조각과 UDP 길이 검사 / UART chunks and UDP length checks

Python 표준 라이브러리로 실행하는 두 호스트 모델과 별도의 실제 localhost UDP 시험입니다. UART·NIC·PHY·케이블·FCS·원시 Ethernet 송신은 실행하지 않습니다.

| 파일 | 내용 |
| --- | --- |
| [models.py](models.py) | 자체 UART 프레임 파서·Internet checksum·일부 Ethernet/IPv4/UDP 캡처 해석입니다. |
| [fixtures.json](fixtures.json) | 프레임·22개 합성 캡처·직접 적은 출력과 오류 이름·checksum 기대값입니다. |
| [run_cases.py](run_cases.py) | 정상/오류/분할/경계 검사·localhost 전송·JSON과 환경/해시 기록입니다. |

[UART 사례](../../../설계와검증사례_engineering-cases/UART의분할수신과재동기화_uart-stream-resync.md) · [Ethernet·UDP 사례](../../../설계와검증사례_engineering-cases/이더넷프레임의길이와UDP경계_ethernet-ipv4-udp.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/UART와UDP수신경계검증_20261021.md)

## 실행

Python 3.12의 표준 라이브러리만 사용합니다. 이 폴더에서 실행하고 결과에는 매번 새 폴더를 지정합니다. 아래 C:/temp 경로는 독자가 선택할 새 경로의 예입니다.

```powershell
python -B run_cases.py --output C:/temp/uart-udp-new
python -B -O run_cases.py --output C:/temp/uart-udp-optimized-new
python -B -O run_cases.py --mutation uart-ignore-checksum --output C:/temp/uart-mutation-new
python -B -O run_cases.py --mutation udp-ignore-checksum --output C:/temp/udp-mutation-new
```

정상은 PASS·종료 0, 의도적 변이는 ERROR·종료 1입니다. 이미 있는 결과 폴더는 종료 2로 거부합니다. `results.json`에는 입력/소스 SHA-256·Python·OS·시각·명령 인수·관측값이 들어갑니다. 소켓 실패도 예외와 ERROR로 기록합니다. 실행 시각과 임시 포트는 실행마다 달라질 수 있습니다.

## UART 계약

자체 형식 `A5 5A LEN SEQ DATA SUM8`에서 LEN은 0~8, SUM8은 LEN부터 DATA까지의 합의 하위 8비트입니다. 기존 저장소의 escape·CRC 프레임과 다른 형식이며 SUM8을 CRC로 부르지 않습니다. `feed(bytes)`는 같은 객체의 상태를 이어 사용합니다. `expire_partial()`은 호출자가 정한 만료 사건이며 실제 시간 측정이 아닙니다. SEQ 중복·신선도·순번 검사는 구현하지 않습니다.

19바이트의 3프레임을 20가지 조각으로 입력해 리터럴 결과와 비교합니다. 잘못된 길이·checksum 뒤의 복구, 미완성 후보의 명시적 만료, 단순 합 충돌, 100,000바이트 잡음 뒤 내부 버퍼 최고 13바이트를 검사합니다. 반환 목록과 외부 큐 용량은 별도입니다.

`uart-ignore-checksum`은 손상 후보도 수락하는 구현 변이입니다. 검증기는 정상 fixture의 기대값을 그대로 두고 이 차이를 검출합니다.

## Ethernet/IPv4/UDP 계약

FCS 없는 untagged EthernetII·EtherType0800·IPv4 IHL 5·비단편 UDP만 지원합니다. capture length→IP total length→UDP length를 순서대로 확인하고 Ethernet padding을 payload에서 제외합니다. IPv4 UDP checksum 0은 `omitted_ipv4`, 비 0을 검사한 경우는 `checked`입니다. `allow_zero_udp=False`는 별도 엄격 정책입니다.

미지원 VLAN/EtherType·IP options·fragment·protocol·UDP surplus와 잘못된 길이/손상을 구분합니다. RFC 9868의 UDP Options를 해석하지 않으므로 IP payload가 UDP length보다 긴 경우 `UNSUPPORTED_UDP_SURPLUS`입니다. 이는 모든 UDP에서 그 길이 관계가 잘못되었다는 뜻이 아닙니다.

기본 캡처는 60바이트, IP 32바이트, UDP 12바이트, payload 4바이트, padding 14바이트입니다. 0~60바이트의 61개 prefix는 46바이트부터 IP/UDP 해석에 충분합니다. 완전한 MAC 최소 길이·FCS 검사 결과는 아닙니다. `udp-ignore-checksum`은 비 0 UDP checksum 검사를 생략하는 변이이며, 손상 payload fixture를 수락해 검증기가 실패합니다.

## 실제 소켓과 합성 캡처의 차이

`loopback_udp()`는 127.0.0.1의 임시 포트에서 4·0·7바이트 datagram을 실제 송수신하고 정확한 bytes를 비교합니다. 합성 Ethernet/IP fixture는 소켓으로 보내지 않습니다. OS가 실제 UDP 헤더를 만들며, 실행 결과에는 endpoint와 `raw_ethernet_fixture_transmitted=false`를 남깁니다. 원격 전달·손실·성능·작은 수신 버퍼의 잘림은 시험하지 않습니다.

## 코드에서 쓰는 문법

| 문법·함수 | 이 코드에서의 뜻 |
| --- | --- |
| import / from ... import | socket·json 등의 표준 기능이나 같은 폴더의 모델 이름을 가져옵니다. |
| def / class / self | 함수·객체 형을 정의하고 각 파서의 상태를 구별합니다. |
| bytes / bytearray | 변경할 수 없는 입력 바이트열·변경할 수 있는 내부 버퍼입니다. |
| [] / {} / () | 리스트나 위치 접근·딕셔너리·함수 호출이나 tuple에 사용합니다. |
| [a:b] / [-1] | a부터b직전까지 자르는 슬라이스·마지막 원소입니다. |
| & / << / >> / ~ | 비트 마스크·이동·반전이며 길이/flags/checksum에 사용합니다. |
| if not / != | 조건 부정·다름 비교이며 입력과 예상 결과를 검사합니다. |
| try / except / raise | 입력 오류·패킷 거부·검증 실패를 예외로 구분합니다. |
| with | 블록이 끝나면 소켓을 닫습니다. |
| int.from_bytes(...,'big') | 상위 바이트부터 수를 만듭니다. 1234hex는 4660입니다. |
| require / -O | 명시적 예외 검사이므로 최적화로 assert가 제거되어도 검사가 남습니다. |

## Sources

[pySerial 3.5 read](https://pyserial.readthedocs.io/en/latest/pyserial_api.html#serial.Serial.read), [RFC 791 §3.1·AppendixB](https://www.rfc-editor.org/rfc/rfc791.html), [RFC 768](https://www.rfc-editor.org/rfc/rfc768.html), [RFC 1071 §1](https://www.rfc-editor.org/rfc/rfc1071.html), [RFC 894 Frame Format](https://www.rfc-editor.org/rfc/rfc894.html), [RFC 9868 §3·7·21](https://www.rfc-editor.org/rfc/rfc9868.html), [Python 3.12 socket](https://docs.python.org/3.12/library/socket.html)를 2026-10-21에 열람했습니다. 판본·읽은 범위와 구현하지 않은 기능은 두 사례 본문에 기록했습니다.

## English

Deterministic byte models cover persistent UART parsing and limited Ethernet/IPv4/UDP capture validation. Independent literal expectations, explicit exceptions under optimization, two intentional mutations, and output-directory protection are included. A separate real localhost UDP test observes three small datagrams; it does not send the synthetic raw captures or validate physical links.
