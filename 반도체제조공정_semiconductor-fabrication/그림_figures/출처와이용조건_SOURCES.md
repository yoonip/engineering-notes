# 그림 출처와 원문 | Figure sources and attribution

[공정 목차](../README.md) · [단면으로 보는 공정 흐름](../11-단면으로보는공정흐름_cross-section-atlas.md)

공정 원리를 설명하기 위해 작성한 개념도와 외부에서 가져온 원도면을 구분합니다. 공정별 장비 사진·연구 단면의 원자료는 해당 본문의 공식 링크로 연결합니다. 공개 웹페이지에 있다는 사실만으로 모든 그림의 재배포가 허용되는 것은 아니므로, 외부 파일은 확인한 이용 조건과 함께 표시했습니다.

## 자체 개념도

다음 SVG는 이 저장소의 설명을 위해 직접 구성했습니다. 공식 자료의 도안·제품 사진·실측 단면을 추적하거나 복제한 그림은 아닙니다. 색은 물질의 실제 색이 아니라 역할을 구분하는 표시이며, 막 두께·폭·깊이는 축척을 나타내지 않습니다.

| 그림 | 설명하는 내용 | 원리 확인에 연결한 공식 자료 |
| --- | --- | --- |
| [웨이퍼 단면](01-웨이퍼단면_wafer-section.svg) | 잉곳·절단 손상·표면 가공 | [SK실트론 제조 흐름](https://www.sksiltron.com/ko/wafer/process.do), [DISCO의 연삭과 손상 완화 설명](https://www.disco.co.jp/eg/solution/library/grinder/thin.html) |
| [열산화 단면](02-산화단면_oxidation-section.svg) | 원래 표면, Si 소비와 산화막 계면 | [SK하이닉스 산화 원리](https://news.skhynix.com/en/semiconductor-front-end-process-episode-2/), [산화 장의 물질수지·성장 모형 근거](../02-산화와게이트절연막_oxidation-gate-dielectrics.md#12-출처와-확인-범위) |
| [포토 단면](03-포토단면_lithography-section.svg) | 양성 PR의 도포·노광·현상 | [EPFL CMi 포토 기초](https://www.epfl.ch/research/facilities/cmi/process/photolithography/introductiontophotolithography/), [삼성전자 포토 공정](https://semiconductor.samsung.com/kr/support/tools-resources/fabrication-process/eight-essential-semiconductor-fabrication-processes-part-4-photolithography-laying-the-blueprint/) |
| [식각 단면](04-식각단면_etch-section.svg) | 마스크 창, 대상막 제거, 마스크 제거 | [EPFL CMi 식각 정의](https://www.epfl.ch/research/facilities/cmi/process/etching/etch-definitions/), [삼성전자 식각 공정](https://semiconductor.samsung.com/kr/support/tools-resources/fabrication-process/eight-essential-semiconductor-fabrication-processes-part-5-etching-a-circuit-pattern/) |
| [증착·주입 단면](05-증착주입단면_deposition-implant-section.svg) | 내부 피복과 별도의 주입·열처리 | [ASM ALD 원리](https://www.asm.com/our-technology-products/ald), [Applied Materials 재료 특성 조절](https://www.appliedmaterials.com/eu/en/semiconductor/semiconductor-capabilities/modify.html) |
| [배선·CMP 단면](06-배선CMP단면_interconnect-section.svg) | 홈·via, 계면막·구리 채움·평탄화 | [IBM 구리 배선의 다마신 설명](https://www.ibm.com/history/copper-interconnects), [EBARA 연마 원리](https://ebara.com/global-en/technology/information/polishing-technology-ex/) |
| [웨이퍼 검사 단면](07-검사단면_wafer-probe-section.svg) | pad 접근과 좌표별 판정 | [삼성전자 EDS 공정](https://semiconductor.samsung.com/kr/support/tools-resources/fabrication-process/eight-essential-semiconductor-fabrication-processes-part-8-eds-electrical-die-sorting-for-the-perfect-chips/), [Advantest 반도체 시험](https://www.advantest.com/en/about/business/) |
| [패키징 단면](08-패키징단면_packaging-section.svg) | flip-chip BGA의 내부·외부 접속 | [SK하이닉스 전통 패키지 설명](https://news.skhynix.com/en/semiconductor-back-end-process-episode-6-conventional-packages/), [Amkor Flip Chip BGA 자료](https://amkor.com/wp-content/uploads/2018/02/Flip_Chip_TS102.pdf) |
| [소자·배선의 연속 단면](소자와배선의연속단면_device-sequence.svg) | 같은 평면형 소자의 게이트·접합·contact·배선 | [MIT 6.004 MOSFET·CMOS 원리](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c3/c3s1/), [통합 흐름의 본문과 근거](../09-공정통합과품질관리_integration-process-control.md) |
| [패턴 전사](패턴전사_pattern-transfer.svg) | PR의 창을 아래 막에 옮기는 기존 개념도 | [포토 본문의 출처](../03-포토와노광_photolithography.md#14-출처와-확인-범위), [식각 본문의 출처](../04-식각과선택비_etching.md#12-출처와-확인-범위) |

증착·주입 그림의 A→B와 C→D는 서로 다른 예입니다. 검사 그림의 판정 맵도 실제 관측 자료가 아닙니다. 패키지 기판·언더필·Si die는 재료와 역할이 다르며, 내부 범프와 외부 ball도 구분합니다.

## 외부 원도면

### MIT OpenCourseWare의 n채널 MOSFET 구조

| 항목 | 내용 |
| --- | --- |
| 저장한 파일 | [mit-6-004-nmos-physical-view.png](외부자료_external/mit-6-004-nmos-physical-view.png) |
| 저작자·제공처 | Chris Terman / MIT OpenCourseWare, Massachusetts Institute of Technology |
| 강좌·위치 | 6.004 Computation Structures, Spring 2017, L03: CMOS Technology의 “N-Channel MOSFET: Physical View” |
| 공식 원문 | [3.1 Annotated Slides](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c3/c3s1/) |
| 이미지 원본 | [MIT OCW Slide03.png](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/d18fcd081f55667ad0111c80b6173df6_Slide03.png) |
| 이용 조건 | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), [MIT OCW Privacy and Terms of Use](https://ocw.mit.edu/pages/privacy-and-terms-of-use/) |
| 변경 | 원본 파일의 이미지·영문·크기·색을 변경하지 않았습니다. 한글 설명은 본문에 별도로 작성했습니다. |
| 기술적 범위 | poly-Si 게이트·SiO₂를 사용하는 평면형 nMOS의 개념 설명입니다. 현대 모든 제품의 막 두께·게이트 재료·양산 순서를 뜻하지 않습니다. |
| 확인일 | 2026-10-26 |

이 PNG에는 위 출처의 비영리·저작자 표시·동일조건변경허락 조건이 적용됩니다. 다른 파일의 이용 조건을 이 PNG로부터 일괄 추정하지 않습니다. 저작자·제공처 표시는 출처를 밝히기 위한 것이며 MIT의 검토·보증·제휴를 뜻하지 않습니다.

## 공식 그림·장비 사진을 더 볼 곳

- [SK실트론 웨이퍼 제조 흐름](https://www.sksiltron.com/ko/wafer/process.do): 잉곳 성장부터 절단·형상 가공·연마·세정까지의 공식 그림입니다.
- [삼성전자 8대 공정의 포토 설명](https://semiconductor.samsung.com/kr/support/tools-resources/fabrication-process/eight-essential-semiconductor-fabrication-processes-part-4-photolithography-laying-the-blueprint/): 감광막과 마스크·노광의 공식 그림입니다.
- [삼성전자 금속배선 공정](https://semiconductor.samsung.com/kr/support/tools-resources/fabrication-process/eight-essential-semiconductor-fabrication-processes-part-7-metal-interconnects-electrical-highways/): 소자와 배선을 연결하는 설명 그림입니다.
- [ASML의 EUV 시스템](https://www.asml.com/en/products/euv-lithography-systems): NXE·EXE 장비의 공식 사진과 역할입니다.
- [TSMC CoWoS](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm): CoWoS-S·R·L의 구조를 비교하는 공식 그림입니다.
- [TSMC SoIC](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/SoIC.htm): die 적층과 연결 구조의 공식 그림입니다.

이 목록의 기업 이미지는 저장소에 복제하지 않고 원문으로 연결했습니다. 각 공정의 본문에는 추가 장비와 실제 보고 사례의 자료를 연결했습니다.
