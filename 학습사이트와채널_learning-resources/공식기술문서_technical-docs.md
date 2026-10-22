# 개발·회로·펌웨어 학습 | Official technical learning resources

[학습 사이트와 채널](README.md) · [국내 공개 강의](국내공개강의_korean-courses.md) · [해외 영상 해설](해외유튜브_global-youtube.md)

설명만 읽고 끝내기보다 예제를 실행하거나 회로·장치의 동작을 확인할 때 쓰기 좋은 자료입니다. 한국어 문서에서도 아직 번역되지 않은 절은 영어로 열릴 수 있습니다.

## 한국어로 시작하는 프로그래밍과 도구

| 자료·운영 주체 | 다루는 내용 | 시작 방법·이용 조건 |
| --- | --- | --- |
| [Python 한국어 자습서](https://docs.python.org/ko/3/tutorial/) — Python 문서 프로젝트 | 제어문, 함수, 자료구조, 모듈과 예외를 예제로 설명합니다. | 무료 문서. 프로그래밍 기초를 아는 독자에게 적합하며, 코딩 자체가 처음이면 [CS50P](https://cs50.harvard.edu/python/)부터 시작할 수 있습니다. |
| [MDN 웹 개발 학습](https://developer.mozilla.org/ko/docs/Learn_web_development) — MDN·Mozilla와 기여자 | HTML·CSS·JavaScript와 웹 페이지 구성 과정을 설명합니다. | 무료 문서. 한국어 진입점에 영문 단원도 함께 있습니다. |
| [Pro Git 한국어판](https://git-scm.com/book/ko/v2) — Scott Chacon·Ben Straub, 번역 기여자 | 버전 관리, 커밋, 브랜치와 원격 협업을 다룹니다. | Git 공식 사이트에서 읽는 공개 도서. 1~3장의 예제를 별도 연습 저장소에서 따라가시면 좋습니다. |
| [Microsoft Learn](https://learn.microsoft.com/ko-kr/training/) — Microsoft | 제품·역할별 학습 경로와 실습 모듈을 제공합니다. | 한국어 검색·안내. 모듈의 사전 지식과 실습에 필요한 계정을 확인합니다. |
| [MATLAB Onramp](https://matlabacademy.mathworks.com/kr/details/matlab-onramp/gettingstarted) — MathWorks | 배열·인덱싱·그래프·조건문을 브라우저 실습으로 익힙니다. | 한국어. MathWorks 계정으로 무료 수강하며, 다른 심화 과정의 구독 조건과 구분합니다. [이용 FAQ](https://kr.mathworks.com/learn/training/online-courses-faq.html) |

## 머신러닝과 AI 구현

| 자료·운영 주체 | 다루는 내용 | 시작 방법·이용 조건 |
| --- | --- | --- |
| [머신러닝 단기집중과정](https://developers.google.com/machine-learning/crash-course?hl=ko) — Google | 회귀·분류·손실·일반화를 애니메이션, 시각화와 실습으로 연결합니다. | 한국어 본문. 처음이라면 선형 회귀부터 과정 순서대로 읽습니다. |
| [Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) — PyTorch | 텐서, 데이터 로더, 모델, 자동 미분과 학습·저장을 한 흐름으로 설명합니다. | 영어. Python과 딥러닝 기초를 전제로 하며, 공개 노트북을 Colab 또는 로컬에서 실행할 수 있습니다. |

## 회로·계측·펌웨어·FPGA

제조사 강의는 실제 부품과 도구의 사용법을 배우기에 좋습니다. 특정 제품에서 설명한 설정·성능을 다른 부품에 적용할 때에는 해당 데이터시트를 다시 확인합니다.

| 자료·운영 주체 | 다루는 내용 | 시작 방법·이용 조건 |
| --- | --- | --- |
| [TI Precision Labs](https://www.ti.com/video/series/precision-labs.html) — Texas Instruments | 연산증폭기, ADC·DAC, 센서, 클록과 통신 인터페이스를 영상·참고 자료로 설명합니다. | 영어 중심. Amplifiers나 Data converters의 기초부터 보기 좋습니다. |
| [Engineering University Program](https://wiki.analog.com/university) — Analog Devices | 회로·전자·전력·통신의 강의 자료와 실험 절차를 제공합니다. | 영어. 이론 자료는 공개이며, ADALM 기반 실습에는 지정 장비·부품이 필요합니다. |
| [STM32 online courses](https://community.st.com/stm32-online-courses-173) — STMicroelectronics | STM32 도구, FreeRTOS, USB, 무선 통신과 엣지 AI를 다룹니다. | 영어 중심. [MOOC 안내](https://www.st.com/content/st_com/en/support/learning/stm32-moocs.html)에서 무료 강좌와 실습 장비 조건을 확인합니다. |
| [Intro to Digital Logic and FPGAs](https://digilent.com/shop/intro-to-digital-logic-and-fpgas/) — Digilent | 논리 게이트·진리표·동기 회로에서 FPGA 기초로 이어집니다. | 영어. 페이지의 Lesson 순서로 영상을 열며, 실제 보드 실습 비용은 별도입니다. |

## 자료를 함께 쓰는 예

연산증폭기의 피드백이 낯설다면 대학 회로 강의에서 식을 배우고 TI 강의에서 대역폭·안정도와 실제 부품의 제약을 확인할 수 있습니다. STM32를 공부할 때에는 강좌에서 사용한 칩과 보드 이름을 먼저 적어 두면, 자신의 보드에서 핀·메모리·주변장치 설정이 다른 이유를 찾기 쉽습니다.

확인일: 2026-10-22. 링크된 공식 문서의 목차·과정 소개·이용 안내를 기준으로 정리했습니다.
