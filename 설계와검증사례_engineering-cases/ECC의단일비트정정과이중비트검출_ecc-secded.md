# ECC의 단일 비트 정정과 이중 비트 검출 | SECDED correction, detection and limits

## 자료가 같아도 정정 기록은 다릅니다

ECC는 error-correcting code, 오류를 알아내거나 제한된 범위에서 바로잡도록 여분의 비트를 붙이는 부호입니다. SECDED는 single-error correction, double-error detection의 약자로 코드워드 안의 한 비트 오류는 정정하고 두 비트 오류는 검출하는 계약입니다. 자료가 기대값과 같다는 사실과 오류가 발생하지 않았다는 사실을 구분해야 합니다.

이 사례의 [Python 코드](../예제_examples/실무검증_practical-validation/ecc_secded/README.md)는 8비트 자료·Hamming parity 4비트·전체 parity 1비트의 고정 `(13,8)` 부호를 실행합니다. 실제 메모리나 vendor ECC의 결과를 옮긴 것이 아닙니다. [Hamming의 1950년 원 논문 §3~5](https://zoo.cs.yale.edu/classes/cs323/doc/Hamming.pdf)의 선택 위치 검사·전체 parity·코드 거리 원리를 참고해 작은 학습 코드를 구성했습니다.

## 비트 번호와 검사 행렬을 고정합니다

코드워드는 자료와 검사 비트를 합친 13비트입니다. 위치1을 Python 정수의 가장 낮은 bit0, 위치13을 bit12로 셉니다. 자료 bit0~7은 아래 순서로 배치합니다.

| 위치 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 역할 | p1 | p2 | d0 | p4 | d1 | d2 | d3 | p8 | d4 | d5 | d6 | d7 | 전체 p |

parity는 선택한 비트들에서 1의 개수가 짝수인지 확인하는 규칙입니다. 각 검사 집합에 자기 parity 위치를 포함합니다.

| 검사 행 | 포함한 위치 |
| --- | --- |
| p1 | 1,3,5,7,9,11입니다. |
| p2 | 2,3,6,7,10,11입니다. |
| p4 | 4,5,6,7,12입니다. |
| p8 | 8,9,10,11,12입니다. |
| 전체 p | 1~13 전부입니다. |

이 표를 행렬로 쓰면 포함한 위치는 1, 나머지는 0입니다. 앞 네 행의 열은 해당 위치 번호의 이진 표현이고 위치13의 앞 네 값은 0입니다. 마지막 행은 전부 1입니다. 비트를 더할 때 `1+1=0`으로 계산하는 이진 연산에서는 각 행의 합이 0이어야 유효한 코드워드입니다. 복잡한 행렬식보다는 각 행에 든 비트를 XOR한다고 읽으시면 됩니다. XOR는 두 값이 다르면 1, 같으면 0인 비트 연산입니다.

자료 1은 d0인 위치3만 켭니다. p1·p2가 각각 1이어야 앞 네 검사가 짝수가 되므로 위치1·2·3이 켜집니다. 세 개의 1은 홀수여서 위치13도 켜고 최종 코드워드는 `0x1007`입니다. 자료 A5의 코드워드는 `0x0A27`, FF는 `0x0F77`입니다. 4자리 16진수 표시는 표시용 0 비트를 포함하며 실제 유효 폭은 13비트입니다.

## syndrome과 전체 parity를 함께 분기합니다

syndrome은 각 검사에서 어느 조건이 어긋났는지를 모은 값입니다. 앞 네 행의 결과를 낮은 비트부터 붙이면 0~15의 정수가 됩니다. 단일 오류가 위치5에 생기면 p1·p4 검사가 실패하므로 `1+4=5`가 됩니다. 구현에서는 켜진 비트들의 위치 번호를 모두 XOR해 같은 값을 구합니다.

| syndrome | 전체 1 개수 | 복호기의 선택 |
| --- | --- | --- |
| 0 | 짝수 | 검사상 clean으로 자료를 반환합니다. |
| 0 | 홀수 | 위치13을 반전하고 corrected로 반환합니다. |
| 1~12 | 홀수 | syndrome 위치를 반전하고 corrected로 반환합니다. |
| 1~15 | 짝수, 단 0 제외 | uncorrectable로 자료 전달을 차단합니다. |
| 13~15 | 홀수 | 존재하지 않는 정정 위치이므로 차단합니다. |

이 표의 오류 개수 해석은 SECDED의 보장 범위인 최대 두 비트 오류를 전제로 합니다. 세 비트 이상에서는 같은 관측이 다른 원인으로 나올 수 있습니다.

```python
overall_bad = bool(word.bit_count() & 1)  # bit_count는 1의 수, & 1은 홀수 여부, bool은 참·거짓으로 바꿉니다.
position = syndrome if syndrome else 13   # 조건 표현식이며 syndrome이 0이면 전체 parity 위치를 고릅니다.
corrected = word ^ (1 << (position-1))    # <<로 반전 마스크를 만들고 ^로 그 비트만 뒤집습니다.
```

A5의 정상 코드워드 `0x0A27`에서 위치13만 바꾸면 `0x1A27`입니다. 앞 네 검사는 여전히 맞아 syndrome=0이지만 전체 parity가 홀수입니다. 이를 이중 오류로 거절하면 정정 가능한 단일 parity 오류를 놓칩니다. 반대로 syndrome이 0이 아니라고 항상 고치면 이중 오류를 잘못 정정합니다. 예를 들어 0에서 위치1·2를 바꾸면 syndrome=3·전체 짝수이므로 위치3을 뒤집어서는 안 됩니다.

`uncorrectable`의 data·corrected_word는 모두 `None`으로 반환합니다. 자료 부분이 우연히 원래와 같아 보여도 정상값으로 전달하지 않는 API 계약입니다. 상태 필드 없이 값만 꺼내는 호출자는 이 차이를 잃습니다. `corrected_word`는 계산한 결과이며 실제 저장 셀을 다시 쓴 결과가 아닙니다.

## 구현과 다른 방법으로 정답을 만듭니다

부호화 구현은 위치별 parity 집합을 계산합니다. 검증기는 같은 함수를 정답으로 부르지 않고 자료 bit 하나씩에 대응하는 고정 generator 기저 `1007,1019,102A,004B,1181,1282,0483,1888`을 XOR해 256개 코드워드를 만듭니다. 각 기저는 해당 자료 bit만 1인 코드워드입니다. 수작업 부호화 리터럴 5개도 대조합니다.

서로 다른 코드워드가 다른 비트의 개수를 Hamming 거리라고 합니다. 예를 들어 `0000`과 `1007`의 차이는 네 비트입니다. 코드북의 서로 다른 모든 쌍 32,640개를 계산한 최소 거리는 4였습니다. 따라서 한 코드워드에서 한 비트만 바꾼 영역은 다른 코드워드의 한 비트 영역과 겹치지 않습니다.

독립 기준은 코드워드 자신과 단일 비트 이웃을 열거합니다. 그 안에 있으면 유일한 해당 자료를 선택하고, 그 밖이면 정정 대상으로 선택하지 않습니다. 정상 256개와 이웃 `256×13=3,328`개를 합한 3,584개가 이 반경1 영역입니다. 나머지 4,608개 입력은 선택하지 않습니다. 모든 13비트 입력 8,192개를 이 기준과 비교했습니다.

이 전체 입력 비교는 복호기가 정한 선택 정책과 일치한다는 뜻입니다. 여러 비트가 바뀐 자료에서 최초 원본까지 알아낸다는 뜻은 아닙니다. 원본별 단일 3,328조합·이중 `256×C(13,2)=19,968`조합은 보장 범위도 따로 확인합니다. 이 수와 프로그램의 32,035비교 수는 같은 입력을 다른 관점에서 중복 검사하므로 독립 시험 수로 합산하지 않습니다.

## 세 비트 오정정과 네 비트 미검출을 직접 확인합니다

| 원래 자료0에서 뒤집은 위치 | 수신 코드 | 관측 | 실제 원본과 비교 |
| --- | --- | --- | --- |
| 1,2,3 | 0007 | syndrome0·전체 홀수로 위치13을 정정합니다. | 자료1이 되어 잘못 복구합니다. |
| 1,2,4 | 000B | syndrome7·전체 홀수로 위치7을 정정합니다. | 자료8이 되어 잘못 복구합니다. |
| 1,2,3,13 | 1007 | 유효 코드워드여서 clean입니다. | 자료1이며 오류를 검출하지 못합니다. |
| 1,4,8 | 0089 | syndrome13·전체 홀수입니다. | 존재하지 않는 위치라 차단합니다. |

첫 수신값 `0007`은 원래 자료1의 `1007`에서 위치13만 바꿔도 나옵니다. 복호기는 같은 수신값만으로 “자료0의 세 비트 오류”와 “자료1의 한 비트 오류”를 구분할 수 없습니다. 원본을 아는 시험 프로그램이 두 경우를 나눠 기록해야 합니다. 이 반례를 감추거나 반례가 있다는 이유로 단일/이중 보장 자체가 실패했다고 쓰지 않습니다. [AMD UG586의 ECC 설명](https://docs.amd.com/r/en-US/ug586_7Series_MIS/Error-Correcting-Code)도 두 비트를 넘는 오류는 검출 여부가 달라질 수 있음을 구분합니다.

## 자료 ECC와 주소·CRC의 보호 범위

이 부호는 13비트만 검사하며 주소·거래 번호는 포함하지 않습니다. 요청한 주소0 대신 주소1의 온전한 코드워드 `1007`이 오면 검사상 clean이고 자료1을 반환합니다. 자료의 내부 일관성과 요청한 위치에서 왔다는 사실은 다른 검사입니다. 실제 시스템이 주소 parity나 별도 보호를 제공하는지는 각 구현을 확인해야 합니다.

CRC도 어떤 바이트를 계산에 넣었는지가 중요합니다. 다음은 주소1의 자료와 CRC가 주소0의 응답으로 잘못 온 계산 예입니다. 자료만으로 만든 CRC는 자기 값과 일치하지만 요청 주소까지 묶으면 이 예의 오배달을 검출합니다.

```python
from zlib import crc32  # from/import로 표준 라이브러리 CRC32 함수를 가져옵니다.
payload = b"\x01"  # b는 bytes이며 이 예의 자료 한 바이트입니다.
requested, actual = 0, 1  # 여러 변수에 요청 주소와 실제 자료 출처를 나누어 저장합니다.
stored_data_crc = crc32(payload)  # 자료만 보호한 체크값입니다.
stored_address_crc = crc32(actual.to_bytes(2, "big") + payload)  # 주소를 2바이트로 바꾸고 +로 자료와 연결합니다.
print(crc32(payload) == stored_data_crc)  # 자료만 비교하면 True입니다.
print(crc32(requested.to_bytes(2, "big") + payload) == stored_address_crc)  # 요청 주소를 묶은 비교는 False입니다.
```

이 CRC 계산도 실제 프로토콜 구현은 아닙니다. 검출 보장은 CRC 다항식·길이·오류 형태와 보호 범위에 달려 있고 충돌 가능성이 있습니다. CRC는 일반적으로 오류를 고치는 복호기가 아니며 [Python zlib 문서](https://docs.python.org/3.12/library/zlib.html#zlib.crc32)도 인증 용도로 쓰지 않도록 구분합니다. 악의적인 변경까지 막으려면 신뢰와 인증의 계약이 별도로 필요합니다.

## 실행과 오류 주입 결과

정상·`-O` 실행은 각각 종료0·32,035비교 PASS였습니다. 아래는 의도적으로 잘못 만든 구현이며 네 가지 모두 두 실행 모드에서 종료1로 검출했습니다.

| 변이 | 첫 관측 | 원인 |
| --- | --- | --- |
| 전체 parity 생성 누락 | 자료1이 1007 대신 0007입니다. | 부호기와 복호기를 단순 왕복만 하면 놓칠 수 있는 부호화 오류입니다. |
| syndrome0·전체 홀수 거절 | 수신0007을 uncorrectable로 처리합니다. | 위치13 단일 오류 분기가 빠졌습니다. |
| 이중 오류까지 정정 | 수신0003에서 위치3을 고쳐 자료1을 반환합니다. | syndrome만 보고 전체 parity 조건을 무시했습니다. |
| 차단 상태에서 자료 노출 | uncorrectable인데 data=0입니다. | 오류 상태를 정상 자료 경로와 분리하지 않았습니다. |

검증기는 첫 실패에서 멈추므로 변이 실행의 비교 수는 정상보다 작습니다. 입력·소스 해시, 분류별 개수와 보장 밖 관측은 [검증 기록](검증기록_evidence/ECC오류주입과검출범위_20261021.md)에 있습니다. [Linux EDAC](https://docs.kernel.org/driver-api/edac.html#c.hw_event_mc_err_type)의 corrected/uncorrected/deferred/fatal 보고와 실제 장치 상태는 이 함수의 세 상태와 별개입니다. 이 코드는 DRAM·NAND의 vendor ECC, BCH·LDPC, chipkill, 물리 오류율이나 보드 신뢰성을 검증하지 않습니다.

## 확인 문제

1. syndrome이 0이면 항상 오류가 없나요? 아닙니다. 전체 parity가 홀수면 단일 오류 전제에서 위치13 오류입니다. 네 비트 반전으로 다른 유효 코드워드가 된 경우도 syndrome0·전체 짝수일 수 있습니다.
2. 이중 오류에서 자료 부분이 기대값과 같으면 써도 되나요? 이 API는 오류 상태에서 자료를 전달하지 않습니다. 검사 결과와 정정 보장 없이 정상 자료처럼 사용하지 않습니다.
3. 모든 수신값 8,192개를 대조했으면 네 비트 오류도 복구하나요? 아닙니다. 정한 반경1 선택 정책과의 일치이며 실제 원본을 추론하는 보장 범위는 별개입니다. 자료0의 네 비트 반전이 자료1의 유효 코드워드와 같다는 반례가 있습니다.

## English

The fixed extended Hamming(13,8) example uses data positions 3,5,6,7,9,10,11,12, Hamming parity positions 1,2,4,8, and overall parity at position13. Position1 is integer bit0. Syndrome zero with odd overall parity selects position13 under the single-error assumption. Uncorrectable results expose neither payload nor corrected codeword.

A literal generator codebook supplies an independent oracle. Its minimum pairwise distance is four. All 8,192 received words match the specified radius-one selection policy; that does not identify the historical original of a multi-bit-corrupted word. Separate injection tests cover all 3,328 single-error and 19,968 double-error origin/position combinations. Counts overlap rather than representing independent physical trials.

Explicit examples show three-bit miscorrection and four-bit undetected corruption. The same received word can arise from different originals and error counts. A valid word delivered from the wrong address also passes this data-only code. CRC coverage, address identity and authentication remain separate contracts.

Normal and optimized runs pass; four deliberate implementation faults fail. The work executes Python functions, not physical memory ECC, vendor BCH/LDPC, EDAC hardware or a reliability qualification.

## 출처

- R. W. Hamming, Error Detecting and Error Correcting Codes, Bell System Technical Journal 29(2), pp. 147–160, April 1950. [출판 정보](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1950.tb00463.x)와 [원 논문 보관본 §3~5](https://zoo.cs.yale.edu/classes/cs323/doc/Hamming.pdf)를 읽었습니다. 13비트 배치·코드·입력은 이 예제에서 구성했습니다.
- Simon Tam, [XAPP645 v2.2, Single Error Correction and Double Error Detection](https://docs.amd.com/api/khub/documents/UXxjwXIsSdz9u~seS8w6cg/content), 2006-08-09, pp.1~3·8~10: parity·syndrome·정정/검출과 오류 주입을 대조했습니다. 해당 FPGA 구현·성능 수치를 재현하지 않았습니다.
- [AMD UG586 v4.2, Error Correcting Code](https://docs.amd.com/r/en-US/ug586_7Series_MIS/Error-Correcting-Code), 2024-11-13: 단일/이중 보장과 그 이상의 한계를 구분했습니다.
- [Linux EDAC 오류 종류](https://docs.kernel.org/driver-api/edac.html#c.hw_event_mc_err_type), [Python3.12 zlib.crc32](https://docs.python.org/3.12/library/zlib.html#zlib.crc32): 상태 보고와 checksum의 보호 범위를 확인했습니다. 확인일은 2026-10-21입니다.
