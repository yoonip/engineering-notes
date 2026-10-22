# 전기·전자·통신 과목별 공개 강의 | Electrical engineering and communications courses

[학습 사이트와 채널](README.md) · [전공 유튜브 채널](전기전자통신유튜브_electrical-engineering-youtube.md) · [컴퓨터공학·AI 과목](컴퓨터공학과AI과목_cs-ai-courses.md)

수학·물리에서 회로·소자·전력·통신·제어·디지털 하드웨어로 이어지는 공개 강의와 교재입니다. 한국어 강의와 영어 심화 자료를 과목별로 모아, 학부 기초부터 석·박사 전공 공부에 필요한 자료까지 찾을 수 있게 정리했습니다.

표의 선수지식은 공부를 시작할 때 권하는 배경입니다. 학교별 필수·선택 과목과 석·박사 이수 규정은 아래 공식 교육과정에서 확인하실 수 있습니다.

## 공부 순서

미적분·선형대수·미분방정식과 기초 물리를 익힌 뒤 회로이론·전자기학·논리회로·프로그래밍으로 이어갑니다. 회로 분야는 전자회로 → 집적회로·RF·혼합신호, 통신 분야는 신호와 시스템·확률 → DSP·통신·정보이론, 전력 분야는 교류 회로·전자기학 → 전력계통·전기기기·전력전자 순서로 접근하시면 좋습니다.

## 수학·물리·계산의 바탕

| 과목 | 강의·교재 | 수준·선수지식 | 내용·자료 형태 |
| --- | --- | --- | --- |
| 미적분·벡터미적분 | [MIT 18.02SC · 2010](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/) | 학부 기초<br>일변수 미적분 | 편미분·다중적분·벡터장·선적분과 면적분을 공부합니다. 영상·노트·문제 풀이 |
| 선형대수 | [MIT 18.06 · 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) | 학부 기초<br>연립방정식·기본 함수 | 벡터공간·직교·고유값을 회로·신호·제어의 수학으로 연결합니다. 영상·과제·시험 |
| 미분방정식·라플라스 변환 | [MIT 18.03SC · 2011](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/) | 학부 기초<br>미적분 | 회로와 동적 시스템에 쓰는 선형 미분방정식·라플라스 변환을 익힙니다. 영상·노트·문제 풀이 |
| 편미분방정식·푸리에 해석 | [Steve Brunton 공학수학](https://www.youtube.com/playlist?list=PLMrJAkhIeNNQromC4WswpU1krLOq5Ro6S) | 학부 심화~대학원<br>벡터미적분·미분방정식 | 공간과 시간에 따라 변하는 장·파동을 다루는 수학을 공부합니다. 공개 영상 |
| 확률·통계의 기초 | [MIT 6.041SC · 2013](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/) | 학부<br>미적분 | 확률변수·조건부확률·추론을 신호·통신·제어 공부의 바탕으로 익힙니다. 영상·문제 풀이·과제 |
| 수치해석·수치선형대수 | [MIT 18.335J · 2019](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/) | 대학원 입문<br>선형대수·미적분·프로그래밍 | 부동소수점·안정성·행렬 계산과 수치 오차를 다룹니다. 노트·과제 |
| 양자역학의 기초 | [MIT 8.04 · 2013](https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/) | 학부<br>미분방정식·파동·기초 역학 | 파동함수와 양자계의 기본 계산을 반도체·광전자 공부에 앞서 익힙니다. 영상·노트·과제 |
| 고체물리 | [MIT 8.231 · 2006](https://ocw.mit.edu/courses/8-231-physics-of-solids-i-fall-2006/) | 학부 심화<br>양자역학·통계물리 기초 | 고체의 양자이론을 공부하는 과목입니다. 참고 교재 목록·과제·학습 자료 |

## 회로이론·전자회로·집적회로

| 과목 | 강의·교재 | 수준·선수지식 | 내용·자료 형태 |
| --- | --- | --- | --- |
| 회로이론 | [김명식 회로이론](https://www.youtube.com/playlist?list=PLDxSDgt8OE1YC4qnsZgP_kEXKJ5iDRSeW) | 학부 · 한국어<br>미적분·복소수 | 소자·단위에서 노드·루프 해석과 과도응답으로 이어집니다. 공개 영상 |
| 회로와 전자공학 입문 | [MIT 6.002 · 2007](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/) | 학부<br>기초 물리·미분방정식 | 회로 모델·증폭·디지털 회로와 동적 응답을 강의·실습 자료로 공부합니다. 영상·노트·실습 안내·문제 |
| 전자회로·증폭기 | [박홍준 전자회로 1](https://www.youtube.com/playlist?list=PLfrHVUu0Cc3kFU9dbJq0SJjp8r7d9FKqu) | 학부 · 한국어<br>회로이론·기초 반도체 소자 | 트랜지스터 회로의 해석에서 증폭기 설계로 이어집니다. 공개 영상 |
| 고급 회로망·회로 합성 | [IIT Madras EE5383](https://www.ee.iitm.ac.in/videolectures/) | 학부 심화~대학원<br>회로망·라플라스 변환 | Advanced Electrical Networks 강의에서 회로망의 심화 해석을 공부합니다. 영상·대학 과목 목차 |
| 아날로그 집적회로 | [IIT Madras EE5320 · 2024](https://www.ee.iitm.ac.in/videolectures/) | 대학원<br>전자회로·소신호 모델·피드백 | Analog Integrated Circuit Design 강의로 소자 수준 해석에서 IC 설계로 이어갑니다. 영상·대학 과목 목차 |
| 능동 필터 | [IIT Madras EE5340](https://www.ee.iitm.ac.in/videolectures/) | 학부 심화~대학원<br>신호와 시스템·전자회로 | Active Filter Design 강의에서 필터 함수와 회로 구현을 연결합니다. 영상·대학 과목 목차 |
| ADC·DAC·혼합신호 회로 | [IIT Madras EE6580](https://www.ee.iitm.ac.in/videolectures/) | 대학원<br>전자회로·확률·신호처리 | VLSI Data Conversion Circuits를 선택해 데이터 변환 회로를 공부합니다. 대학 목차에서 NPTEL 영상 연결 |
| PLL·클록 회로 | [IIT Madras EE6324 · 2020](https://www.ee.iitm.ac.in/videolectures/) | 대학원<br>피드백·신호·전자회로 | Phase-Locked Loops 강의로 위상 동기 회로를 공부합니다. 영상·대학 과목 목차 |
| RF 집적회로 | [IIT Madras EE6320 · 2015](https://www.ee.iitm.ac.in/videolectures/) | 대학원<br>전자회로·잡음·고주파 해석 | RF Integrated Circuits 강의로 무선 송수신 회로 설계에 들어갑니다. 영상·대학 과목 목차 |

## 반도체·공정·광전자·마이크로시스템

| 과목 | 강의·교재 | 수준·선수지식 | 내용·자료 형태 |
| --- | --- | --- | --- |
| 반도체 물리·소자 | [Sungho Kim — 김성호](https://www.youtube.com/@devicephysics) | 학부 · 한국어<br>기초 물리·미적분·회로 | 에너지 밴드·캐리어·접합·MOS를 반도체 소자의 동작과 연결합니다. 공개 영상·과목별 재생목록 |
| 소자 모델과 전자회로 | [MIT 6.012 · 2009](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/) | 학부<br>회로·반도체 기초 | 접합·MOS·BJT의 물리와 대신호·소신호 회로 모델을 연결합니다. 노트·과제·시험 |
| 고급 반도체 소자 | [MIT 6.720J · 2007](https://ocw.mit.edu/courses/6-720j-integrated-microelectronic-devices-spring-2007/) | 대학원<br>반도체 물리·소자·미분방정식 | 캐리어 통계·수송·접합·MOS·단채널 효과를 공부합니다. 노트·과제·시험·프로젝트 |
| 나노 트랜지스터·수송 모델 | [nanoHUB MOSFET Essentials](https://www.youtube.com/watch?v=5eG6CvcEHJ8) | 학부 심화~대학원<br>반도체 물리·양자역학 기초 | Mark Lundstrom의 나노소자 강의에서 MOSFET과 수송 모델로 이어갑니다. 공개 영상·nanoHUB 후속 강의 |
| 반도체 공정·미세 제작 | [MIT 6.152J · 2005](https://ocw.mit.edu/courses/6-152j-micro-nano-processing-technology-fall-2005/) | 학부 심화<br>기초 화학·물리·반도체 소자 | 산화·확산·주입·증착·식각과 공정 흐름을 공부합니다. 노트·실습 안내·과제 |
| 광전자·레이저·광도파로 | [MIT 6.974 · 2006](https://ocw.mit.edu/courses/6-974-fundamentals-of-photonics-quantum-electronics-spring-2006/) | 대학원<br>전자기파·양자역학·미분방정식 | 광학계·공진기·광섬유·레이저와 빛과 물질의 상호작용을 공부합니다. 노트·시험 |
| MEMS·센서·액추에이터 | [MIT 6.777J · 2007](https://ocw.mit.edu/courses/6-777j-design-and-fabrication-of-microelectromechanical-devices-spring-2007/) | 대학원<br>미세공정·역학·회로 | 마이크로시스템의 재료·감지·구동·잡음과 설계 프로젝트를 다룹니다. 노트·문제·프로젝트 |
| 반도체·전자 시스템 패키징 | [NPTEL · IISc Bangalore](https://nptel.ac.in/courses/108108031) | 학부 심화~대학원<br>소자·재료·회로·기초 열전달 | 칩·보드·시스템 단계의 패키징, 조립과 시험을 공부합니다. 공식 강의 안내·[강의계획서](https://archive.nptel.ac.in/content/syllabus_pdf/108108031.pdf) |

## 전자기장·전파·고속 배선

| 과목 | 강의·교재 | 수준·선수지식 | 내용·자료 형태 |
| --- | --- | --- | --- |
| 전자기학 | [김동명 교수 전자기학](https://www.youtube.com/@Electro-Magnetic_Kim) | 학부 · 한국어<br>벡터미적분·기초 물리 | 전기장·자기장과 공간적 해석을 수식·응용으로 연결합니다. 공개 영상 |
| 전자기파·전송선·복사 | [MIT 6.013 · 2009](https://ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/) | 학부<br>벡터미적분·회로 | 맥스웰 방정식·도파·복사와 통신·센서 응용을 공부합니다. 교재·노트·시연·문제 |
| 고급 전자기장·전자기 에너지 변환 | [MIT 6.641 · 2005](https://ocw.mit.edu/courses/6-641-electromagnetic-fields-forces-and-motion-spring-2005/) | 대학원<br>전자기학·미분방정식 | 장과 물질의 경계 문제, 힘·에너지·전자기계의 모델을 다룹니다. 노트·문제·시험 |
| 안테나·전파·위성통신 | [Greg Durgin 강의](https://www.youtube.com/@profdurgin) | 학부 전공~대학원<br>전자기파·회로·통신 | Electromagnetics와 Satellite Communications의 과목별 목록으로 전파·안테나·위성 링크를 공부합니다. 공개 영상·[ECE6390 계획서](https://syllabus.gatech.edu/sites/default/files/2026-04/ECE6390_Syllabus_0.pdf) |
| 수치 전자기학·FDTD | [WSU John B. Schneider — Understanding the FDTD Method](https://eecs.wsu.edu/~schneidj/ufdtd/) | 학부 심화~대학원<br>맥스웰 방정식·수치해석·C | 시간과 공간을 나누어 전자기장을 계산하는 방법을 교재와 C 예제로 익힙니다. 저자 공개 교재·C 코드 |
| 신호 무결성·EMC·고속 PCB | [Eric Bogatin 강의와 측정](https://www.colorado.edu/faculty/bogatin/youtube-videos) | 학부 심화·설계 실습<br>회로·전자기학·전송선 | 리턴 전류·반사·누화와 PCB 배선을 계측 사례로 연결합니다. 교수의 공개 영상 목차·[PCB 설계 채널](전기전자통신유튜브_electrical-engineering-youtube.md) |

## 신호처리·통신·정보이론

| 과목 | 강의·교재 | 수준·선수지식 | 내용·자료 형태 |
| --- | --- | --- | --- |
| 신호와 시스템 | [소클래스TV](https://www.youtube.com/playlist?list=PLvjZBINYJc2aLpbT8L6_8X2C79OovqGym) | 학부 · 한국어<br>미적분·복소수·선형대수 | 스펙트럼·샘플링·필터의 바탕을 공부합니다. 공개 영상 |
| 연속·이산 신호의 해석 | [MIT 6.003 · 2011](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/) | 학부<br>미적분·미분방정식 | 합성곱·푸리에·라플라스·z 변환과 LTI 시스템을 다룹니다. 영상·노트·과제 |
| 디지털 신호처리 | [MIT RES.6-008 · 2011 공개판](https://ocw.mit.edu/courses/res-6-008-digital-signal-processing-spring-2011/) | 대학원 수준 기초<br>신호와 시스템·이산시간 변환 | 이산시간 신호와 필터의 기본 해석·구현 방법을 공부합니다. 영상·노트·문제 |
| 확률과정·대기행렬 | [MIT 6.262 · 2011](https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/) | 대학원<br>확률·미적분 | 마르코프·포아송·갱신 과정 등 시간에 따라 변하는 확률 모형을 다룹니다. 영상·교재·문제 |
| 통신·신호의 검출과 추정 | [MIT 6.011 · 2010](https://ocw.mit.edu/courses/6-011-introduction-to-communication-control-and-signal-processing-spring-2010/) | 학부 심화<br>선형시스템·확률 | 상태 관측·상관·전력스펙트럼·최소제곱 추정·Wiener 필터를 공부합니다. 공개 교재·시험 |
| 디지털 통신 | [MIT 6.450 · 2006](https://ocw.mit.edu/courses/6-450-principles-of-digital-communications-i-fall-2006/) | 대학원<br>확률·선형대수·신호와 시스템 | 양자화·표본화·PAM/QAM·신호공간·검출을 연결합니다. 영상·노트·문제 |
| 무선통신·페이딩·다중 안테나 | [Stanford EE359 · 2020](https://web.stanford.edu/class/ee359/) | 대학원<br>디지털 통신·확률·선형대수 | 무선 채널과 통신 시스템의 성능·설계 기법을 공부합니다. 슬라이드·강의 자료·과제 |
| 정보이론·소스 및 채널 부호화 | [MIT 6.441 · 2016](https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/) | 대학원<br>확률·통계·증명 | 엔트로피·무손실/손실 압축·가설검정·채널 부호화를 공부합니다. 노트·문제 |
| 광대역 통신 회로 | [IIT Madras EE6322 · 2024](https://www.ee.iitm.ac.in/videolectures/) | 대학원<br>아날로그 IC·신호·고주파 회로 | VLSI Broadband Communication Circuits에서 통신 이론을 회로 구현과 연결합니다. 대학 목차의 EE6322w 영상 |

## 제어·추정·로봇

| 과목 | 강의·교재 | 수준·선수지식 | 내용·자료 형태 |
| --- | --- | --- | --- |
| 고전 제어·피드백 | [김동한 자동제어](https://www.youtube.com/playlist?list=PLP4rlEcTzeFL3DTMN2xaRt_iMyoqSiTjA) | 학부 · 한국어<br>미분방정식·라플라스 변환 | 동적 시스템과 피드백 제어를 대학 수업 순서로 공부합니다. 공개 영상 |
| 상태공간·선형 제어 | [Steve Brunton Control Bootcamp](https://www.youtube.com/playlist?list=PLMrJAkhIeNNR20Mz-VpzgfQs5zrYi085m) | 학부 심화~대학원<br>선형대수·미분방정식 | 상태공간에서 시스템 응답과 제어 설계로 이어갑니다. 공개 영상 |
| 고급 동적 시스템·안정성 | [MIT 6.241J · 2011](https://ocw.mit.edu/courses/6-241j-dynamic-systems-and-control-spring-2011/) | 대학원<br>선형시스템·행렬·피드백 | 동적 시스템의 응답·상호연결·안정성과 제어 설계를 다룹니다. 교재·노트·문제 |
| 비선형·최적 제어·궤적 최적화 | [MIT Underactuated Robotics](https://underactuated.mit.edu/) | 대학원<br>동역학·선형제어·최적화 | 진자·보행·비행 모형에서 비선형 동역학·안정성·최적 제어를 공부합니다. 교재·영상·계산 예제 |
| 로봇 기구학·동역학·경로 계획 | [Northwestern Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) | 학부 심화~대학원<br>선형대수·역학·프로그래밍 | 강체 운동에서 로봇의 기구학·동역학·계획·제어로 이어갑니다. 저자 교재 공개본·영상·코드 |

## 전력·전기기기·산업 제어

| 과목 | 강의·교재 | 수준·선수지식 | 내용·자료 형태 |
| --- | --- | --- | --- |
| 전력계통·교류 전력 해석 | [MIT 6.061 · 2011](https://ocw.mit.edu/courses/6-061-introduction-to-electric-power-systems-spring-2011/) | 학부<br>교류 회로·복소수 | 전력망·다상 회로·전기 에너지 변환의 바탕을 공부합니다. 공개 교재·문제·시험 |
| 전기기기·전자기계 | [MIT 6.685 · 2013](https://ocw.mit.edu/courses/6-685-electric-machines-fall-2013/) | 대학원<br>전력 기초·전자기학 | 모터·발전기 등 전기기계의 특성과 시스템 상호작용을 해석합니다. 노트·과제·시험 |
| 전력전자·전력변환 제어 | [MIT 6.622 · 2023](https://ocw.mit.edu/courses/6-622-power-electronics-spring-2023/) | 대학원<br>회로·전자회로·제어 | 전력변환 회로의 모델·분석·설계·제어를 공부합니다. 영상·노트·설계 과제 |
| 스위칭 전원·컨버터 안정성 | [byungcho choi](https://www.youtube.com/@byungchochoi3322) | 학부 심화~대학원 · 영어 중심<br>전력전자·피드백 | PWM 컨버터의 평균·소신호 모델과 루프 이득·안정성으로 이어집니다. 공개 영상·EE ClassRoom 과목 안내 |
| 전력계통 보호·고장 해석 | [NPTEL Power System Protection](https://nptel.ac.in/courses/108101039) | 학부 심화~대학원<br>전력계통·대칭좌표·계측 | 보호 원리·계기용 변성기·과전류 및 방향성 보호를 공부합니다. 공식 과목의 강의 목록 |
| 고전압 공학 | [NPTEL High Voltage Engineering](https://nptel.ac.in/courses/108104048) | 학부 심화~대학원<br>전자기학·회로·전력 | IIT Kanpur의 Ravindra Arora 강의로 고전압 분야를 공부합니다. 공식 과목 안내·강의 자료 |
| 모터 제어·전력 시스템 시뮬레이션 | [MATLAB Korea](https://www.youtube.com/@MATLABKorea) | 학부 실습~심화 · 한국어·자막<br>회로·제어·모델링 | 모터와 전력전자 모델을 MATLAB/Simulink 예제로 연결합니다. 공개 영상·도구 라이선스 별도 |
| 시퀀스·PLC·자동화 | [전병칠 PLC 제어](https://www.youtube.com/playlist?list=PLt-9xySRVAc2kOWnrObkEAGXO5e6lrk12) | 실습 입문 · 한국어<br>전기 기초·접점·타이머 | 릴레이·인터록에서 PLC의 동작 순서와 제어로 이어갑니다. 공개 영상 |

## 디지털 하드웨어·임베디드·계측

| 과목 | 강의·교재 | 수준·선수지식 | 내용·자료 형태 |
| --- | --- | --- | --- |
| 논리회로·명령어·프로세서 | [MIT 6.004 · 2017](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | 학부<br>프로그래밍·이진수 | 디지털 논리에서 명령어·프로세서·메모리로 이어지는 구조를 공부합니다. 영상·노트·문제 |
| 마이크로프로세서·주변장치 | [김동한 STM32](https://www.youtube.com/playlist?list=PLP4rlEcTzeFLg8p8HCbGdcYFHPQHNvjcq) | 학부 실습 · 한국어<br>C·논리회로·기초 회로 | MCU의 동작을 보드와 주변장치 제어로 연결합니다. 공개 영상 |
| 임베디드 시스템·실시간 운영체제 | [UT Austin Jonathan Valvano 강의 자료](https://users.ece.utexas.edu/~valvano/) | 학부 심화·실습<br>C·컴퓨터구조·인터럽트 | 공식 페이지의 ECE445L·ECE445M 자료에서 입출력·동기화·스케줄링·실시간 디버깅을 공부합니다. 강의·실습 자료·소프트웨어, 교재·보드 별도 |
| FPGA·HDL·하드웨어 구현 | [Nandland FPGA-101](https://nandland.com/fpga-101/) | 학부·설계 입문<br>논리회로 | Verilog/VHDL의 하드웨어 기술과 FPGA 구현을 익힙니다. 공개 글·영상·예제 |
| 설계 검증·SystemVerilog·UVM | [KK SystemVerilog](https://www.youtube.com/playlist?list=PL8NoqZRUC7hfc5GP8ugqKWK88MP1J_yst) | 학부 심화·실무<br>Verilog·동기식 논리회로 | 검증 언어에서 UVM 테스트벤치·디버깅으로 이어집니다. 공개 영상, VCS·Verdi 실습 환경 별도 |
| IC 설계·시험 | [IIT Madras EE6326 · 2024](https://www.ee.iitm.ac.in/videolectures/) | 대학원<br>논리회로·전자회로·디지털 IC | IC Design and Testing 강의에서 회로 설계와 시험을 함께 공부합니다. 영상·대학 과목 목차 |
| 계측·RF 측정·PCB 실험 | [전기전자 설계·계측 채널](전기전자통신유튜브_electrical-engineering-youtube.md) | 학부 실험~설계 실무<br>회로·신호·장비 기본 조작 | w2aew·Keysight·R&S의 계측 기초와 Bogatin·Feranec의 PCB 측정을 골라 볼 수 있습니다. 주제별 영상·제조사 기술 강의 |

## 생체 신호와 영상

| 과목 | 강의·교재 | 수준·선수지식 | 내용·자료 형태 |
| --- | --- | --- | --- |
| 생체신호처리·의료영상 | [MIT HST.582J · 2007](https://ocw.mit.edu/courses/hst-582j-biomedical-signal-and-image-processing-spring-2007/) | 대학원<br>DSP·확률·선형대수·기초 생리학 | 생체 데이터의 수집·필터링·특징 추출·영상 처리를 심장·음성·의료영상 예제와 연결합니다. 노트·MATLAB 실습 안내·과제 |

## 연결해서 공부할 분야

고체물리·양자 소자·광통신·생체계측·영상처리·AI 가속기 등은 전기전자와 다른 전공이 만나는 분야입니다. 세부 과목은 아래 교육과정의 전공 분류에서 찾고, [컴퓨터공학·AI 과목](컴퓨터공학과AI과목_cs-ai-courses.md)의 구조·병렬처리·로보틱스·비전·머신러닝 자료와 연결해 공부하실 수 있습니다. 논문 세미나와 연구 과목은 관심 분야의 교재·강의를 익힌 뒤 연구실의 공개 강연과 논문으로 이어가시면 좋습니다.

## 공식 교육과정과 전공 분류

- [서울대학교 전기·정보공학부 학부 교과과정](https://ece.snu.ac.kr/academics/undergraduate/curriculum): 전기에너지·통신·제어·반도체·전자물리·컴퓨터 분야의 과목 연결입니다.
- [서울대학교 전기·정보공학부 대학원 교과과정](https://ece.snu.ac.kr/academics/graduate/curriculum): 소자·공정·회로·전자기·광전자·통신·제어·컴퓨터·생체 분야를 찾아볼 수 있습니다.
- [Georgia Tech ECE 2026–2027 과목 목록](https://catalog.gatech.edu/coursesaz/ece/): 학부와 대학원 전공 과목 설명입니다.
- [MIT EECS 박사자격 평가 과목표 · 2026 봄](https://www.eecs.mit.edu/wp-content/uploads/2026/01/TQE-Grid-effective-spring-2026.pdf): 시스템·이론·AI·제어·회로·통신·생체·전자기·물리 분야를 나누어 제시합니다.
- [IIT Madras 집적회로·시스템 공개 강의 목차](https://www.ee.iitm.ac.in/videolectures/): 회로망·아날로그 IC·RFIC·PLL·데이터 변환·IC 시험의 학년도별 영상 연결입니다.

확인 기준: 2026-10-22~23. 각 행에서 공개 영상·교재·강의노트·실습 안내를 구분했습니다.
