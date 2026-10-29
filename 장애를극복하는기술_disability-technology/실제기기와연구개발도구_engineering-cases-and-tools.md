# 장애 보조기기와 재활 연구의 실제 제품·개발 도구 | Assistive devices and rehabilitation engineering

이 글은 장애 유형별 문서의 개요를 실제 기기와 연구 흐름으로 연결합니다. 의지와 외골격, 시각·청각 접근 기술, 의사소통 장치, 투석·심장·호흡 보조기기, 센서와 소프트웨어의 구성, 개발 도구와 검증 방법을 함께 살펴봅니다.

제품을 소개할 때는 제조사 설명, 규제기관의 허가·사용 범위, 임상 연구의 결과를 따로 확인합니다. 연구 논문에서 가능한 동작을 보였더라도 일상용 제품과 같다고 보지 않습니다. FDA의 510(k) ‘실질적 동등성’ 결정도 특정 제품의 미국 내 시판 경로와 표시된 사용 범위에 관한 결정이며, 모든 사용자에게 효과가 있거나 한국에서 같은 허가·판매 상태라는 뜻은 아닙니다.

## 목차

- [보조기기 개발은 사용자 과제에서 시작합니다](#engineering-process)
- [지체장애: 의지·보행 외골격·신경 신호 연결](#limb-mobility)
- [뇌병변장애: 기능적 전기자극과 운동 재활](#neurological-motor)
- [시각장애: 화면 접근성과 장면 인식](#vision-access)
- [청각장애: 인공와우의 소리 신호 경로](#hearing-access)
- [언어장애: 시선 입력 AAC와 음성 신경보철 연구](#communication)
- [안면장애: 영상에서 맞춤 보철까지](#facial-rehabilitation)
- [신장장애: 가정 투석과 인공신장 연구](#kidney-support)
- [심장장애: 리드리스 심박조율기와 심실보조장치](#cardiac-support)
- [간장애: 체외 간 보조와 임상시험](#liver-support)
- [호흡기장애: 환기 장치의 제어와 안전 사례](#respiratory-support)
- [장루·요루장애: 보호판 아래 누출 감지](#ostomy-care)
- [뇌전증장애: 발작 알림과 반응성 신경자극](#epilepsy)
- [췌장장애: 연속혈당측정과 자동 인슐린 전달](#glucose-control)
- [연구·개발에서 실제 쓰이는 도구](#engineering-tools)
- [검증 계획과 고장 분석](#verification)
- [출처와 자료의 범위](#sources)

<a id="engineering-process"></a>
## 보조기기 개발은 사용자 과제에서 시작합니다

보조기기와 의료기기는 센서나 AI 모델 하나로 완성되지 않습니다. 사용자가 하려는 일과 장소를 정하고, 몸에 닿는 구조와 입력 신호, 전자회로, 펌웨어·앱, 출력 장치, 교육·유지관리까지 하나의 시스템으로 설계합니다.

```text
사용자 목표와 사용 환경
        ↓
요구사항·위험 분석
        ↓
기계 구조·센서·전극·유체 회로
        ↓
신호 처리·펌웨어·제어 알고리즘·사용자 인터페이스
        ↓
모터·전기 자극·음성·화면·약물 전달
        ↓
시험 장비를 이용한 벤치 검증
        ↓
사용성·임상 평가와 장기 유지관리
```

예를 들어 보행 보조기기는 보행 의도나 발의 움직임을 감지하고, 신호 지연을 고려해 모터 또는 전기 자극을 동작시킵니다. 시각 접근 앱은 카메라 영상에서 글자·물체를 추정해 음성으로 읽어 줍니다. 인슐린 전달 장치는 연속혈당 센서 입력과 사용자의 식사 알림을 바탕으로 펌프 명령을 계산합니다. 이들 기능은 모두 ‘센서 입력 → 판단 → 출력’의 형태를 갖지만, 위험도와 허용 가능한 오차는 크게 다릅니다.

AI가 모든 보조기기에 들어가는 것은 아닙니다. 정해진 파형 처리, 임계값, 상태기계, PID·모델 기반 제어처럼 검증 가능한 규칙을 쓰는 제품도 많습니다. AI를 쓴다면 학습 데이터와 평가 대상, 오검출, 다른 사용자·환경에서의 성능 저하를 별도로 확인해야 합니다. 제조사가 공개하지 않은 모델 구조나 개발 언어는 추정하지 않습니다.

## 설계에서 확인할 공학 항목

| 계층 | 실제로 결정하는 것 | 확인할 실패 예 |
|---|---|---|
| 사용자 과제 | 무엇을 돕고 어디에서 사용하는지, 혼자 쓰는지 | 제품은 작동하지만 사용자가 착용·충전·세척하기 어려움 |
| 기계·재료 | 무게, 관절축, 착용부, 피부 접촉 재료, 밀폐·방수 | 압박, 미끄러짐, 피부 손상, 재료 변형 |
| 센서·아날로그 회로 | 측정량, 대역폭, 잡음, 샘플링, 전극 접촉 | 움직임 잡음을 실제 생체 신호로 오인 |
| 펌웨어·제어 | 상태 전이, 지연, 출력 상한, 통신·배터리 고장 처리 | 끊긴 센서값을 정상값처럼 계속 사용 |
| 앱·AI | 인식·경보·설정·데이터 전송 | 오경보, 누락, 접근성 부족, 개인정보 노출 |
| 검증·임상 | 요구사항별 시험, 사용성, 임상 결과, 장기 안전 | 실험실 성능을 일상 효과로 확대 해석 |
| 운영·수리 | 부품·소모품, 교육, 업데이트, 긴급 대체 | 소모품이나 수리 경로가 없어 보조 기능 중단 |

의료기기 소프트웨어는 요구사항, 위험, 시험 결과가 서로 추적되도록 관리해야 합니다. FDA의 소프트웨어 검증 지침은 의료기기 소프트웨어뿐 아니라 의료기기의 설계·개발·제조에 쓰는 소프트웨어의 검증 원칙을 설명합니다. 위험관리 표준은 위험을 찾아 줄이고 남은 위험을 다루는 틀을 제공합니다. 이는 아래 사례별 시험을 대신하는 만능 체크리스트가 아니라 개발 기록을 일관되게 만드는 기준입니다.

<a id="limb-mobility"></a>
## 지체장애: 의지·보행 외골격·신경 신호 연결

### C-Leg: 보행 상태에 맞춰 무릎 저항을 바꾸는 의지

Ottobock의 C-Leg는 무릎 관절 의지 안에 관절각 센서, 가속도계·자이로스코프, 마이크로프로세서, 유압 장치를 둡니다. 센서로 무릎과 하퇴의 움직임을 읽고, 제어기가 보행 주기와 상황을 추정한 뒤 유압 저항을 조절합니다. 제조사 전문가 안내서는 센서 정보가 초당 100회 갱신·평가된다고 밝히며, 배터리 부족·고장 때의 안전 모드도 설명합니다. 보행 속도 하나만 읽는 장치가 아니라 입각기와 유각기, 앉기·서기, 경사 등 서로 다른 상황에서 무릎이 접히거나 펴지는 속도를 조정하는 시스템입니다. ([Ottobock 사용 및 전문가 안내서](https://spa-prod-commerce.cep.ottobock.com/medias/C-Leg4Update-InstructionsforProfessionals-English-7-2024.pdf?attachment=true&context=bWFzdGVyfHJvb3R8MzQ2NjA5NnxhcHBsaWNhdGlvbi9wZGZ8aDZkL2g4OC85Mzk3MDgxNDQwMjg2LnBkZnwwZDEzYTkzODI1YzlhZjUwYTVjZTRmODdkOWQ4OTlmMjJiYTE0MmEwNDBjYjUxN2ZmYTM0NDVmOTZjODBiZDVi)

보장구 전문가는 C-Soft Plus 설정 소프트웨어로 장치 설정과 정렬을 조정합니다. 제조사 안내서는 설정 절차를 단계별로 안내하고, 설정을 저장·출력해 기록할 수 있다고 설명합니다. 조정 결과를 확인할 때는 평지 보행뿐 아니라 경사·계단·의자에서 일어나기, 속도 변화, 배터리 저하 때의 동작을 사용자의 안전 조건에 맞춰 살펴야 합니다.

### Hero Arm: 근전도 입력을 손가락 모터로 연결하는 의지

Open Bionics의 Hero Arm은 잔존 근육에서 발생하는 근전도(EMG) 신호를 전극으로 읽고, 사용자가 선택한 손 동작을 여러 모터로 구현하는 다관절 상지 의지입니다. 제조사 사용자 안내에 따르면 손 크기에 따라 3모터 또는 4모터 손 구성이 있으며, 4모터 구성은 검지와 중지를 독립적으로 움직일 수 있습니다. 소켓은 잔존 사지의 3D 스캔을 바탕으로 개인별 설계·출력합니다. 따라서 실제 성능은 근전도 전극의 위치와 피부 접촉, 소켓 압력, 사용자 훈련, 배터리와 기계적 정비에 좌우됩니다. ([Open Bionics 사용자 안내](https://openbionics.com/en/hero-arm-user-guide/))

공학적으로는 EMG 전처리와 동작 분류가 불안정할 때 손이 의도치 않게 움직이지 않도록 해야 합니다. 사용 설명서는 배터리가 방전되면 기기가 멈출 수 있고 물에 잠기도록 설계되지 않았음을 명시합니다. 공개된 사용자 문서에는 개발 언어나 내부 분류 모델이 적혀 있지 않으므로, 특정 AI 프레임워크를 사용한다고 단정하지 않습니다.

### ReWalk 7: 착용형 보행 외골격

Lifeward의 ReWalk 7은 다리와 몸통 일부에 착용하는 배터리 구동형 외골격입니다. FDA 510(k) 문서에는 손목 무선 제어기, 목발 장착 제어기, 몸통 기울기 센서, 엉덩이·무릎 관절의 모터와 기어가 기재되어 있습니다. FDA 문서상 사용 범위는 T7–L5 척수손상 사용자의 가정·지역사회 보행(인증된 동반자 감독 및 평가·훈련 프로그램 포함), T4–T6 사용자의 재활기관 보행으로 구분됩니다. ([FDA 510(k) K241822 요약](https://www.accessdata.fda.gov/cdrh_docs/pdf24/K241822.pdf)) 따라서 ‘척수손상이 있으면 누구나 혼자 걸을 수 있다’는 설명은 FDA 문서와 다릅니다.

실제 시스템에서는 사용자 평가와 훈련을 마친 사람이 제어 입력을 주고, 착용부의 관절 구동기가 보행 동작을 보조합니다. 핵심 검증 항목은 넘어짐 위험, 관절 정렬, 보행 시작·정지, 계단·경사 사용 범위, 비상 정지, 배터리·통신 고장 때의 상태입니다. 임상 효과와 사용성은 해당 사용 조건의 연구 자료로 따로 평가해야 합니다.

### 뇌 신호와 척수 자극을 연결하는 연구

2023년 Nature 논문은 만성 척수손상 참여자 한 명에게 뇌 신호 측정과 척수 전기자극을 연결한 뇌-척수 인터페이스를 보고했습니다. 뇌 피질 신호에서 걷기 의도를 해독하고, 외부 처리 장치가 척수의 경막외 자극 시점과 패턴으로 변환해 다리 근육의 운동을 돕는 구조입니다. 참가자는 재활 훈련과 함께 장치를 이용했으며, 연구진은 실험실 밖 보행도 보고했습니다. 이 결과는 제품이 아니라 단일 참가자 기반의 임상 개념 증명입니다. 다음 연구에는 더 많은 손상 유형과 사람, 장기 이식 안정성, 무선화, 자극과 자연 감각의 통합, 장치 유지관리 평가가 필요합니다. ([Nature 원논문](https://www.nature.com/articles/s41586-023-06094-5))

<a id="neurological-motor"></a>
## 뇌병변장애: 기능적 전기자극과 운동 재활

Bioness L300 Go는 발처짐이나 일부 하지 근력 저하를 돕는 기능적 전기자극(FES) 시스템의 예입니다. 피부 전극이 말초신경·근육을 자극해 발목을 들어 올리거나, 적응증에 해당하는 성인의 무릎 굴곡·신전을 돕습니다. 이 방식은 마비된 근육을 로봇처럼 외부에서 움직이는 것이 아니라, 자극할 신경과 근육의 반응이 남아 있을 때 보행 과제의 특정 시점에 전기 펄스를 전달합니다. ([Bioness 사용 안내](https://www.bionessuniversity.com/documents/L300Go%20User%27s%20Guide%20Rev.%20E%20%5Befile%5D.pdf), [제조사 사용 목적 자료](https://bionessrehab.com/wp-content/uploads/2022/02/03785_productbrochure.pdf))

재활 로봇 연구에서는 관절 위치, 힘, 보행 속도, 근전도, 균형을 측정해 과제 난이도를 조정합니다. Stanford의 OpenSim은 근골격 모델을 이용해 동작을 시뮬레이션하고, OpenSense는 IMU 관성 센서 자료로 움직임을 추정하며, Moco는 동작 궤적·근육 사용 등의 최적화 문제를 다룹니다. 이 도구들은 임상 판단을 대체하지 않고, 모델의 가정과 환자별 몸의 차이를 검토하는 연구 도구입니다. ([Stanford OpenSim](https://opensim.stanford.edu/), [Mobilize Center 도구 목록](https://mobilize.stanford.edu/software/))

로봇 제어 연구의 공개 사례는 SolidWorks에서 설계한 6자유도 상지 재활 로봇을 Gazebo와 ROS 시뮬레이션에 연결하고, MATLAB/Simulink에서 운동학과 제어기를 평가합니다. 2025년 IEEE 학회 논문은 시뮬레이션과 제어 설계 연구이며, 환자 임상시험이나 치료 효과 평가가 아닙니다. 2026년 공개된 RehabBot 연구 환경은 MuJoCo 물리 시뮬레이터와 UR5e 협동로봇 모델, 관절형 사람 모델을 이용해 상·하지 재활 동작을 강화학습으로 연구하도록 구성했습니다. 이 역시 가상 환경에서 학습·평가하는 연구 도구이지, 재활 로봇 제품이나 환자 대상 효과를 입증한 임상 결과가 아닙니다. ([IEEE 공동시뮬레이션 논문](https://ieeexplore.ieee.org/abstract/document/11142188), [RehabBot, SoftwareX (2026)](https://doi.org/10.1016/j.softx.2026.102800))

<a id="vision-access"></a>
## 시각장애: 화면 접근성과 장면 인식

Apple VoiceOver는 화면 요소를 음성이나 점자 장치로 전달하고, 사용자가 제스처·키보드·점자 입력으로 앱과 운영체제를 조작하도록 지원하는 접근성 기능입니다. 화면의 버튼과 텍스트에 접근성 레이블을 제공하는 것은 앱 개발자가 구현해야 하며, 누락되거나 모호한 레이블은 화면 읽기만으로 해결할 수 없는 접근성 결함입니다. 따라서 운영체제 기능과 앱의 접근성 설계가 함께 작동해야 합니다. ([Apple 접근성 안내](https://www.apple.com/accessibility/), [Apple 개발자 VoiceOver 문서](https://developer.apple.com/documentation/accessibility/voiceover/))

Microsoft Seeing AI는 카메라로 촬영한 글자·제품·사람·장면을 분석해 음성 설명을 제공하는 모바일 앱입니다. 내부 알고리즘은 제조사의 서비스로 제공되며, 공개 사용자 설명서는 모든 장면 인식 결과가 정답이라고 보장하지 않습니다. 연구·개발 관점에서는 광학문자인식(OCR), 이미지 분류·객체 인식, 장면 설명, 음성 출력, 카메라 프레임 선택, 지연·배터리·개인정보 처리가 연결됩니다. 안전한 길 찾기처럼 결과 오류가 즉시 위험으로 이어지는 과제를 맡기려면 별도 센서, 보행 안내 체계, 사용자 연구와 안전 검증이 필요합니다. ([Microsoft Seeing AI 사용자 안내서](https://www.microsoft.com/en-us/garage/wp-content/uploads/2025/04/Seeing-AI-User-Manual.pdf))

현행 접근성 기술은 화면 확대·고대비·음성·점자·광학문자인식처럼 기능에 따라 조합할 수 있습니다. AI 시각 보조 연구는 실시간 장면 설명과 문서·물체 인식을 확장하고 있지만, 학습 자료에 드문 물체, 저조도, 역광, 언어별 글꼴, 카메라 흔들림에서의 오류를 시험해야 합니다. 시각 보조 앱의 결과를 의료 진단이나 완전한 자율 이동으로 소개하지 않습니다.

<a id="hearing-access"></a>
## 청각장애: 인공와우의 소리 신호 경로

Cochlear Nucleus 8은 외부 음향 처리기와 피부 아래 이식부가 무선으로 연결되는 인공와우 시스템의 한 제품입니다. 외부 마이크가 소리를 받고, 디지털 신호처리기가 주파수 대역별 정보를 전극 자극 패턴으로 인코딩합니다. 송신 코일은 피부를 사이에 두고 이식된 수신부로 전력과 신호를 전달하며, 달팽이관 전극이 청신경을 자극합니다. 이는 손상된 유모세포를 우회하는 방식이며, 자연 청력의 모든 세부 정보를 그대로 복구하는 장치는 아닙니다. ([Cochlear Nucleus 8 기술 사양](https://assets.cochlear.com/api/public/content/FUN4812-Nucleus-8-Tech-Specs-Sheet.pdf), [NIDCD 인공와우 설명](https://www.nidcd.nih.gov/health/cochlear-implants))

제조사의 Nucleus 8 사양 자료는 이중 마이크, telecoil, 무선 연결과 처리기 사양을 설명하고, Custom Sound 7.0 이상 또는 Custom Sound Pro를 청각 전문가의 설정에 연결합니다. 전문가가 전극별 자극 역치와 편안한 수준을 측정해 매핑하고, 소리 환경과 청취 과제에 맞춰 조정합니다. 특정한 개인별 청취 결과는 이식 전 평가, 청신경 상태, 재활과 사용 경험에 따라 달라지므로 제품 사양만으로 예측할 수 없습니다.

연구 방향에는 전극 배열·전력 효율·잡음 억제, 음악과 말소리 구분, 양측 장치의 시간차·공간 정보 처리, 실시간 자막·원격 마이크 연동, 청취 결과를 반영한 개인별 매핑이 있습니다. 제품의 내부 신호처리 알고리즘과 펌웨어 개발 도구는 공개되지 않은 범위가 있어 이 글에서 특정 언어·프레임워크를 추정하지 않습니다.

<a id="communication"></a>
## 언어장애: 시선 입력 AAC와 음성 신경보철 연구

Tobii Dynavox TD I-Series는 시선 추적 장치와 음성생성 소프트웨어를 결합한 보완대체의사소통(AAC) 기기입니다. 화면상의 문자·기호를 응시하면 시선 추적기가 눈 위치를 추정하고, 선택된 글자·문장을 음성으로 출력합니다. 제조사는 눈 외에 손가락·스위치 입력도 소개합니다. 개인 어휘, 문장 예측, 선택 시간, 화면 크기, 조명·안경·자세를 조정하는 접근성 설정이 핵심입니다. ([TD I-Series 제품 설명](https://www.tobiidynavox.com/pages/td-i-series))

2023년 Nature의 음성 신경보철 연구는 뇌 표면에서 얻은 ECoG 신호를 해독해 텍스트와 음성·아바타 출력을 만드는 가능성을 한 참가자에게 보였습니다. 연구 시스템은 뇌 신호 전극, 신호 전처리, 신경망 기반 음성 해독, 화면·음성 출력으로 구성됩니다. 이 연구와 기존 시선 AAC의 차이는 입력 신호원입니다. 시선 AAC는 눈 움직임을 이용하는 실제 의사소통 장치이고, 뇌 신호 방식은 침습 전극·수술·신호 안정성·장기 훈련을 포함한 연구 단계입니다. 해당 논문의 성능 수치는 실험 조건과 참가자에게 한정되며 일반 제품의 보장 성능이 아닙니다. ([Nature 원논문](https://www.nature.com/articles/s41586-023-06443-4))

음성 생성에는 개인화 음성, 글자판·기호판, 예측 입력과 오류 수정이 함께 중요합니다. 개발자는 단어 입력 속도뿐 아니라 문장 수정, 대화 순서, 배경 소음, 피로, 보호자나 대화 상대의 도움 없이 쓸 수 있는지를 사용자와 평가합니다.

<a id="facial-rehabilitation"></a>
## 안면장애: 영상에서 맞춤 보철까지

안면 보철의 디지털 제작은 의료 영상이나 3D 표면 스캔에서 결손 부위와 반대편 해부학을 확보하고, CAD에서 보철 형상과 유지 구조를 설계한 뒤, 몰드나 보조 부품을 적층 제조하고 실리콘 등 재료로 마감하는 흐름을 가질 수 있습니다. CT·CBCT 영상을 3D 모델로 바꾸는 작업에는 영상 분할 소프트웨어가 쓰이며, Materialise Mimics는 의료 영상의 구조를 분할해 3D 모델을 만드는 상용 도구의 한 예입니다. 안면 보철 연구에서 실제 사용한 도구는 논문마다 다르므로 제품 설명과 연구 재료·방법을 구분해야 합니다.

2022년 기술 논문은 CBCT와 ZBrush로 결손을 모델링하고 3D 프린팅을 이용해 안면 보철을 제작하는 과정을 설명합니다. ([기술 노트](https://www.mdpi.com/2076-3417/12/23/11974)) UCLA 연구진의 임상 사례 보고는 부분 비절제 환자용 실리콘 코 보철을 위해 두 조각 몰드를 적층 제조했으며, 출력 재료와 실리콘이 접촉할 때 경화가 방해되는 문제를 보고했습니다. 즉 출력 형상이 맞아도 재료의 표면 화학과 실리콘 경화제가 맞지 않으면 완성품이 실패할 수 있습니다. 재료 조합, 표면 처리, 탈형제·프라이머, 경화 시간, 피부 접촉성까지 시험해야 합니다. 이 보고는 증례 기반이며 제작 방법의 우월성을 비교한 임상시험은 아닙니다. ([임상 사례 보고](https://pubmed.ncbi.nlm.nih.gov/39531175/))

연구에서는 3D 스캔의 반복 정합, 보철 테두리의 피부 밀착, 색상 재현, 자석·안경·접착제 고정, 세척과 장기 변색을 평가합니다. 디지털 설계가 전통 수작업보다 모든 면에서 우월하다는 결론을 내리려면 제작 시간, 비용, 적합도, 수정 횟수, 환자 보고 결과를 비교하는 임상 자료가 더 필요합니다.

<a id="kidney-support"></a>
## 신장장애: 가정 투석과 인공신장 연구

Fresenius NxStage System One은 가정 혈액투석에 쓰이는 이동 가능한 장비의 예입니다. 혈액 회로, 투석기, 펌프, 압력·공기·누출 감시, 소모품 카트리지와 투석액 공급이 하나의 시스템으로 묶입니다. 제품 구성에 따라 미리 준비한 투석액 봉투 또는 PureFlow 계열의 투석액 준비 장치를 씁니다. 제어 소프트웨어가 처방된 치료 흐름을 관리하더라도 사용자는 교육, 물·전기·청소 환경, 소모품과 의료진의 관리를 함께 필요로 합니다. ([Fresenius 제품 자료](https://freseniusmedicalcare.com/en/healthcare-professionals/home-therapies/home-hemodialysis/nxstage-system-one/))

Baxter AMIA는 자동 복막투석기의 한 예로, 처방에 따라 밤 동안 복강에 투석액을 주입하고 배액하는 사이클러입니다. FDA 510(k) 문서에는 연결된 Sharesource 원격 관리 플랫폼이 포함된 구성이 설명되어 있습니다. 원격 데이터는 치료 현황 확인에 쓰이는 것이며, 이를 의료진의 감독이나 환자 관리가 필요 없다는 뜻으로 해석하면 안 됩니다. ([FDA 510(k) K151525](https://www.accessdata.fda.gov/cdrh_docs/pdf15/K151525.pdf))

휴대형·이식형 인공신장 연구는 혈액 여과 소형화, 막·흡착 소재, 체액·전해질 균형, 저전력 펌프, 감염·혈전 위험과 장기 내구성에 집중합니다. UCSF Kidney Project는 MEMS 공정으로 만든 실리콘 나노공극 막의 혈액 여과기와 신세뇨관 세포를 배양하는 생물반응기를 조합한 이식형 생체인공신장을 연구하고 있습니다. 목표는 혈압으로 혈액을 여과하고, 여과액에서 물과 염분을 다시 흡수하는 구조입니다. UCSF가 공개한 현재 단계는 소형 시제품의 동물 시험이며, 사람 대상 임상시험은 시작하지 않았습니다. ([UCSF 연구 개요](https://engineering.ucsf.edu/research/kidney-project), [UCSF 연구 단계 FAQ](https://pharm.ucsf.edu/kidney/device/faq))

별도의 휴대형 혈액투석 장치인 NextKidney NeoKidney는 투석액을 재생해 폐쇄 회로에서 다시 쓰도록 설계됐습니다. UMC Utrecht는 일반 가정 투석보다 적은 약 4.5 L의 투석액을 사용하고, 주 4–7회·회당 2시간의 짧고 잦은 치료를 목표로 하는 장치라고 설명합니다. 2026년 네덜란드의 가정 사용 연구는 안전성·혈액 정화 효과·사용 편의와 일상생활 영향을 평가 중이며, 상용 제품으로 널리 판매되는 단계가 아닙니다. ([UMC Utrecht, NeoKidney 가정 사용 연구](https://research.umcutrecht.nl/news/patients-test-a-portable-artificial-kidney-at-home-for-the-first-time/))

UMC Utrecht가 2026년 9월 시작을 알린 BioHybrid Kidney XB 연구는 혈액 필터, 미세유체 기술, 생체 적합 재료와 살아 있는 신장 세포를 하나의 장치로 통합하는 방향입니다. 여과막과 세포를 연결하는 유체 경로, 혈액 접촉 재료, 세포가 물과 유용한 물질을 회수하는 기능을 함께 설계합니다. 연구진은 이식형 장치를 만들기까지 장기 안전성과 세포 기능을 확인해야 한다고 설명합니다. 공개된 대학 자료에는 특정 CAD·해석 프로그램이나 제작 장비 목록이 없어 이를 임의로 추정하지 않습니다. ([UMC Utrecht, BioHybrid Kidney 연구 개요](https://research.umcutrecht.nl/news/new-step-towards-a-bioartificial-kidney-that-could-replace-dialysis/))

연구 도구와 시험에서는 막을 통한 용질 제거율, 압력 강하, 유량, 체액·전해질 수지, 혈액 적합성, 누출·응고, 장시간 사용 때의 안정성을 측정합니다. 인공신장 연구에서 ‘실험실에서 여과가 작동했다’는 것과 ‘사람에게 신장을 대체해 장기간 쓸 수 있다’는 것은 서로 다른 단계입니다.

<a id="cardiac-support"></a>
## 심장장애: 리드리스 심박조율기와 심실보조장치

Medtronic Micra는 심장 안에 직접 삽입하는 리드리스 심박조율기의 FDA 승인 사례입니다. 쇄골 부근의 펄스 발생기와 정맥을 통해 심장까지 이어지는 전극선을 두는 전통 방식과 달리, 작은 기기 안에 감지·제어·배터리·자극 전극을 통합해 우심실 안에 고정합니다. 전극선과 피하 포켓을 줄이는 장점이 있지만, 적용 대상과 해부학적 조건은 FDA 표시 범위에 따르며 기존 심박조율기를 모두 대체하지 않습니다. ([FDA Micra 승인 자료](https://www.fda.gov/news-events/press-announcements/fda-approves-first-leadless-pacemaker-treat-heart-rhythm-disorders))

Abbott Aveir DR은 심방용과 심실용 리드리스 장치가 서로 통신해 특정 환자에게 이중방 조율을 제공하는 시스템입니다. 두 개의 독립된 이식 장치 사이 통신, 시간 동기화, 감지 신호 신뢰성, 배터리 교체·회수 전략이 설계 과제입니다. ([FDA Aveir DR PMA 기록](https://www.accessdata.fda.gov/cdrh/devicesatfda/index.cfm?db=pma&id=520981)) FDA PMA 자료는 승인과 적응증, 임상 평가 내용을 확인하는 출처이며 모든 환자군에 대한 임상 우월성을 의미하지 않습니다.

심실보조장치(VAD)는 펌프, 심실 유입관·대동맥 유출관, 피부를 통과하는 구동선, 외부 제어기와 배터리로 이루어진 시스템입니다. HeartMate 3 등 제품의 평가에서는 혈류량, 혈전·용혈, 펌프 회전, 구동선 감염, 전원·제어기 교체와 경보가 중요합니다. 실제 임상에서 관리하는 항응고와 감염 대응은 전자 제어 성능과 별개로 안전한 사용에 필수적입니다. ([FDA HeartMate 3 보충 허가자료](https://www.accessdata.fda.gov/cdrh_docs/pdf16/P160054S008D.pdf))

<a id="liver-support"></a>
## 간장애: 체외 간 보조와 임상시험

MARS(Molecular Adsorbent Recirculating System)는 알부민 투석을 이용해 혈액의 알부민 결합 독성 물질을 체외 회로에서 제거하는 간 보조 기술입니다. FDA K113313 자료에는 두 개의 투석기와 흡착 컬럼, 알부민 포함 투석액, 롤러 펌프 및 혈액·알부민 회로 감시 항목이 설명되어 있습니다. 이 문서의 표시사항은 약물 과량·중독과 만성 간질환 악화에 따른 간성뇌증이며, 간이식 가교로 허가된 장치라고 설명하지 않습니다. 간세포의 모든 대사·합성·응고 기능을 대신하는 완전한 인공 간은 아닙니다. ([FDA MARS 5.0 510(k) K113313](https://www.accessdata.fda.gov/cdrh_docs/pdf11/K113313.pdf))

Fresenius Medical Care가 2007년 제품자료에서 설명한 Prometheus 체외회로는 알부민 투과 필터로 혈장 일부를 분리하고, 중성 수지·음이온 교환 흡착기로 알부민 결합 물질을 제거한 뒤, 고유량 투석기로 수용성 물질을 처리합니다. 회로에는 혈액 회로와 분리된 혈장 회로, 혈액·혈장 펌프, 필터와 흡착기가 포함됩니다. 2003년 첫 임상 적용 논문은 초기 환자군에서 안전성과 물질 제거를 연구했습니다. 이 장치의 회로 구조나 독성물질 제거만으로 환자의 생존 이득이 입증되는 것은 아닙니다. ([Fresenius Medical Care의 2007년 Prometheus 제품 기술자료](https://www.freseniusmedicalcare.com/fileadmin/data/masterContent/pdf/Prometheus/Prometheus_Product_Range.pdf), [Prometheus 최초 임상 적용 연구](https://www.sciencedirect.com/science/article/pii/S0168827803004689))

간 보조 장치의 실험·임상 평가에는 회로 압력, 혈액 손상, 응고, 알부민·독성물질 제거, 전해질·열·체액 균형, 치료 세션별 임상 결과가 포함됩니다. EASL 2023 가이드라인은 급성-만성 간부전에서 인공·바이오인공 간 보조를 임상시험 외 일상적으로 사용하도록 권고할 근거가 충분하지 않다고 정리합니다. ([EASL 임상지침 (2023)](https://www.journal-of-hepatology.eu/article/S0168-8278%2823%2900244-1/fulltext)) UK HRA에 등록된 DIALIVE 2.0 계획은 영국 약 12개 병원에서 72명을 모집해 표준 치료와 비교하고, 10일 동안 최대 7회의 치료와 90일 추적을 하도록 설계됐습니다. 이는 연구 계획이며 효과가 입증되거나 상용화된 결과가 아닙니다. ([UK HRA 연구 요약](https://www.hra.nhs.uk/planning-and-improving-research/application-summaries/research-summaries/dialive-20-in-aclf/))

<a id="respiratory-support"></a>
## 호흡기장애: 환기 장치의 제어와 안전 사례

가정용 인공호흡기는 사용자가 설정한 환기 모드와 압력·용적·호흡수에 따라 공기를 전달하고, 회로 압력과 유량, 누출, 배터리와 내부 상태를 감시합니다. 환자와 회로 연결이 빠지거나 전원·센서·밸브·제어기 중 하나가 고장 나면 경보가 사용자의 안전과 직접 연결됩니다. 백업 환기, 배터리 상태, 알람 전달, 보호자 훈련은 제품을 쓰는 시스템의 일부입니다.

2026년 FDA는 ResMed Astral 100/150 중 특정 일련번호 범위에 대해 Class I 리콜을 분류했습니다. FDA 기록에 따르면 내부 슈퍼커패시터에서 전해액이 누출되어 회로기판의 충전 칩을 손상시키고, 장치가 fail-safe 상태로 들어가 환기가 중단될 수 있습니다. 원인 분류는 부품 설계·선정이며, 모든 Astral 기기에 해당하는 문제가 아니라 공지된 영향 범위의 장치에 관한 시정 조치입니다. 이 사례는 전자부품 단품 수명시험만으로는 누액이 인접 회로에 미치는 영향과 실제 환기 중단의 시스템 안전성을 놓칠 수 있음을 보여줍니다. ([FDA Class I 리콜 기록 Z-2735-2026](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRES/res.cfm?id=221232))

이 고장 원인을 바탕으로 한 공학적 시험 제안에는 부품 노화·온도·진동 조건 후 누액 감지, 오염 확산 경로, 충전·배터리 전환 반복, 고장 주입, 경보와 백업 환기 전환이 포함됩니다. 이는 FDA나 제조사가 공개한 실제 조사 절차를 옮긴 것이 아니라, 공개된 고장 사슬에서 도출한 검증 항목입니다.

NeuRx Diaphragm Pacing System은 FDA가 지정한 일부 고위 경수 손상 등 대상자에서 횡격막 신경을 전극으로 자극하는 삽입형 시스템입니다. FDA 문서에는 복강경으로 설치하는 네 전극, 외부 임상 시스템과 펄스 발생기·제어기가 설명되어 있습니다. 적응증과 횡격막 신경 반응을 확인하는 평가가 선행되어야 하며, 모든 호흡기 장애에서 인공호흡기를 대체하지 않습니다. ([FDA NeuRx P200018](https://www.fda.gov/medical-devices/recently-approved-devices/neurx-diaphragm-pacing-system-p200018))

<a id="ostomy-care"></a>
## 장루·요루장애: 보호판 아래 누출 감지

Coloplast Heylo System은 장루 주머니 보호판 아래의 누출을 감지해 앱으로 알림을 보내는 시스템입니다. FDA 510(k) 문서에 따르면 접착 보호 장벽에 통합된 센서가 장루 배출물이 새는 상황을 감지하고, 송신기가 자료를 앱에 전달합니다. 미국 표시사항은 회장루 또는 결장루가 있는 12세 이상 사용자의 장루 기기 누출 감지입니다. 요루까지 같은 표시 범위라고 확대하지 않습니다. ([FDA 510(k) K252140](https://www.accessdata.fda.gov/cdrh_docs/pdf25/K252140.pdf))

기술 흐름은 보호판 아래 센서 → 송신기 → Bluetooth 등 근거리 무선 연결 → 모바일 앱 알림입니다. 감지 시점이 너무 늦으면 피부 노출을 막지 못하고, 습기·땀·움직임을 누출로 오인하면 오경보가 늘 수 있습니다. 2023년 ASSISTER 무작위 교차시험은 144명을 배정하고 139명을 분석해 Heylo 사용 8주 뒤 정서적 영향과 사회 참여 지표가 표준 관리보다 개선되었다고 보고했습니다. 기기 관련 이상사례 5건은 피부 자극이었습니다. 이 논문에는 Coloplast 소속 저자가 포함되어 있으므로 연구 설계·이해관계와 함께 결과를 읽고 다른 집단과 환경의 자료도 확인해야 합니다. 2024년 다기관 연구는 실제 사용 단계의 누출 감지와 사용 경험을 살펴봅니다. 이들 연구를 여러 국가의 모든 사용자가 같은 결과를 얻는다는 뜻으로 확대하지 않습니다.

평가에서는 누출을 얼마나 일찍 감지하는지, 알림 지연과 오경보, 보호판 종류·피부 주름·움직임에 따른 편차, 배터리와 앱 연결 실패, 사용자의 교체 행동을 함께 봅니다. 요루 관리에 적용하려면 해당 제품의 별도 표시사항과 임상 근거를 확인해야 합니다.

<a id="epilepsy"></a>
## 뇌전증장애: 발작 알림과 반응성 신경자극

Empatica EpiMonitor는 손목형 EmbracePlus와 모바일 앱을 결합해 FDA 510(k) 실질적 동등성 결정을 받은 기기입니다. 손목의 피부전도(EDA)와 움직임 신호로 전신 강직간대발작과 연관될 수 있는 패턴을 감지해 지정 보호자에게 알림을 보냅니다. FDA 표시사항은 성인과 6세 이상 아동의 보조적 발작 감시를 명시합니다. 발작을 예측하거나 진단하는 장치로 보지 않습니다. ([FDA 510(k) K232915](https://www.accessdata.fda.gov/cdrh_docs/pdf23/K232915.pdf))

NeuroPace RNS는 뇌 안의 전극에서 신경 신호를 감지하고, 발작 패턴으로 판단될 때 반응성 자극을 주는 삽입형 시스템입니다. FDA의 최초 PMA 표시는 약물 저항성 부분발작 성인 가운데 진단검사로 발작 발생 부위가 최대 두 곳으로 확인된 경우의 보조 치료입니다. 피부 위 손목 센서의 발작 감시와 두개 내 신호를 이용한 치료 장치는 측정 위치·기능·위험이 다른 기술입니다. ([FDA NeuroPace RNS PMA](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?id=P100026))

연구와 임상 검증은 감도와 함께 시간당 오경보, 야간·운동 중 성능, 신호가 없는 구간, 발작 종류별 누락, 자극 후 부작용과 배터리·데이터 전송을 평가합니다. 감지 알고리즘의 민감도 설정을 높이면 오경보가 늘 수 있으므로, 임계값은 사용자 환경과 사용 목적에 맞춰 평가해야 합니다.

<a id="glucose-control"></a>
## 췌장장애: 연속혈당측정과 자동 인슐린 전달

자동 인슐린 전달(AID) 시스템은 연속혈당측정기(CGM), 제어 소프트웨어와 인슐린 펌프가 연결된 폐루프 제어 시스템입니다. CGM은 혈액이 아닌 간질액의 포도당을 측정하므로 혈당 변화와 센서값 사이에 지연이 있을 수 있습니다. 제어 소프트웨어는 최근 센서값과 추세를 처리해 펌프 명령을 결정하고, 전달한 인슐린이 몸에서 작용하기까지의 시간과 저혈당 위험을 고려해야 합니다.

FDA가 2023년 510(k) 실질적 동등성 결정을 내린 Beta Bionics iLet 시스템은 iLet ACE Pump, iLet Dosing Decision Software, 호환되는 FDA 허가 CGM으로 구성됩니다. FDA는 미국에서 6세 이상 제1형 당뇨병 환자를 대상으로 한 표시사항을 설명합니다. 제품 알고리즘은 체중 입력으로 시작하고, 식사량을 소·중·대 식사로 알리는 방식으로 인슐린 용량 계산을 조정합니다. FDA 문서는 알고리즘이 기저·보정·식사 인슐린 결정을 내린다고 기술하지만, 소프트웨어의 소스 코드나 개발 언어는 공개하지 않습니다. ([FDA iLet 결정 자료](https://www.fda.gov/news-events/press-announcements/fda-clears-new-insulin-pump-and-algorithm-based-software-support-enhanced-automatic-insulin-delivery))

검증은 정상적인 식사·운동뿐 아니라 CGM 지연·탈락·압축 저혈당·통신 단절·펌프 막힘·잔량 부족·사용자 입력 누락을 포함합니다. 안전 상태로 전환하는 규칙과 알람, 수동 인슐린 투여를 위한 백업 계획, 사용자가 장치를 다시 제어할 수 있는 방법도 시스템 요구사항입니다. 알고리즘을 분석할 때는 평균 혈당만 보지 않고 저혈당 시간, 목표 범위 시간, 고혈당 시간, 센서 누락과 사용자별 편차를 함께 봅니다.

제품 상태를 볼 때는 FDA가 2026년 10월 27일 갱신한 공개 회수 기록도 확인할 수 있습니다. 기록에는 특정 iLet 소프트웨어 버전에서 상태 표시줄 아이콘으로 잠금 화면이나 제한 접근 화면을 우회할 수 있는 문제가 기재되어 있습니다. 승인된 사용자 외 사람이 식사량을 입력하거나 인슐린 전달을 중단할 경우 중증 저혈당 위험이 생길 수 있어, FDA는 소프트웨어 설계 문제로 분류했습니다. 이 기록은 특정 버전의 수정 조치에 관한 것이며, 제품 전체나 다른 버전에 같은 결함이 있다는 뜻은 아닙니다. ([FDA iLet 소프트웨어 회수 기록 Z-1809-2026](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRES/res.cfm?id=218989))

## 미래 연구를 읽을 때 구분할 단계

| 연구 방향 | 현재 공개된 연구·개발의 예 | 아직 입증되지 않은 것 |
|---|---|---|
| 뇌-척수 인터페이스 | 한 명의 척수손상 참가자에서 걷기 의도와 척수 자극 연결을 보고한 임상 개념 증명 | 다양한 손상·사용자에서의 장기 안전성과 일상용 보급 |
| 음성 신경보철 | ECoG 신호에서 텍스트·음성 출력을 해독한 참가자 연구 | 수술 없이 사용하거나 광범위한 언어장애에 적용하는 성능 |
| 생체공학 신장 | UCSF 실리콘 나노공극 필터와 신세뇨관 생물반응기 연구 | 임상시험을 통한 장기 이식 안전성과 신장 기능 대체 |
| 휴대형 투석 | NeoKidney 등 가정 사용을 평가하는 임상 연구 | 일반 판매·통상 치료에서의 효과와 접근성 |
| 간 보조 장치 | DIALIVE 2.0 등 임상시험 설계 및 모집 단계의 연구 | 생존율 향상을 포함한 확증적 임상 결과 |
| 접근성 AI | 장면·문서·물체 인식과 자연어 설명 | 인식 오류가 있는 환경에서의 안전한 자율 이동 대체 |
| 근전도 의지 제어 | 다중 근전도 입력, 개인별 동작 분류, 감각 피드백 연구 | 다양한 사용자에게 장기간 안정적으로 맞는 상용 성능 |
| 로봇 재활 | 생체역학 모델과 로봇 제어의 시뮬레이션·임상 연구 | 환자별 일상 기능의 장기 향상을 입증하는 임상 자료 |

연구의 다음 단계를 확인할 때는 논문 전문의 연구대상·설계·측정변수, 임상시험 등록 상태, 규제기관의 허가 문서, 제품 제조사의 사용 설명서를 각각 확인합니다. 기업·대학 연구실의 보도자료만으로 임상 효과나 제품 이용 가능성을 단정하지 않습니다.

<a id="engineering-tools"></a>
## 연구·개발에서 실제 쓰이는 도구

| 도구·연구 방식 | 공개 자료로 확인되는 쓰임 | 결과물과 주의점 |
|---|---|---|
| [OpenSim](https://opensim.stanford.edu/) | Stanford의 오픈소스 근골격 모델링·시뮬레이션 플랫폼 | 관절 운동과 근육·힘줄 모델을 분석합니다. 실제 환자의 힘을 직접 측정한 값과 모델 추정값을 구분합니다. |
| [OpenSense](https://mobilize.stanford.edu/software/) | IMU 관성 센서 기반 동작 분석 | 웨어러블 센서의 방향·보정·센서 배치 오차가 관절 운동 추정에 미치는 영향을 확인합니다. |
| [OpenSim Moco](https://opensim.stanford.edu/) | 근골격 시뮬레이션의 최적화 문제 | 목적함수와 생체역학 제약을 둔 계산 결과이며, 임상적으로 최선인 동작을 자동으로 보장하지 않습니다. |
| [AddBiomechanics](https://mobilize.stanford.edu/software/) | 보행 자료를 처리하고 OpenSim 분석 흐름을 지원하는 연구 도구 | 입력 자료 품질과 모델 가정을 확인해야 합니다. |
| MATLAB/Simulink, SolidWorks, ROS, Gazebo ([논문](https://ieeexplore.ieee.org/abstract/document/11142188)) | IEEE 재활 로봇 논문에서 3D 구조 설계, 로봇 시뮬레이션, 운동학·제어 계산을 연결 | 2025년 학회 논문에서 사용한 연구 구성입니다. 임상시험이나 모든 병원·기업의 공통 툴체인이라는 뜻은 아닙니다. |
| [MuJoCo 기반 RehabBot](https://doi.org/10.1016/j.softx.2026.102800) | 2026년 논문에서 UR5e 협동로봇과 관절형 사람 모델로 어깨·팔꿈치·엉덩이·무릎 운동을 강화학습에 적용한 오픈소스 시뮬레이션 환경 | 안전 제약이 있는 관측·행동·보상 체계를 갖춥니다. 가상 모델의 결과이며, 실제 환자 효과나 안전성이 입증됐다는 뜻은 아닙니다. |
| [ZBrush와 CBCT](https://www.mdpi.com/2076-3417/12/23/11974) | 맞춤 안면 보철의 디지털 설계 사례에서 사용 | 논문이 사용한 영상·모델링 도구와 출력 몰드·실리콘 재료를 함께 확인합니다. |
| [Materialise Mimics](https://www.materialise.com/en/healthcare/mimics/mimics-core) | 의료 영상 분할과 3D 해부 모델 제작을 지원하는 상용 소프트웨어 | 회사가 설명하는 기능입니다. 특정 안면 보철 논문에서 Mimics를 썼다고 연결하지 않습니다. |
| [UCSF 생체인공신장 연구](https://engineering.ucsf.edu/research/kidney-project) | MEMS 실리콘 나노공극 막, 혈압 구동 여과기, 신세뇨관 세포 생물반응기를 통합하는 연구 방식 | 소형 시제품의 동물 시험 단계입니다. 공개 자료에 특정 설계·해석 프로그램은 적혀 있지 않습니다. |
| [C-Soft Plus](https://spa-prod-commerce.cep.ottobock.com/medias/C-Leg4Update-InstructionsforProfessionals-English-7-2024.pdf?attachment=true&context=bWFzdGVyfHJvb3R8MzQ2NjA5NnxhcHBsaWNhdGlvbi9wZGZ8aDZkL2g4OC85Mzk3MDgxNDQwMjg2LnBkZnwwZDEzYTkzODI1YzlhZjUwYTVjZTRmODdkOWQ4OTlmMjJiYTE0MmEwNDBjYjUxN2ZmYTM0NDVmOTZjODBiZDVi) | 보장구 전문가가 C-Leg 설정을 조정하는 제조사 도구 | 제조사 안내서에 적힌 설정 절차를 뜻하며, 공개 연구용 개발 환경은 아닙니다. |
| [Cochlear Custom Sound](https://assets.cochlear.com/api/public/content/FUN4812-Nucleus-8-Tech-Specs-Sheet.pdf) | 청각 전문가가 인공와우를 설정하는 제조사 소프트웨어 | 환자별 전극 매핑에 쓰입니다. 외부 개발자가 내부 신호처리 코드를 수정하는 도구가 아닙니다. |
| [FDA 소프트웨어 검증 지침](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-principles-software-validation) | 의료기기 소프트웨어와 의료기기 설계·개발·제조에 사용하는 소프트웨어의 검증 원칙 | 개발 산출물·시험·요구사항 추적 기준을 참고합니다. 제품별 허가 규정을 대신하지 않습니다. |

임베디드 펌웨어, 신경 신호 처리, 인공와우의 인코더, 인슐린 제어 소프트웨어는 제품 안전과 지식재산 때문에 상세 코드나 툴체인이 공개되지 않는 경우가 많습니다. 공개되지 않은 내용을 C, C++, Python, 특정 IDE나 딥러닝 프레임워크로 구현했다고 꾸며 쓰지 않습니다. 공개된 논문·매뉴얼에서 실제로 확인된 도구만 사례에 연결합니다.

<a id="verification"></a>
## 검증 계획과 고장 분석

제품마다 위험은 다르지만, 요구사항과 시험 결과를 연결하는 표를 만들면 기능을 어떻게 확인할지 구체적으로 정할 수 있습니다. 아래 시험 예시는 기술 학습을 위한 공학적 제안이며, 개별 제조사의 실제 검증 프로토콜을 인용한 것은 아닙니다.

| 시스템 | 입력·출력 | 시험 예 | 고장 시 안전한 동작 |
|---|---|---|---|
| 근전도 의지 | EMG → 손가락 모터 | 전극 접촉 변화, 땀·근피로, 동시 수축에서 오동작률 측정 | 불확실한 신호에서 모터를 멈추거나 안전한 그립 상태로 제한 |
| 무릎 의지·외골격 | 관성·각도·사용자 입력 → 유압 저항·관절 모터 | 평지·경사·계단·정지·배터리 저하·센서 단선 시나리오 | 보행 중 급격한 관절 붕괴나 의도하지 않은 동작 방지 |
| FES | 보행 센서 → 전기 펄스 | 센서 지연, 잘못된 보행 위상, 전극 접촉 저하 | 자극 상한·중단 조건, 사용자 수동 중지 |
| 화면 인식·AAC | 영상·시선 → 음성·문자 선택 | 낮은 조도·안경 반사·문장 수정·오입력 회복 | 잘못 인식한 정보를 확정된 사실처럼 읽지 않도록 표시 |
| 투석 장치 | 압력·유량·온도·혈액 회로 → 펌프·밸브 | 막힘·누출·공기·정전·센서 편차의 고장 주입 | 환자 회로를 안전 상태로 격리하고 경보·대체 절차 제공 |
| 인공호흡기 | 압력·유량·전원 → 송풍기·밸브 | 전원 전환, 배터리 수명, 회로 누출, 충전 회로 부품 열화 | 환기 중단을 조기에 알리고 백업 환기 절차로 이어짐 |
| 발작 감지·자극 | EDA·가속도·뇌 신호 → 알림·신경자극 | 발작 유형·수면·운동에 따른 민감도와 오경보 평가 | 알림 누락을 치료 효과로 오인하지 않고 치료 출력을 제한 |
| AID | CGM·식사 입력 → 인슐린 펌프 | 지연·센서 탈락·저혈당·통신 단절·막힘 상황 시험 | 전달량 상한, 안전한 일시중지, 명확한 사용자 경보 |

FDA Astral 리콜 사례는 알려진 고장 사슬을 시스템 수준에서 검토할 필요를 보여줍니다.

```text
슈퍼커패시터 전해액 누출
        ↓
회로기판(PCBA) 오염·충전 칩 손상
        ↓
안전 정지 상태 진입
        ↓
환기 치료 중단
```

첫 원인을 부품 검사에서 찾더라도, 환기 중단을 예방하고 감지하는 기능은 전원·배터리·알람·백업 장비와 함께 시험해야 합니다. 특정 장치의 회수·점검 여부는 FDA가 공개한 일련번호 및 제조사 시정 공지를 확인해야 하며, 이 문서만으로 개인 기기의 사용 여부를 판단하지 않습니다.

## English

This article connects disability-specific overviews to real assistive devices, rehabilitation systems, research programs and engineering tools. It distinguishes products with regulatory indications from clinical studies and early-stage research. Public documentation identifies some tools, such as OpenSim, OpenSense, C-Soft-Plus, Custom Sound, ZBrush and Mimics; proprietary firmware stacks and unpublished algorithms are not guessed. Verification examples are labeled as engineering proposals unless they are directly reported in a public regulatory or research source.

<a id="sources"></a>
## 출처와 자료의 범위

### 의지·이동·운동 재활

- [Ottobock, C-Leg 사용 및 전문가 안내서](https://spa-prod-commerce.cep.ottobock.com/medias/C-Leg4Update-InstructionsforProfessionals-English-7-2024.pdf?attachment=true&context=bWFzdGVyfHJvb3R8MzQ2NjA5NnxhcHBsaWNhdGlvbi9wZGZ8aDZkL2g4OC85Mzk3MDgxNDQwMjg2LnBkZnwwZDEzYTkzODI1YzlhZjUwYTVjZTRmODdkOWQ4OTlmMjJiYTE0MmEwNDBjYjUxN2ZmYTM0NDVmOTZjODBiZDVi): 센서·유압 무릎 구조, 안전 모드, 전문가용 C-Soft-Plus 설정.
- [Open Bionics, Hero Arm 사용자 안내](https://openbionics.com/en/hero-arm-user-guide/): 근육 제어, 손 모터 구성, 3D 스캔 기반 소켓, 사용 조건과 안전 정보.
- [미국 FDA, ReWalk 7 510(k) K241822](https://www.accessdata.fda.gov/cdrh_docs/pdf24/K241822.pdf): 결정일 2025년 3월 12일, 제품 설명과 척수 손상 수준·장소별 표시사항.
- [Courtine et al., Walking naturally after spinal cord injury using a brain–spine interface, Nature (2023)](https://www.nature.com/articles/s41586-023-06094-5): 뇌-척수 인터페이스 임상 개념 증명.
- [Bioness, L300 Go 사용 안내서](https://www.bionessuniversity.com/documents/L300Go%20User%27s%20Guide%20Rev.%20E%20%5Befile%5D.pdf): FES 기기 사용·안전 정보.
- [Stanford OpenSim](https://opensim.stanford.edu/), [Mobilize Center software](https://mobilize.stanford.edu/software/): OpenSim, OpenSense, Moco, AddBiomechanics의 공식 소프트웨어 소개.
- [MATLAB/Simulink and ROS/Gazebo Co-Simulation of an Upper Limb Rehabilitation Robot for Kinematics and Dynamic Modeling, IEEE ATiGB (2025)](https://ieeexplore.ieee.org/abstract/document/11142188): SolidWorks, Gazebo, ROS, MATLAB/Simulink를 연결한 6자유도 상지 재활 로봇 시뮬레이션.
- [RehabBot: Reinforcement learning environment for upper and lower limb robot-assisted rehabilitation, SoftwareX (2026)](https://doi.org/10.1016/j.softx.2026.102800): MuJoCo 기반 강화학습 연구 환경과 가상 사람 모델.

### 시각·청각·의사소통 접근

- [Apple Accessibility](https://www.apple.com/accessibility/) 및 [Apple Developer, VoiceOver](https://developer.apple.com/documentation/accessibility/voiceover/): 화면 읽기·점자·앱 접근성.
- [Microsoft Seeing AI 사용자 안내서](https://www.microsoft.com/en-us/garage/wp-content/uploads/2025/04/Seeing-AI-User-Manual.pdf): 모바일 앱의 인식 기능과 출력 방식.
- [Cochlear, Nucleus 8 기술 사양](https://assets.cochlear.com/api/public/content/FUN4812-Nucleus-8-Tech-Specs-Sheet.pdf), [NIDCD, Cochlear Implants](https://www.nidcd.nih.gov/health/cochlear-implants): 외부 처리기·이식부·전극의 신호 경로.
- [Tobii Dynavox, TD I-Series](https://www.tobiidynavox.com/pages/td-i-series), [ASHA, AAC Practice Portal](https://www.asha.org/practice-portal/professional-issues/augmentative-and-alternative-communication/): 시선 입력·음성생성 AAC와 개인별 접근 방식.
- [Metzger et al., A high-performance neuroprosthesis for speech decoding and avatar control, Nature (2023)](https://www.nature.com/articles/s41586-023-06443-4): 뇌 표면 신호를 활용한 음성 신경보철 연구.

### 안면 보철·신장·심장·간

- [Kiat-Amnuay et al., CBCT와 디지털 모델링 기반 안면 보철 사례](https://www.mdpi.com/2076-3417/12/23/11974): CBCT, ZBrush와 적층 제조 과정.
- [Chen et al., Silicone cure inhibition with material jetting additive manufacturing utilized for facial prosthesis fabrication (Epub 2024; 2026 issue)](https://pubmed.ncbi.nlm.nih.gov/39531175/): 부분 비절제 환자용 실리콘 코 보철 제작에서 출력 몰드와 실리콘의 경화 저해를 보고한 임상 증례.
- [Materialise Mimics Core](https://www.materialise.com/en/healthcare/mimics/mimics-core): 의료 영상 분할·3D 모델 소프트웨어의 제조사 설명.
- [Fresenius Medical Care, NxStage System One](https://freseniusmedicalcare.com/en/healthcare-professionals/home-therapies/home-hemodialysis/nxstage-system-one/): 가정 혈액투석 제품 구조와 운영 개요.
- [미국 FDA, AMIA with Sharesource 510(k) K151525](https://www.accessdata.fda.gov/cdrh_docs/pdf15/K151525.pdf): 자동 복막투석 시스템의 허가 자료.
- [UCSF Kidney Project](https://engineering.ucsf.edu/research/kidney-project), [UCSF 자주 묻는 질문](https://pharm.ucsf.edu/kidney/device/faq): MEMS 실리콘 나노공극 여과기, 세포 생물반응기, 동물 시험과 임상 전 단계.
- [UMC Utrecht, NeoKidney 가정 사용 임상 연구 소식](https://research.umcutrecht.nl/news/patients-test-a-portable-artificial-kidney-at-home-for-the-first-time/): 투석액 재생 회로, 짧고 잦은 치료 방식, 환자 대상 임상 평가.
- [UMC Utrecht, BioHybrid Kidney XB 연구](https://research.umcutrecht.nl/news/new-step-towards-a-bioartificial-kidney-that-could-replace-dialysis/): 혈액 필터·미세유체·생체재료·신장 세포의 통합 연구.
- [미국 FDA, Micra 리드리스 심박조율기 승인 자료](https://www.fda.gov/news-events/press-announcements/fda-approves-first-leadless-pacemaker-treat-heart-rhythm-disorders), [Abbott Aveir DR PMA](https://www.accessdata.fda.gov/cdrh/devicesatfda/index.cfm?db=pma&id=520981): 리드리스 조율기의 규제·제품 자료.
- [미국 FDA, HeartMate 3 허가·표시자료](https://www.accessdata.fda.gov/cdrh_docs/pdf16/P160054S008D.pdf): 심실보조장치 구성과 사용 범위.
- [미국 FDA, MARS 510(k) K113313](https://www.accessdata.fda.gov/cdrh_docs/pdf11/K113313.pdf): 알부민 투석 장치 및 회로 감시 정보.
- [Fresenius Medical Care, Prometheus 2007 제품 기술자료](https://www.freseniusmedicalcare.com/fileadmin/data/masterContent/pdf/Prometheus/Prometheus_Product_Range.pdf), [Rifai et al., Prometheus 최초 임상 적용 연구, Journal of Hepatology (2003)](https://www.sciencedirect.com/science/article/pii/S0168827803004689): 혈장 분획·흡착·고유량 투석 회로와 초기 임상 평가.
- [EASL Clinical Practice Guidelines on acute-on-chronic liver failure (2023)](https://www.journal-of-hepatology.eu/article/S0168-8278%2823%2900244-1/fulltext): 체외 간 보조의 임상 권고 근거.
- [UK HRA, DIALIVE 2.0 in ACLF](https://www.hra.nhs.uk/planning-and-improving-research/application-summaries/research-summaries/dialive-20-in-aclf/): 임상시험 설계와 윤리 검토 현황.

### 호흡·장루·뇌전증·혈당

- [미국 FDA, ResMed Astral 100/150 Class I recall Z-2735-2026](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRES/res.cfm?id=221232): 리콜 시작일 2026년 6월 25일, 게시일 7월 28일, 영향 일련번호와 고장 사슬.
- [미국 FDA, NeuRx Diaphragm Pacing System P200018](https://www.fda.gov/medical-devices/recently-approved-devices/neurx-diaphragm-pacing-system-p200018): 기기 구성·대상·사용 범위.
- [미국 FDA, Coloplast Heylo K252140](https://www.accessdata.fda.gov/cdrh_docs/pdf25/K252140.pdf): 2025년 10월 6일 결정 및 누출 감지 사용 표시사항.
- [Heylo multi-centre clinical evaluation (2024), PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11477101/), [ASSISTER randomized crossover trial (2023), PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11975707/): 보호판 아래 누출 감지와 사용자의 삶의 질·참여를 평가한 연구.
- [미국 FDA, EpiMonitor K232915](https://www.accessdata.fda.gov/cdrh_docs/pdf23/K232915.pdf): EDA·움직임 기반 감시와 사용자 범위.
- [미국 FDA, NeuroPace RNS PMA P100026](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpma/pma.cfm?id=P100026): 승인 표시사항과 후속 자료.
- [미국 FDA, Beta Bionics iLet AID 허가 보도자료 (2023)](https://www.fda.gov/news-events/press-announcements/fda-clears-new-insulin-pump-and-algorithm-based-software-support-enhanced-automatic-insulin-delivery), [미국 FDA, iLet 소프트웨어 회수 기록 Z-1809-2026](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfRES/res.cfm?id=218989): 허가 구성·대상 범위와 특정 소프트웨어 버전의 GUI 접근 제어 시정 조치.

### 개발·검증 기준

- [FDA, General Principles of Software Validation (2002)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-principles-software-validation): 의료기기 소프트웨어와 개발·제조 소프트웨어의 검증 원칙.
- [FDA, ISO 14971:2019 recognized consensus standard record](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/detail.cfm?standard__identification_no=41349): 의료기기 위험관리 표준의 FDA 인정 정보.
