# 지체장애와 의지·이동 보조기술 | Limb difference and mobility technology

## 기능과 필요한 과제

지체장애는 팔·다리·몸통의 기능, 관절 움직임, 근력, 감각, 절단·변형 등 여러 상태를 포괄합니다. 필요한 기술도 손으로 물건을 잡기, 서기, 실내외 이동, 오래 앉아 있기처럼 과제마다 달라집니다. 한 사람에게도 활동과 장소에 따라 의지, 보조기, 수동 휠체어, 전동 휠체어가 함께 필요할 수 있습니다.

## 현재 쓰이는 기술

의지는 소켓·현가부·관절·말단 장치로 이루어집니다. 소켓은 잔존 사지와 의지를 연결하므로 압력 분포, 피부 상태, 땀, 정렬과 움직임 때의 미끄러짐이 착용성과 직접 연결됩니다. 전동 의수의 근전도 제어는 피부 전극이 근육에서 생기는 작은 전압 변화를 읽고, 이를 손가락·손목의 동작 명령으로 바꿉니다. 다관절 의수는 여러 근전도 패턴이나 별도 스위치로 그립을 바꿉니다. 제어 정확도뿐 아니라 전극 위치 변화, 땀과 피로, 무게, 배터리, 물체를 놓치는 안전성도 확인해야 합니다.

하지 의지와 보조기는 무릎·발목의 하중과 관절 운동을 전달합니다. 기계식 무릎은 기구의 저항과 걸림 구조로 안정성을 확보하고, 마이크로프로세서 제어 무릎은 각도·하중 센서와 움직임 정보를 이용해 보행 단계에 따라 저항을 조절합니다. 휠체어는 구동부만큼 좌석·등받이·쿠션 설정이 중요합니다. 체형과 자세를 맞추지 못하면 압력 손상, 통증, 이동 피로가 생길 수 있습니다.

미국 FDA는 DEKA Arm System을 상지 의지의 한 사례로 분류했습니다. 이는 다자유도 의지의 규제·평가 사례이며 모든 사용자가 같은 동작을 얻거나 같은 장치를 이용할 수 있다는 뜻은 아닙니다. 척수손상 사용자를 위한 ReWalk 개인용 외골격도 FDA 자료에서 처방형 장치와 사용 조건이 제시됩니다. 실제 보행은 지정된 사용자 조건과 교육·감독 범위에서 평가해야 합니다.

## 공학적으로 살펴볼 지점

- 기구·재료: 관절 가동범위, 하중 경로, 구조 피로, 소켓 압력, 방수·먼지와 피부 접촉 재료를 봅니다.
- 센서: 근전도, 관절 각도, 관성측정장치(IMU), 발바닥·소켓 하중을 조합할 수 있습니다.
- 제어: 의수는 의도한 그립과 실제 손 동작의 대응을, 하지 장치는 보행 단계 전환과 낙상 위험을 평가합니다.
- 검증: 실험실의 최대 힘뿐 아니라 물체를 잡아 옮기기, 문 열기, 경사로 이동, 배터리 소진과 센서 고장 상황을 시험합니다.

## 앞으로의 연구

연구 중인 방향에는 의지의 촉각을 피부나 신경 자극으로 돌려주는 감각 피드백, 착용 압력을 줄이는 맞춤 소켓, 사용자의 보행에 맞춰 제어를 조정하는 장치, 뇌·신경 신호와 보조기기를 연결하는 폐회로 인터페이스가 있습니다. 일부는 실험실이나 제한된 임상 연구 단계이며 일상 제품으로 널리 쓰이는 기술과 구분해야 합니다. 장기 사용에는 전극 안정성, 수술·감염 위험, 배터리·충전, 정비, 개인 데이터 보호 문제가 함께 남습니다.

## 실제 제품·연구와 공학 도구

실제 제품의 작동 흐름, 제조사가 공개한 사용 범위, 관련 연구와 개발 도구는 [장애 보조기기와 재활 연구의 실제 제품·개발 도구](실제기기와연구개발도구_engineering-cases-and-tools.md#limb-mobility)에서 이어서 보실 수 있습니다.

## English

Mobility technology includes prosthetic limbs, orthoses, wheelchairs and powered exoskeletons. Fit, control, skin pressure, fatigue, battery life and safety in real tasks matter as much as actuator performance. Sensory feedback and neural control remain research directions with different levels of clinical evidence and availability.

## 출처

- [대한민국 법제처, 장애인복지법 시행령 별표 1](https://www.law.go.kr/LSW/flDownload.do?bylClsCd=110201&flSeq=159613615&gubun=): 지체장애의 법적 유형 기준.
- [미국 FDA, DEKA Arm System De Novo 결정 자료](https://www.accessdata.fda.gov/cdrh_docs/reviews/DEN120016.pdf): 장치의 분류와 평가 범위.
- [미국 FDA, ReWalk Personal Exoskeleton 6.0 요약](https://www.accessdata.fda.gov/cdrh_docs/pdf22/K221696.pdf): 처방·사용 조건의 예.
- [미국 NIH/NINDS, Spinal Cord Injury](https://www.ninds.nih.gov/health-information/disorders/spinal-cord-injury): 휠체어·보조기·전기자극·로봇재활·BCI 연구.
- [휠체어 처방과 맞춤 좌석에 관한 임상 리뷰](https://pmc.ncbi.nlm.nih.gov/articles/PMC7384540/): 사용자 능력·환경·좌석 맞춤의 중요성.
