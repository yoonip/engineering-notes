# 회로·레이아웃 원본과 출처 | Circuit and layout sources

[실제 회로와 레이아웃 읽기](../../18-실제회로와레이아웃읽기_circuit-layout-walkthrough.md) · [전체 사진·화면 출처](../README.md)

확인일: 2026-10-27. 원본 GDS·회로·넷리스트는 파일 내용 그대로 보관했습니다. GDS에서 출력한 PNG는 KLayout 0.30.12의 정적 이미지이며, 보기 색·무늬·표시 층·확대 범위만 바꾸었습니다. 원본 설계의 도형·배치를 새로 작성하지 않았습니다.

## 설계 원본과 대응 자료

| 보관 파일 | 원본 판본·경로 | 이용 조건 |
| --- | --- | --- |
| [openram/cell_1rw.gds](원본_sources/openram/cell_1rw.gds) | [원본](https://github.com/VLSIDA/OpenRAM/blob/b2b069ce119d1488cbe6883b2240bceb5c7ce29a/technology/freepdk45/gds_lib/cell_1rw.gds) · `b2b069c` | BSD-3-Clause |
| [openram/cell_1rw.sp](원본_sources/openram/cell_1rw.sp) | [원본](https://github.com/VLSIDA/OpenRAM/blob/b2b069ce119d1488cbe6883b2240bceb5c7ce29a/technology/freepdk45/sp_lib/cell_1rw.sp) · `b2b069c` | BSD-3-Clause |
| [openram/sense_amp.gds](원본_sources/openram/sense_amp.gds) | [원본](https://github.com/VLSIDA/OpenRAM/blob/b2b069ce119d1488cbe6883b2240bceb5c7ce29a/technology/freepdk45/gds_lib/sense_amp.gds) · `b2b069c` | BSD-3-Clause |
| [openram/sense_amp.sp](원본_sources/openram/sense_amp.sp) | [원본](https://github.com/VLSIDA/OpenRAM/blob/b2b069ce119d1488cbe6883b2240bceb5c7ce29a/technology/freepdk45/sp_lib/sense_amp.sp) · `b2b069c` | BSD-3-Clause |
| [openram/write_driver.gds](원본_sources/openram/write_driver.gds) | [원본](https://github.com/VLSIDA/OpenRAM/blob/b2b069ce119d1488cbe6883b2240bceb5c7ce29a/technology/freepdk45/gds_lib/write_driver.gds) · `b2b069c` | BSD-3-Clause |
| [openram/write_driver.sp](원본_sources/openram/write_driver.sp) | [원본](https://github.com/VLSIDA/OpenRAM/blob/b2b069ce119d1488cbe6883b2240bceb5c7ce29a/technology/freepdk45/sp_lib/write_driver.sp) · `b2b069c` | BSD-3-Clause |
| [openram/layers.map](원본_sources/openram/layers.map) | [원본](https://github.com/VLSIDA/OpenRAM/blob/b2b069ce119d1488cbe6883b2240bceb5c7ce29a/technology/freepdk45/layers.map) · `b2b069c` | BSD-3-Clause |
| [ihp/sram1024x32.gds](원본_sources/ihp/sram1024x32.gds) | [원본](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/5e6d592e4002946a4616f798c357f0f3c06cf3b6/ihp-sg13g2/libs.ref/sg13g2_sram/gds/RM_IHPSG13_1P_1024x32_c2_bm_bist.gds) · `5e6d592` | Apache-2.0 |
| [ihp/sram1024x32.cdl](원본_sources/ihp/sram1024x32.cdl) | [원본](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/5e6d592e4002946a4616f798c357f0f3c06cf3b6/ihp-sg13g2/libs.ref/sg13g2_sram/cdl/RM_IHPSG13_1P_1024x32_c2_bm_bist.cdl) · `5e6d592` | Apache-2.0 |
| [ihp/sg13g2.lyp](원본_sources/ihp/sg13g2.lyp) | [원본](https://github.com/IHP-GmbH/IHP-Open-PDK/blob/5e6d592e4002946a4616f798c357f0f3c06cf3b6/ihp-sg13g2/libs.tech/klayout/tech/sg13g2.lyp) · `5e6d592` | Apache-2.0 |
| [jku-ihp/inverter.gds](원본_sources/jku-ihp/inverter.gds) | [원본](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template/blob/b1d4a98d0ec8ad71c57f8ec4c33344340f911dad/macros/inverter/layout/inverter.gds) · `b1d4a98` | Apache-2.0 WITH SHL-2.1 |
| [jku-ihp/inverter.sch](원본_sources/jku-ihp/inverter.sch) | [원본](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template/blob/b1d4a98d0ec8ad71c57f8ec4c33344340f911dad/macros/inverter/schematic/xschem/inverter.sch) · `b1d4a98` | Apache-2.0 WITH SHL-2.1 |
| [jku-ihp/inverter.cdl](원본_sources/jku-ihp/inverter.cdl) | [원본](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template/blob/b1d4a98d0ec8ad71c57f8ec4c33344340f911dad/macros/inverter/netlist/schematic/inverter_klayout.cdl) · `b1d4a98` | Apache-2.0 WITH SHL-2.1 |
| [jku-ihp/chip_top.gds.gz](원본_sources/jku-ihp/chip_top.gds.gz) | [원본](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template/blob/b1d4a98d0ec8ad71c57f8ec4c33344340f911dad/layout/chip_top.gds.gz) · `b1d4a98` | Apache-2.0 WITH SHL-2.1 |
| [jku-ihp/inverter-schematic.svg](원본_sources/jku-ihp/inverter-schematic.svg) | [원본](https://github.com/iic-jku/ihp-sg13g2-ams-chip-template/blob/b1d4a98d0ec8ad71c57f8ec4c33344340f911dad/tutorial/fig/inverter_top/inverter_schematic.svg) · `b1d4a98` | Apache-2.0 WITH SHL-2.1 |
| [jku-sar/adc_top.gds.gz](원본_sources/jku-sar/adc_top.gds.gz) | [원본](https://github.com/iic-jku/SKY130_SAR-ADC1/blob/3cec5823e64cf1ea5c625615ad71f2a505cf27bc/gds/adc_top.gds.gz) · `3cec582` | Apache-2.0 |
| [jku-sar/adc_comp_latch.gds.gz](원본_sources/jku-sar/adc_comp_latch.gds.gz) | [원본](https://github.com/iic-jku/SKY130_SAR-ADC1/blob/3cec5823e64cf1ea5c625615ad71f2a505cf27bc/gds/adc_comp_latch.gds.gz) · `3cec582` | Apache-2.0 |
| [jku-sar/adc_comp_latch.sch](원본_sources/jku-sar/adc_comp_latch.sch) | [원본](https://github.com/iic-jku/SKY130_SAR-ADC1/blob/3cec5823e64cf1ea5c625615ad71f2a505cf27bc/xschem/adc_comp_latch.sch) · `3cec582` | Apache-2.0 |
| [jku-sar/adc_comp_circuit.sch](원본_sources/jku-sar/adc_comp_circuit.sch) | [원본](https://github.com/iic-jku/SKY130_SAR-ADC1/blob/3cec5823e64cf1ea5c625615ad71f2a505cf27bc/xschem/adc_comp_circuit.sch) · `3cec582` | Apache-2.0 |
| [jku-sar/adc_comp_latch.sch.spice](원본_sources/jku-sar/adc_comp_latch.sch.spice) | [원본](https://github.com/iic-jku/SKY130_SAR-ADC1/blob/3cec5823e64cf1ea5c625615ad71f2a505cf27bc/spice/adc_comp_latch.sch.spice) · `3cec582` | Apache-2.0 |
| [jku-sar/adc_top.sch](원본_sources/jku-sar/adc_top.sch) | [원본](https://github.com/iic-jku/SKY130_SAR-ADC1/blob/3cec5823e64cf1ea5c625615ad71f2a505cf27bc/xschem/adc_top.sch) · `3cec582` | Apache-2.0 |

## 이미지와 표시 범위

| 이미지 | 원본에서 표시한 범위 |
| --- | --- |
| [openram-cell_1rw-all-layers.png](openram-cell_1rw-all-layers.png) | `cell_1rw` · 원본의 전체 도형층 · 선택 셀 전체 · 1600×2600 px |
| [openram-cell_1rw-devices.png](openram-cell_1rw-devices.png) | `cell_1rw` · 레이어 1, 2, 3, 4, 5, 6, 9, 10 · 선택 셀 전체 · 1600×2600 px |
| [openram-sense_amp-all-layers.png](openram-sense_amp-all-layers.png) | `sense_amp` · 원본의 전체 도형층 · 선택 셀 전체 · 1000×2600 px |
| [openram-write_driver-all-layers.png](openram-write_driver-all-layers.png) | `write_driver` · 원본의 전체 도형층 · 선택 셀 전체 · 1000×2600 px |
| [ihp-sram1024x32-full.png](ihp-sram1024x32-full.png) | `RM_IHPSG13_1P_1024x32_c2_bm_bist` · 원본의 전체 도형층 · 선택 셀 전체 · 4000×3300 px |
| [ihp-sram-bitkit-cell.png](ihp-sram-bitkit-cell.png) | `RM_IHPSG13_1P_BITKIT_CELL` · 원본의 전체 도형층 · 선택 셀 전체 · 2400×1700 px |
| [ihp-sram-16x2-array.png](ihp-sram-16x2-array.png) | `RM_IHPSG13_1P_BITKIT_16x2_SRAM` · 원본의 전체 도형층 · 선택 셀 전체 · 1400×3100 px |
| [jku-ihp-chip-top-full.png](jku-ihp-chip-top-full.png) | `chip_top` · 원본의 전체 도형층 · 선택 셀 전체 · 4000×4000 px |
| [jku-ihp-inverter-cell.png](jku-ihp-inverter-cell.png) | `inverter` · 원본의 전체 도형층 · 선택 셀 전체 · 2800×1400 px |
| [jku-sar-comparator-detail.png](jku-sar-comparator-detail.png) | `adc_comp_latch` · 원본의 전체 도형층 · 확대 좌표 [10, 48, 42, 80] µm · 2400×2400 px |
| [jku-sar-adc-full.png](jku-sar-adc-full.png) | `adc_top` · 원본의 전체 도형층 · 선택 셀 전체 · 3600×3400 px |

FreePDK45와 SKY130의 색·무늬는 이 글에서 정한 [보기 설정](원본_sources/보기설정_display)입니다. IHP 그림은 보관한 공식 `sg13g2.lyp`를 사용했습니다. IHP 하위 셀·SKY130 그림에서는 겹치는 텍스트를 숨겼으며, 도형은 그대로 유지했습니다. 인버터 회로도 SVG는 원저자의 파일입니다.

## 논문의 회로·레이아웃·칩 사진

원문 PDF: [eDRAM 회로·레이아웃 논문](https://mdpi-res.com/d_attachment/sensors/sensors-23-09329/article_deploy/sensors-23-09329.pdf) · [HBM 인터포저 배선 논문](https://mdpi-res.com/d_attachment/micromachines/micromachines-16-00896/article_deploy/micromachines-16-00896.pdf)

| 보관 그림 | 원문과 그림 번호 | 저작자·이용 조건 |
| --- | --- | --- |
| [hbm-2025-fig3.png](hbm-2025-fig3.png) · [출판사 PNG](https://mdpi-res.com/micromachines/micromachines-16-00896/article_deploy/html/images/micromachines-16-00896-g003.png) | [원논문](https://www.mdpi.com/2072-666X/16/8/896) · Figure 3(a)-(b) | Wen-Xue Tang et al. (2025) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [edram-2023-fig15.png](edram-2023-fig15.png) · [출판사 PNG](https://mdpi-res.com/sensors/sensors-23-09329/article_deploy/html/images/sensors-23-09329-g015.png) | [원논문](https://www.mdpi.com/1424-8220/23/23/9329) · Figure 15(a)-(c) | Subin Kim, Ingu Jeong, Jun-Eun Park (2023) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [edram-2023-fig7.png](edram-2023-fig7.png) · [출판사 PNG](https://mdpi-res.com/sensors/sensors-23-09329/article_deploy/html/images/sensors-23-09329-g007.png) | [원논문](https://www.mdpi.com/1424-8220/23/23/9329) · Figure 7 | Subin Kim, Ingu Jeong, Jun-Eun Park (2023) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [edram-2023-fig14.png](edram-2023-fig14.png) · [출판사 PNG](https://mdpi-res.com/sensors/sensors-23-09329/article_deploy/html/images/sensors-23-09329-g014.png) | [원논문](https://www.mdpi.com/1424-8220/23/23/9329) · Figure 14 | Subin Kim, Ingu Jeong, Jun-Eun Park (2023) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

논문 그림은 전체 원본 PNG를 보관했으며 자르기·색 변경·도형·주석 추가를 하지 않았습니다. eDRAM은 gain-cell 연구, HBM 그림은 인터포저 배선 연구입니다. 상용 DRAM·HBM 최신 코어 다이의 전체 GDS로 소개하지 않습니다.

## 저작권과 이용 조건

- OpenRAM: [BSD-3-Clause 전문](이용조건_licenses/OpenRAM-BSD-3-Clause.txt)의 저작권·조건을 보존합니다.
- JKU IHP: © 2026 Simon Dorrer and Harald Pretl. [REUSE.toml](이용조건_licenses/jku-ihp-REUSE.toml)이 지정한 Apache-2.0 WITH SHL-2.1 자료입니다. [프로젝트 LICENSE](이용조건_licenses/jku-ihp-LICENSE), [Apache 전문](이용조건_licenses/jku-ihp-Apache-2.0.txt), [SHL 전문](이용조건_licenses/jku-ihp-SHL-2.1.txt)을 보관했습니다.
- IHP: Copyright 2025 IHP PDK Authors. [Apache-2.0 전문](이용조건_licenses/ihp-pdk-LICENSE)을 보관했습니다. 공식 레이어 파일의 Copyright 2024 고지와 CDL의 Copyright 2025 고지는 원문대로 유지합니다. JKU 전체 칩의 PDK 유래 부분에도 IHP 고지가 적용됩니다.
- JKU SAR ADC: Copyright 2022 Manuel Moser가 표시된 원본 회로 자료와 [Apache-2.0 전문](이용조건_licenses/jku-sar-LICENSE)을 보관했습니다. SKY130 유래 부분의 [소자 라이브러리 라이선스](이용조건_licenses/skywater-pdk-libs-sky130_fd_pr-LICENSE)와 [표준셀 라이브러리 라이선스](이용조건_licenses/skywater-pdk-libs-sky130_fd_sc_hd-LICENSE)도 함께 보관했습니다.
- 논문 이미지: 위 표의 저자·논문·그림 번호와 CC BY 4.0을 표시합니다. 이미지의 권리는 각 원저자에게 있습니다.

## 파일 판본과 해시

[source-manifest.json](source-manifest.json)에 각 파일의 원본 URL·커밋·SHA-256, GDS 출력의 셀 이름·레이어·확대 좌표를 기록했습니다. 원본 파일의 이름 일부는 서로 다른 프로젝트를 구별하기 위해 보관 경로에서 바꾸었으며 파일 내용은 유지했습니다. 출처 파일의 동일성 확인과 회로의 DRC·LVS·PEX 또는 시뮬레이션 통과는 서로 다른 확인입니다.

## English

Original circuit/layout sources and static KLayout exports, with pinned upstream revisions, matching netlists, image framing, attribution and license files. Research figures are retained as unmodified publisher PNGs. File hashes identify the stored bytes; no new design signoff or measurement is claimed.
