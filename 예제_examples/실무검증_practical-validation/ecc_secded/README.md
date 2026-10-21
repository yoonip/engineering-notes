# 단일 비트 정정과 이중 비트 검출 | Single-bit correction and double-bit detection

8비트 자료를 13비트 코드워드로 바꾸는 고정 extended Hamming(13,8) 학습 코드입니다. Python 함수에 비트 반전 오류를 주입해 정정·검출과 보장 밖의 반례를 비교합니다. 실제 DRAM·NAND·FPGA ECC나 Linux EDAC 장치를 실행한 결과는 아닙니다.

| 파일 | 역할 |
| --- | --- |
| [codec.py](codec.py) | 위치별 짝수 parity 부호화, syndrome·전체 parity 검사, 정정과 자료 전달 차단입니다. |
| [fixtures.json](fixtures.json) | 비트 번호, generator 기저, 부호화 리터럴 5개, 보장 밖 반례 4개입니다. |
| [verify.py](verify.py) | 독립 코드북·반경1 기준, 전체 자료·단일/이중 오류·전체 입력 검사와 기록입니다. |

## 위치와 반환 계약

정수 bit0을 위치1, bit12를 위치13으로 셉니다. 자료 bit0~7은 차례대로 위치 `3,5,6,7,9,10,11,12`에 둡니다. Hamming parity는 위치 `1,2,4,8`, 전체 parity는 위치13입니다. 모든 parity는 검사 집합의 1 개수를 짝수로 만듭니다. 4자리 16진수 표시는 앞쪽에 사용하지 않는 0 비트를 포함하며 코드워드의 유효 폭은 13비트입니다.

`decode`는 `Decoded` 객체로 status·data·corrected_word·corrected_position·syndrome·overall_bad를 돌려줍니다. `clean`은 검사상 이상 없음, `corrected`는 정정 규칙 적용, `uncorrectable`은 정정 가능한 대상으로 판단하지 않았다는 뜻입니다. 마지막 상태의 `data`와 `corrected_word`는 모두 `None`이므로 정상 자료로 전달하지 않습니다. 세 비트 이상이 바뀌면 `clean`이나 `corrected`가 원본의 정확성을 보장하지 않습니다.

## 실행

Python 3.10 이상 표준 라이브러리만 사용합니다. 이번 실행 환경은 Python 3.12.14·Windows 11입니다. 이 폴더에서 새 출력 경로를 지정합니다.

```powershell
python -X utf8 -B verify.py --out C:/temp/ecc-normal-new
python -X utf8 -B -O verify.py --out C:/temp/ecc-optimized-new
python -X utf8 -B verify.py --mutation omit-overall --out C:/temp/ecc-encode-fault-new
python -X utf8 -B verify.py --mutation reject-overall-bit --out C:/temp/ecc-overall-fault-new
python -X utf8 -B verify.py --mutation correct-double --out C:/temp/ecc-double-fault-new
python -X utf8 -B verify.py --mutation leak-double-data --out C:/temp/ecc-data-fault-new
```

정상 기본·`-O`는 각각 종료0·PASS이며 32,035번 비교합니다. 네 mutation은 두 모드에서 모두 종료1·FAIL입니다. 기존 출력 경로는 종료2로 거절하고 이전 파일을 보존합니다. 판정은 `assert`에 의존하지 않습니다. `input_manifest.json`에는 자료와 오류 위치 조합, `report.json`에는 환경·명령 인수·소스/입력 SHA256·비교 개수·반례 관측 또는 첫 실패가 들어갑니다.

## 검사 범위

| 항목 | 실행 수 | 기대 |
| --- | ---: | --- |
| 자료 부호화 / 오류 없는 복호 | 각각256 | 독립 generator 코드북과 원래 자료가 일치합니다. |
| 단일 오류 | 256×13 = 3,328 | parity 위치를 포함해 원래 코드워드·자료로 정정합니다. |
| 이중 오류 | 256×78 = 19,968 | 전부 uncorrectable이며 자료를 반환하지 않습니다. |
| 모든 13비트 입력 | 8,192 | 유효 코드워드 또는 그 반경1 이웃을 선택하는 정책과 일치합니다. |
| 보장 밖 반례 | 4 | 3중 오정정·4중 미검출·사용하지 않는 syndrome을 구별합니다. |

코드북의 서로 다른 모든 쌍 32,640개의 거리를 계산해 최소값4를 확인합니다. 독립 기준은 위치별 parity 식을 재사용하지 않고 고정 generator 기저로 256코드워드를 만든 뒤 1비트 이웃을 열거합니다. 8,192개 입력 검사는 이 선택 정책을 확인하며 여러 비트 오류의 원본을 알아낸다는 뜻이 아닙니다.

단일/이중 수는 원본 자료와 오류 위치의 조합 수이고, 32,035는 프로그램의 비교 횟수입니다. 같은 자료·수신값을 여러 관점에서 검사하므로 이 수들을 더해 독립 시험 수나 실제 장치 fault coverage로 계산하지 않습니다.

[원리·계산·반례](../../../설계와검증사례_engineering-cases/ECC의단일비트정정과이중비트검출_ecc-secded.md) · [실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/ECC오류주입과검출범위_20261021.md)

## English

This fixed educational extended Hamming(13,8) codec protects eight data bits with four Hamming parity bits and one overall parity bit. Position1 is integer bit0; position13 is the overall parity. Uncorrectable results expose no payload or corrected codeword.

Normal and optimized runs each pass 32,035 comparisons, including all 256 payloads, 3,328 single-error combinations, 19,968 double-error combinations, and all 8,192 received words against an independent radius-one codebook oracle. These counts overlap. Four controlled implementation defects fail in both modes. Three-bit miscorrection and four-bit undetected examples demonstrate limits rather than failures of the stated SECDED guarantee. No physical memory, vendor ECC, EDAC, BCH or LDPC implementation is tested.
