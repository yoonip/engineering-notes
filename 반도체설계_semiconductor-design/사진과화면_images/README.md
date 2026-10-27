# 사진과 설계 화면의 출처 | Chip photographs and EDA screenshots

[반도체 설계 목차](../README.md)

실물 사진, 레이아웃 출력과 도구 창 캡처를 구분하여 본문에 사용했습니다. 아래 원본 자료 표의 이미지는 제공된 파일 그대로 보관했습니다. 별도로 출력한 GDS 이미지는 레이아웃 원본 목록에 표시 설정과 함께 기록했습니다. 사진·화면 속 설계와 실행 기록의 제작자는 아래 출처에 표시한 기관·프로젝트입니다. 원본 자료 표의 확인일은 2026-10-26입니다.

## 회로·셀·배열의 실제 GDS

[회로와 레이아웃 원본](회로와레이아웃_layout-detail/README.md)에 SRAM 셀·주변회로·매크로, 인버터·ADC·전체 칩의 원본 파일과 확대 이미지를 모았습니다. 이 자료는 기존 GDS를 KLayout으로 출력했으며 보기 색·표시 층·확대 범위를 기록했습니다. 논문의 회로·레이아웃 원본 그림도 같은 출처 목록에서 연결합니다. 확인일은 2026-10-27입니다.

## SRAM·DRAM·HBM 사진과 설계 화면

최근 제품의 공개일, 실물·레이아웃·도구 화면의 종류와 원본은 [메모리 자료의 출처](메모리_memory/README.md)에서 확인할 수 있습니다.

## 원본 자료

| 자료 | 종류 | 제작자·제공처 | 원본과 설명 | 이용 조건 |
| --- | --- | --- | --- | --- |
| [NASA SiC RAM 다이](nasa-sic-ram-die.webp) | 실물 광학 사진 | NASA / NASA Glenn Research Center | [파일](https://science.nasa.gov/wp-content/uploads/2023/04/integrated_circuits_4-jpg.webp) · [설명](https://science.nasa.gov/science-research/science-enabling-technology/technology-highlights/integrated-circuits-to-enable-exploration-of-the-harshest-environments-in-solar-system/) | [NASA 교육·정보 목적 이용 지침](https://www.nasa.gov/nasa-brand-center/images-and-media/) |
| [NASA SiC 다이와 패키지](nasa-sic-package.webp) | 실물 사진 | NASA / NASA Glenn Research Center | [파일](https://science.nasa.gov/wp-content/uploads/2023/04/integrated_circuits_3-jpg.webp) · [설명](https://science.nasa.gov/science-research/science-enabling-technology/technology-highlights/integrated-circuits-to-enable-exploration-of-the-harshest-environments-in-solar-system/) | [NASA 교육·정보 목적 이용 지침](https://www.nasa.gov/nasa-brand-center/images-and-media/) |
| [Xschem RLC 회로도 편집기](xschem-rlc-schematic.png) | 실제 GUI 캡처 | Stefan Frederik Schippers / Xschem | [파일](https://github.com/StefanSchippers/xschem/blob/6066ee9ddbd925c1533f814a8444be997c779622/doc/xschem_man/tutorial_run_simulation_09.png) · [설명](https://xschem.sourceforge.io/stefan/xschem_man/tutorial_run_simulation.html) | [GPL-2.0-or-later](LICENSES/LICENSE-xschem-GPL-2.0-or-later.txt) |
| [ngspice RLC 파형·로그](xschem-ngspice-transient.png) | 실제 GUI 캡처 | Stefan Frederik Schippers / Xschem | [파일](https://github.com/StefanSchippers/xschem/blob/6066ee9ddbd925c1533f814a8444be997c779622/doc/xschem_man/tutorial_run_simulation_10.png) · [설명](https://xschem.sourceforge.io/stefan/xschem_man/tutorial_run_simulation.html) | [GPL-2.0-or-later](LICENSES/LICENSE-xschem-GPL-2.0-or-later.txt) |
| [JKU 인버터 매크로](jku-inverter-layout.png) | 설계 데이터의 레이아웃 출력 | © 2026 Simon Dorrer and Harald Pretl | [파일](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template/blob/b1d4a98d0ec8ad71c57f8ec4c33344340f911dad/tutorial/fig/inverter_top/inverter_top_black.png) · [설명](https://iic-jku.github.io/ihp-sg13g2-ams-chip-template/) | [Apache-2.0 WITH SHL-2.1](LICENSES/LICENSE-JKU-SHL-2.1.txt) · [Apache 전문](LICENSES/LICENSE-JKU-Apache-2.0.txt) |
| [JKU KLayout DRC](jku-inverter-drc.png) | 실제 검사 창 캡처 | © 2026 Simon Dorrer and Harald Pretl | [파일](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template/blob/b1d4a98d0ec8ad71c57f8ec4c33344340f911dad/tutorial/fig/inverter_top/KLayout_DRC_Output.png) · [설명](https://iic-jku.github.io/ihp-sg13g2-ams-chip-template/) | [Apache-2.0 WITH SHL-2.1](LICENSES/LICENSE-JKU-SHL-2.1.txt) · [Apache 전문](LICENSES/LICENSE-JKU-Apache-2.0.txt) |
| [JKU KLayout LVS](jku-inverter-lvs.png) | 실제 비교 창 캡처 | © 2026 Simon Dorrer and Harald Pretl | [파일](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template/blob/b1d4a98d0ec8ad71c57f8ec4c33344340f911dad/tutorial/fig/inverter_top/KLayout_LVS_Output.png) · [설명](https://iic-jku.github.io/ihp-sg13g2-ams-chip-template/) | [Apache-2.0 WITH SHL-2.1](LICENSES/LICENSE-JKU-SHL-2.1.txt) · [Apache 전문](LICENSES/LICENSE-JKU-Apache-2.0.txt) |
| [OpenROAD Ibex floorplan](openroad-ibex-floorplan.webp) | 실제 GUI 캡처 | © 2018–2025 The OpenROAD Authors | [파일](https://github.com/The-OpenROAD-Project/OpenROAD/blob/79eaac151c5b65925cc24226a8a116cfd2651f4a/docs/images/ibex_floorplan.webp) · [설명](https://github.com/The-OpenROAD-Project/OpenROAD/blob/79eaac151c5b65925cc24226a8a116cfd2651f4a/README.md) | [BSD-3-Clause](LICENSES/LICENSE-OpenROAD-BSD-3-Clause.txt) |
| [OpenROAD Ibex routing](openroad-ibex-routing.webp) | 실제 GUI 캡처 | © 2018–2025 The OpenROAD Authors | [파일](https://github.com/The-OpenROAD-Project/OpenROAD/blob/79eaac151c5b65925cc24226a8a116cfd2651f4a/docs/images/ibex_routing.webp) · [설명](https://github.com/The-OpenROAD-Project/OpenROAD/blob/79eaac151c5b65925cc24226a8a116cfd2651f4a/README.md) | [BSD-3-Clause](LICENSES/LICENSE-OpenROAD-BSD-3-Clause.txt) |
| [Caravel 전체 칩](caravel-layout.png) | 설계 데이터의 레이아웃 출력 | Efabless Corporation / Caravel contributors | [파일](https://github.com/efabless/caravel/blob/27cbe49c90ba5362ad52c9968dd98e035c30c74f/docs/source/_static/caravel.png) · [설명](https://caravel-harness.readthedocs.io/en/latest/) | [Apache-2.0](LICENSES/LICENSE-Caravel-Apache-2.0.txt) |

## 판본과 화면의 표시

| 자료 | 확보한 원본 판본 | 화면에서 확인한 정보 |
| --- | --- | --- |
| Xschem | `6066ee9ddbd925c1533f814a8444be997c779622` | RLC 공식 튜토리얼이며 캡처에 도구 릴리스 번호는 표시되어 있지 않습니다. |
| OpenROAD | `79eaac151c5b65925cc24226a8a116cfd2651f4a` | floorplan은 `v2.0-8870-gaaabb2ef8`, routing은 `v2.0-8693-g67ac6cf4b`로 서로 다른 공개 예시입니다. |
| JKU AMS 템플릿 | `b1d4a98d0ec8ad71c57f8ec4c33344340f911dad` | `inverter_top` 레이아웃과 2026-05-18로 표시된 DRC·LVS 결과 창입니다. |
| Caravel | `27cbe49c90ba5362ad52c9968dd98e035c30c74f` | 공식 문서의 기본 harness 전체 레이아웃입니다. |
| NASA Science | 2020-01-15 기사, 2024-08-14 갱신 표시 | 패키징 전 SiC RAM 다이와 별도의 SiC 패키지 사례입니다. |

고정 커밋은 원본 이미지 파일을 확보한 자료 판본입니다. 캡처 당시 프로그램의 릴리스 번호와는 구분합니다. JKU 그림 경로의 저작권·라이선스 지정은 [원본 REUSE.toml](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template/blob/b1d4a98d0ec8ad71c57f8ec4c33344340f911dad/REUSE.toml)과 [보관한 고지](LICENSES/REUSE-JKU.toml)에서도 확인할 수 있습니다.

## 관련 본문

- [도구와 공급사](../03-설계도구와공급사_eda-tool-map.md)
- [회로 설계와 파형](../04-회로설계와Spectre_custom-circuit-simulation.md)
- [배치배선과 전력망](../09-배치배선과전력설계_physical-implementation.md)
- [DRC·LVS·PEX](../10-DRC와LVS및PEX_physical-verification.md)
- [풀커스텀 레이아웃](../14-아날로그풀커스텀레이아웃_full-custom-layout.md)
- [칩 최상위 검증과 패키지](../17-칩최상위검증과제조인계_chip-top-signoff.md)
