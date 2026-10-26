# 최종 파일과 제조 인계 | Tapeout deliverables

[설계 목차](README.md) · [DRC·LVS·PEX](10-DRC와LVS및PEX_physical-verification.md) · [HBM·3D 집적](11-HBM과3D집적설계_hbm-3d-integration.md)

## GDS가 생긴 뒤에 확인하는 것

GDSII와 OASIS는 레이아웃의 도형·계층·배치 등을 전달하는 형식입니다. 회로도 화면에서 보이는 그림을 저장한 이미지와 다릅니다. 같은 디자인을 GDSII 또는 OASIS로 저장할 수 있지만, 제조에 받는 형식은 공정 제공기관과 합의합니다. [KLayout의 저장 문서](https://www.klayout.org/downloads/master/doc-qt5/manual/save.html)는 셀·계층·레이어 선택과 저장 형식을 설명합니다.

파일을 열 수 있어도 실제 제조에 필요한 도형이 빠져 있을 수 있습니다. 레이아웃을 저장할 때 top cell과 하위 계층, 셀·매크로의 실제 도형, 레이어 매핑, 데이터베이스 단위가 일치하는지 확인합니다. [KLayout Database API의 Layout·database unit 설명](https://www.klayout.org/downloads/master/doc-qt5/programming/database_api.html)은 정수 좌표와 물리 길이의 관계를 설명합니다. 예를 들어 단위가 0.001 μm일 때 좌표 차이 100은 0.1 μm입니다. 이 예시는 단위 변환을 보여 주는 자체 계산입니다.

## 파일별 역할과 전달 대상

아래는 설계 데이터를 분류하기 위한 일반적인 묶음입니다. 실제 제출 형식·필수 파일·암호화·전송 방식은 선택한 공정·IP·MPW 프로그램의 요구사항을 따릅니다.

| 자료 | 주요 내용 | 함께 맞춰 볼 대상 |
| --- | --- | --- |
| 최종 GDSII/OASIS | 모든 제출 대상의 레이아웃 도형과 계층 | top cell·공정·금속 옵션·레이어·단위·die 크기 |
| 최종 넷리스트·CDL/SPICE | 논리·트랜지스터의 연결 | LVS 기준과 실제 추출 넷리스트 |
| DEF·물리 데이터베이스 | 배치·배선·설계 상태 | GDS 생성에 사용한 같은 설계 판본 |
| LEF·매크로 물리 추상 | 크기·핀·막힘 영역 | 실제 GDS·포트·전원과 일치 여부 |
| Liberty·타이밍 모델 | 지연·제약·전력의 특성화 결과 | 셀·매크로 판본과 PVT·부하 범위 |
| SDC·모드/코너 설정 | 클록·I/O 조건·예외 경로 | 검토한 모든 모드와 STA 보고서 |
| 기생 추출 데이터 | 배선 저항·정전용량·결합 | 추출 대상의 GDS/배선·RC 코너·넷 이름 |
| 검증 보고서 | DRC·LVS·ERC·antenna·density·STA 등 | 사용한 rule deck·설계 파일·승인된 예외 |
| 전력·신뢰성 보고서 | IR drop·EM·전력 상태와 열 조건 | 활동도·전류·전원·온도·패키지 조건 |
| IP·PDK 판본 기록 | 모델·셀·메모리·공정 자료의 식별자 | 검증에서 읽은 파일과 전달한 결과물 |
| 검사·패키지 자료 | pad/bump 맵·전원·테스트 접근·조립 정의 | 외부 연결과 적층 전·후 검사 계획 |

표준셀의 실제 GDS를 합치지 않고 LEF 크기만 남기면 배치 화면은 그럴듯해 보여도 트랜지스터·배선 도형이 완성되지 않습니다. [ETH·PULP의 공개 물리 검증 실습](https://pulp-platform.org/docs/efclseminar2026/track1_ex/ex06.pdf)의 Design Flow Recap은 DEF·LEF·셀의 GDS 도형을 합쳐 검증용 GDS를 만드는 과정을 설명합니다. 해당 실습의 특정 경로를 다른 도구 흐름에 그대로 적용하지 않고, 본인의 흐름에서 같은 자료가 어떻게 합쳐지는지 확인합니다.

## 제출 전 확인하는 순서

1. 제조할 공정·금속 옵션·top cell·die 경계와 사용할 IP 판본을 고정합니다.
2. 최종 넷리스트와 레이아웃을 기준으로 검증을 다시 연결합니다. 중간 배치 파일의 결과를 최종 배선 결과로 표시하지 않습니다.
3. DRC·LVS·ERC·density·antenna 등의 필수 항목과 해당 공정에서 추가로 요구하는 항목을 확인합니다.
4. 실제 RC·동작 모드·공정/전압/온도에서 타이밍·회로 성능·전력·신뢰성을 확인합니다.
5. 도형이나 연결을 바꾼 ECO가 있으면 영향을 받는 검증을 다시 수행합니다.
6. 보고서가 어떤 입력 해시·도구·deck·설정에 해당하는지 묶습니다.
7. 제조·패키지·검사 담당자와 전송·수신·검토 승인을 확인합니다.

이 순서는 인계를 설명하기 위해 정리한 것입니다. 공정의 승인 절차를 대신하는 임의의 ‘통과 기준’은 아닙니다. [GF180MCU Essential Tapeout Checklist](https://gf180mcu-pdk.readthedocs.io/en/latest/physical_verification/design_manual/drm_06.html)는 계층형 GDSII 제공, 필요한 레이어 전체 제공과 제출 전 DRC 통과를 명시합니다. LVS·전기적 성능·신뢰성 등의 항목은 사용하는 공정과 프로젝트의 별도 제출 규칙까지 확인합니다.

## 검증 결과와 파일을 묶는 방법

다음 두 명령은 [GNU Coreutils의 SHA-2 도구](https://www.gnu.org/s/coreutils/manual/html_node/sha2-utilities.html)를 사용해 직접 구성한 파일 동일성 확인 예입니다. EDA 공급사의 tapeout 스크립트가 아니며 설계 검증을 수행하지 않습니다. `final.gds`와 `final.cdl`이 있는 별도의 인계 폴더에서 실행합니다.

```bash
sha256sum final.gds final.cdl > SHA256SUMS  # 두 파일의 SHA-256과 이름을 계산하고 >로 목록에 기록합니다.
sha256sum --check SHA256SUMS               # --check로 현재 파일이 기록한 해시와 같은지 확인합니다.
```

파일을 받는 쪽에서도 같은 목록과 파일을 비교하면 전송 중 바뀐 데이터나 다른 판본의 혼입을 확인할 수 있습니다. 해시가 같다는 것은 파일의 동일성에 관한 확인입니다. 어떤 공정에서 회로가 동작하는지는 설계 검증 보고서로 확인합니다. 공개 저장소에는 권한이 있는 공개 PDK·소스·결과만 올리고, 기관에서 제공받은 비공개 PDK나 라이선스 파일은 해당 기관의 보관 위치에서 관리합니다.

검증 이력을 읽을 때에는 ‘DRC errors 0’만 적지 않고 사용한 deck·범위·미지원 규칙·승인 예외를 같이 읽습니다. 예외를 없애기 위해 도구 설정에서 규칙을 끈 결과와, 공정 담당자가 승인한 예외는 의미가 다릅니다.

## 인계에서 자주 드러나는 문제

| 겉으로 보이는 결과 | 실제 확인할 원인 | 확인 방법 |
| --- | --- | --- |
| GDS가 열리지만 내부가 빈 블록 | 매크로·표준셀 GDS를 합치지 않았습니다. | 계층 아래의 실제 도형과 입력 라이브러리 목록을 대조합니다. |
| 크기가 예상과 다릅니다. | 단위·스케일·공정 옵션이 다릅니다. | die 경계의 물리 길이와 데이터베이스 단위를 확인합니다. |
| 같은 설계가 LVS에서 달라집니다. | top cell·전원 이름·핀 순서·매크로 기준이 다릅니다. | 최종 넷리스트와 추출 입력·매크로 판본을 대조합니다. |
| 수정 후 옛 보고서가 남았습니다. | ECO 이전 결과를 함께 묶었습니다. | 입력 해시와 실행 시점·설계 판본을 대조합니다. |
| 단일 다이는 맞지만 적층 연결이 틀립니다. | 다이 회전·반전·범프 대응이 다릅니다. | 조립 좌표와 다이별 핀·범프 맵을 검사합니다. |
| GDS만 전달하고 제작이 진행되지 않습니다. | 프로그램 등록·계약·필수 자료·인계 승인이 남았습니다. | 제조 프로그램의 제출 절차와 수신 상태를 확인합니다. |

이 표는 원인을 찾는 설명용 사례이며 실제 고객 장애 기록은 아닙니다.

## GDS 이후에는 마스크와 제조가 이어집니다

설계 GDS의 도형이 그대로 사진처럼 축소되어 웨이퍼에 찍히는 것은 아닙니다. [ASML의 computational lithography 설명](https://www.asml.com/en/products/computational-lithography)은 공정 모델로 마스크 패턴을 조정해 웨이퍼에서 원하는 패턴을 얻는 원리를 설명합니다. [Fraunhofer IPMS의 Mask Data Preparation](https://www.ipms.fraunhofer.de/en/cleanrooms/Screening-Fab-Services/Semiconductor-Process-Services/Lithography.html)은 설계 레이어를 노광 레이어로 변환하고, 레이어 연산·마스크 프레임·형식 변환을 적용하는 실제 서비스 범위를 설명합니다.

따라서 설계 팀의 GDS 인계, 마스크 데이터 준비, 웨이퍼 제조, 웨이퍼 검사, 패키징, 최종 시험은 서로 이어지는 별도 단계입니다. 이 제조 과정은 [반도체 제조 공정](../반도체제조공정_semiconductor-fabrication/README.md)에서 이어집니다.

## 실제 제작 경로를 선택할 때

MPW는 여러 설계가 한 웨이퍼 제작 비용을 나누는 방식입니다. 공개 설계도 참여 계약과 사용 가능한 공정·면적·일정·결과물 조건을 확인합니다. [IHP Open-Silicon MPW](https://dk.ihp-microelectronics.com/OpenSourceRequest.php)는 공개 설계의 참여·라이선스·계약 조건을 설명하고, [imec IC-Link의 MPW 안내](https://www.imeciclink.com/en/asic-fabrication/mpw-schedules-2026)는 등록 시점과 GDS 제출 기한을 구분합니다. 비용·일정은 각 프로그램의 해당 회차에서 확인합니다.

HBM·멀티다이에서는 다이별 설계 인계 외에 조립체의 연결·재료·열·검사 자료가 추가됩니다. 각 다이의 GDS 하나를 하나의 거대한 GDS에 합치는 것만으로 조립 설계가 끝나지 않는 이유는 [HBM·3D 집적 설계](11-HBM과3D집적설계_hbm-3d-integration.md)에서 설명합니다.
