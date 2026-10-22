# 컴퓨터공학·AI 과목별 공개 강의 | Computer science and AI courses

[학습 사이트와 채널](README.md) · [컴퓨터공학·AI 채널](컴퓨터공학과AI유튜브_computing-ai-youtube.md) · [전기전자 과목](전기전자통신과목_ece-courses.md)

컴퓨터과학·컴퓨터공학·AI의 학부 기초부터 대학원 전공 심화까지 공부할 수 있는 공개 강의와 교재입니다. 프로그래밍·수학·알고리즘을 공통 기반으로 두고, 언어·시스템·데이터·보안·AI의 세부 분야로 나누었습니다. 과목 구성은 KAIST·MIT의 전산학 교육과정과 CMU의 머신러닝 석사 교육과정을 참고했습니다.

표에는 수준·권장 선수지식과 이용할 수 있는 자료 형식을 적었습니다. 별도로 한국어를 표시한 자료 외에는 영어 자료입니다. 학교별 필수·선택 과목과 석·박사 이수 요건은 아래 공식 교육과정에서 찾으실 수 있습니다.

## 분야별 바로가기

- [수학과 전산 기초](#수학과-전산-기초) · [알고리즘과 언어](#알고리즘과-언어) · [소프트웨어와 시스템](#소프트웨어와-시스템)
- [데이터·네트워크·보안](#데이터네트워크보안) · [사람·시각·로봇](#사람시각로봇)
- [AI 기초와 심화](#ai-기초와-심화) · [학습 이론과 데이터 해석](#학습-이론과-데이터-해석) · [AI 시스템과 연구](#ai-시스템과-연구)

## 과목을 고르는 순서

프로그래밍·이산수학·선형대수·확률을 익힌 뒤 자료구조와 알고리즘을 공부하시면 다음 과목을 따라가기 수월합니다. 시스템 분야는 컴퓨터구조 → 운영체제·시스템 프로그래밍 → 네트워크·DB·분산시스템으로, AI 분야는 확률·선형대수 → 머신러닝 → 딥러닝 → 관심 응용과 AI 시스템으로 이어갈 수 있습니다.

미적분·미분방정식·신호처리와 디지털 논리·마이크로프로세서·임베디드 하드웨어는 [전기·전자·통신 과목](전기전자통신과목_ece-courses.md)에서 함께 공부하실 수 있습니다.

## 수학과 전산 기초

| 과목 | 공개 강의·교재 | 수준·권장 선수지식 | 공부 범위·공개 조건 |
| --- | --- | --- | --- |
| 프로그래밍 입문 | [Harvard CS50x](https://cs50.harvard.edu/x/) | 입문·학부<br>프로그래밍 경험이 없어도 시작할 수 있습니다. | C의 메모리와 자료구조에서 Python·SQL·웹 구현까지 연결합니다. 강의·문제는 공개이며 제출 계정과 인증서는 별도입니다. |
| 이산수학·증명 | [MIT 6.042J Mathematics for Computer Science · 2015](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/) | 학부<br>고등학교 수학 이후 논리와 증명 연습부터 진행합니다. | 집합·관계·귀납법·그래프·계수·이산확률을 공부합니다. 영상·교재·노트·문제와 일부 해설이 공개되어 있습니다. |
| 선형대수 | [MIT 18.06 Linear Algebra · 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) | 학부<br>연립방정식과 기본 함수에 익숙하면 좋습니다. | 벡터공간·선형변환·직교·고유값을 컴퓨터과학과 AI 수학의 바탕으로 익힙니다. 강의 영상·문제·시험 자료가 공개되어 있습니다. |
| 확률·확률과정 기초 | [MIT 6.041SC Probabilistic Systems Analysis · 2013](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/) | 학부<br>미적분과 합·적분 계산을 권장합니다. | 확률변수·조건부확률·확률과정·대수의 법칙·추론을 연결합니다. 강의 영상·문제 풀이 영상·과제가 공개되어 있습니다. |
| 통계·추정 | [MIT 18.650 Statistics for Applications · 2016](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/) | 학부<br>확률·미적분·선형대수를 권장합니다. | 통계 모형과 추정·검정의 이론을 데이터 분석과 연결합니다. 영상·슬라이드·문제가 공개되어 있습니다. |
| 수치계산·과학계산 | [MIT 18.335J Introduction to Numerical Methods · 2019](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/) | 대학원 입문<br>선형대수·미적분·프로그래밍을 권장합니다. | 부동소수점·조건수·안정성과 행렬 계산의 오차를 공부합니다. 노트·문제·시험을 제공합니다. |

## 알고리즘과 언어

| 과목 | 공개 강의·교재 | 수준·권장 선수지식 | 공부 범위·공개 조건 |
| --- | --- | --- | --- |
| 자료구조·기본 알고리즘 | [MIT 6.006 Introduction to Algorithms · 2020](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) | 학부<br>Python과 이산수학을 권장합니다. | 자료구조 선택·탐색·정렬·그래프·동적 계획법과 실행 시간 분석을 공부합니다. 강의·노트·문제·시험 자료가 공개되어 있습니다. |
| 알고리즘 설계·분석 | [MIT 6.046J Design and Analysis of Algorithms · 2015](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/) | 학부 심화<br>자료구조·기초 알고리즘·증명·확률을 권장합니다. | 분할 정복·탐욕법·무작위화·동적 계획법과 복잡도 분석을 다룹니다. 강의·보충 강의·노트·문제가 공개되어 있습니다. |
| 고급·근사·온라인 알고리즘 | [MIT 6.854J Advanced Algorithms · 2005](https://ocw.mit.edu/courses/6-854j-advanced-algorithms-fall-2005/) | 대학원 입문<br>알고리즘 설계·증명·확률·선형대수를 권장합니다. | 분할상환 분석·무작위화·흐름·근사·온라인·스트리밍 알고리즘으로 범위를 넓힙니다. 노트·문제·프로젝트를 제공합니다. |
| 프로그래밍 언어·함수형 프로그래밍 | [UW CSE 341 Programming Languages · 2023](https://sites.google.com/cs.washington.edu/cse341spring2023/lecture) | 학부<br>함수·재귀·자료구조를 사용하는 프로그래밍 경험을 권장합니다. | OCaml·Racket으로 클로저·패턴 매칭·타입·객체 지향의 의미를 비교합니다. 공개 슬라이드·읽기 노트·코드를 이용합니다. |
| 컴파일러 | [MIT 6.035 Computer Language Engineering · 2010](https://ocw.mit.edu/courses/6-035-computer-language-engineering-spring-2010/) | 학부 심화<br>자료구조·C 계열 프로그래밍·컴퓨터구조를 권장합니다. | 작은 언어의 컴파일러를 구현하면서 언어 처리 과정을 익힙니다. 강의 노트·Decaf 프로젝트·시험이 공개되어 있습니다. |
| 계산이론·복잡도 | [MIT 18.404J Theory of Computation · 2020](https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/) | 학부 심화·대학원 입문<br>이산수학·증명·알고리즘을 권장합니다. | 오토마타·계산 가능성·환원·시간과 공간 복잡도의 한계를 공부합니다. 강의 영상·노트·문제·시험이 공개되어 있습니다. |
| 논리·프로그램 의미론·형식 검증 | [Software Foundations](https://softwarefoundations.cis.upenn.edu/) | 학부 심화~대학원<br>프로그래밍 경험과 수학적 증명에 대한 익숙함을 권장합니다. | Logical Foundations부터 Rocq를 이용한 증명, 언어 의미론, Hoare 논리와 자료구조 검증으로 이어집니다. 대화형 교재와 연습 코드가 공개되어 있습니다. |
| 타입 이론·프로그래밍 언어 의미론 | [Harper, Practical Foundations for Programming Languages · 2판, 2016](https://www.cs.cmu.edu/~rwh/pfpl/index.html) | 학부 심화~대학원<br>함수형 프로그래밍·이산수학·증명과 기본 언어 이론을 권장합니다. | 정적·동적 의미론·타입 안전성·다형성으로 언어의 동작을 정의하고 증명합니다. 저자의 공개 PDF 발췌본·보충 노트·연습문제를 이용합니다. |
| 컴파일러 최적화·실행 환경 | [Cornell CS6120 Self-Guided Course · 2025 가을](https://www.cs.cornell.edu/courses/cs6120/2025fa/self-guided/) | 대학원<br>기초 컴파일러 구현·자료구조·컴퓨터구조를 권장합니다. | 중간 표현·데이터 흐름·SSA·최적화·메모리 관리를 작은 컴파일러에 구현합니다. 자율 학습용 영상·설명·Bril 코드·과제가 연결되어 있습니다. |
| 프로그램 분석·자동 오류 탐지 | [CMU 17-355/665/819 Program Analysis · 2025](https://cmu-program-analysis.github.io/2025/index.html) | 학부 심화~대학원<br>프로그래밍 언어·자료구조·수학적 증명을 권장합니다. | 추상 해석·포인터 분석·기호 실행·퍼징으로 프로그램의 속성과 오류를 분석합니다. 슬라이드·강의 노트·과제와 프로젝트 안내를 제공합니다. |
| 알고리즘 게임이론·메커니즘 설계 | [Tim Roughgarden CS364A · 2013 가을](https://timroughgarden.org/f13/f13.html) | 대학원 입문<br>알고리즘 설계·확률·증명과 최적화 기초를 권장합니다. | 경매·인센티브·균형·혼잡을 계산 문제로 다룹니다. 대학 강의 영상·강의 노트·연습문제가 공개되어 있습니다. |

## 소프트웨어와 시스템

| 과목 | 공개 강의·교재 | 수준·권장 선수지식 | 공부 범위·공개 조건 |
| --- | --- | --- | --- |
| 소프트웨어 설계·테스트 | [MIT 6.005 Elements of Software Construction · 2008](https://ocw.mit.edu/courses/6-005-elements-of-software-construction-fall-2008/) | 학부<br>객체 지향 프로그래밍과 기본 자료구조를 권장합니다. | 명세·추상화·불변식·테스트·코드 커버리지를 프로그램 구성과 연결합니다. 노트·과제·실습·프로젝트가 공개되어 있습니다. |
| 시스템 프로그래밍 | [SPIN Lab. KOREATECH 공개 강의](https://sites.google.com/view/hpclab/courses) | 학부 · 한국어<br>C 언어·포인터·기본 운영체제를 권장합니다. | 시스템 프로그래밍 목록에서 운영체제 기능을 프로그램이 사용하는 방법을 공부합니다. 공식 연구실 페이지에서 강의 목록과 연결된 YouTube 목록을 찾을 수 있습니다. |
| 컴퓨터구조·메모리 시스템 | [Onur Mutlu Lecture Videos](https://people.inf.ethz.ch/~omutlu/lecture-videos.html) | 학부~대학원<br>디지털 논리·C·기초 구조 이후 수준에 맞는 과목을 고릅니다. | 디지털 설계·컴퓨터구조·메모리 시스템을 기초 강의와 심화 강의로 나눠 공부합니다. 교수 공식 페이지에서 연도별 영상과 강의 자료를 연결합니다. |
| 운영체제 | [SPIN Lab. KOREATECH 운영체제](https://www.youtube.com/playlist?list=PLBrGAFAIyf5rby7QylRc6JxU5lzQ9c4tN) | 학부 · 한국어<br>C 언어·자료구조·컴퓨터구조를 권장합니다. | 프로세스·스레드·메모리·동기화 같은 운영체제 기본 내용을 순서대로 공부합니다. 연구실이 연결한 공개 영상 목록입니다. |
| 운영체제 구현·커널 실습 | [MIT 6.S081 Operating System Engineering · 2020](https://pdos.csail.mit.edu/6.828/2020/schedule.html) | 학부 심화<br>C·컴퓨터구조·기본 운영체제·디버깅을 권장합니다. | xv6로 시스템 호출·페이지 테이블·트랩·잠금·파일시스템을 구현합니다. 수업 일정에 영상·xv6 교재·코드·실습을 연결합니다. |
| 멀티코어·병렬 프로그래밍 | [SPIN Lab. KOREATECH 멀티코어 프로그래밍](https://www.youtube.com/playlist?list=PLBrGAFAIyf5pp3QNigbh2hRU5EUD0crgI) | 학부 심화 · 한국어<br>C·스레드·동기화·컴퓨터구조를 권장합니다. | 여러 코어로 일을 나누는 방법과 동기화·성능 문제를 함께 공부합니다. 연구실의 공개 강의 영상 목록입니다. |
| GPU·병렬 시스템과 성능 | [Stanford CS149 Parallel Computing · 2023 가을](https://gfxcourses.stanford.edu/cs149/fall23) · [공개 강의 첫 영상](https://www.youtube.com/watch?v=V1tINV2-9p4) | 학부 심화<br>C/C++·운영체제·컴퓨터구조를 권장합니다. | SIMD·CUDA·메모리 지역성·캐시 일관성·잠금 없는 동기화와 병렬 성능을 공부합니다. 2023년 강의 영상과 프로그래밍·필기 과제를 이용할 수 있습니다. CUDA 과제에는 NVIDIA GPU가 필요합니다. |
| 웹·모바일 서비스와 개발 도구 | [University of Helsinki Full Stack Open](https://fullstackopen.com/en/) | 학부 심화<br>프로그래밍·웹·DB·Git 기초를 권장합니다. | React·Node.js·API·테스트에서 TypeScript·React Native·CI·컨테이너로 이어집니다. 글 중심 무료 수업과 실습이며 과제 제출에는 GitHub와 제출 시스템을 사용합니다. |

## 데이터·네트워크·보안

| 과목 | 공개 강의·교재 | 수준·권장 선수지식 | 공부 범위·공개 조건 |
| --- | --- | --- | --- |
| 데이터베이스 구현 | [CMU 15-445/645 Database Systems · 2024](https://15445.courses.cs.cmu.edu/fall2024/schedule.html) | 학부 심화·대학원 입문<br>자료구조·운영체제·C++를 권장합니다. | 버퍼 풀·인덱스·질의 실행·트랜잭션·복구를 DBMS 구현과 연결합니다. 영상·슬라이드·노트·프로젝트가 공개되어 있습니다. |
| 고급 데이터베이스 연구 | [CMU 15-721 Advanced Database Systems · 2024](https://15721.courses.cs.cmu.edu/spring2024/schedule.html) | 대학원·학부 심화<br>DBMS 구현·논문 읽기·시스템 성능 분석을 권장합니다. | 현대 분석형 DBMS의 설계 선택을 논문별로 비교하는 읽기 경로입니다. 강의 일정에서 주제별 연구 논문을 읽을 수 있습니다. |
| 컴퓨터 네트워크·TCP 구현 | [Stanford CS144 Computer Networking](https://cs144.github.io/) | 학부 심화<br>C++·자료구조·운영체제를 권장합니다. | 바이트 스트림·TCP 송수신과 네트워크 동작을 단계별 구현 과제로 익힙니다. 공개 과제·교재·일정을 제공합니다. |
| 분산시스템 | [Martin Kleppmann Distributed Systems · 2020](https://martin.kleppmann.com/2020/11/18/distributed-systems-and-elliptic-curves.html) | 학부 심화·대학원 입문<br>기초 컴퓨터과학·운영체제·수학 표기법을 권장합니다. | 분산 실행·복제·동기화·일관성을 짧은 연속 강의와 노트로 공부합니다. 강의 영상·노트·연습문제가 공개되어 있습니다. |
| 컴퓨터 보안·암호 기초 | [UC Berkeley CS161 Computer Security · 2024](https://sp24.cs161.org/) | 학부<br>C·기본 구조·네트워크·확률을 권장합니다. | 메모리 안전·암호·웹·네트워크 보안의 위협과 방어를 연결합니다. 해당 학기 공개 노트·영상·과제를 사용할 수 있습니다. |
| 시스템 보안 연구 | [MIT 6.858 Computer Systems Security · 2014](https://ocw.mit.edu/courses/6-858-computer-systems-security-fall-2014/) | 대학원<br>운영체제·네트워크·보안 입문·시스템 프로그래밍을 권장합니다. | OS·정보 흐름·언어·하드웨어·웹 보안을 논문과 시스템 구현으로 공부합니다. 영상·노트·읽을거리·실습·프로젝트가 공개되어 있습니다. |
| 네트워크 구조·혼잡 제어·연구 | [Stanford CS244 Advanced Topics in Networking · 2025 봄](https://web.stanford.edu/class/cs244/) | 대학원<br>컴퓨터 네트워크·운영체제·논문 읽기를 권장합니다. | 인터넷 구조·혼잡 제어·SDN·패킷 처리·데이터센터 네트워크의 설계 선택을 비교합니다. 공개 읽기 논문·강의 자료·프로젝트 안내를 이용합니다. |
| 현대 암호·프로토콜과 보안 증명 | [Boneh·Shoup, A Graduate Course in Applied Cryptography · v0.6, 2023](https://toc.cryptobook.us/) | 학부 심화~대학원<br>확률·모듈러 연산·알고리즘·수학적 증명을 권장합니다. | 대칭키·공개키 암호·서명에서 영지식 증명·키 교환·안전한 다자 계산으로 이어집니다. 저자가 공개한 PDF 교재와 연습문제로 공부합니다. |
| 차등 개인정보보호 | [Dwork·Roth, The Algorithmic Foundations of Differential Privacy · 2014](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf) | 대학원 입문<br>확률·알고리즘·선형대수와 증명을 권장합니다. | 개인 한 명의 데이터가 결과에 미치는 영향을 제한하는 정의와 잡음 메커니즘·합성·학습 응용을 공부합니다. 저자 공개 교재의 정의·정리·알고리즘을 따라갑니다. |

## 사람·시각·로봇

| 과목 | 공개 강의·교재 | 수준·권장 선수지식 | 공부 범위·공개 조건 |
| --- | --- | --- | --- |
| 인간과 컴퓨터 상호작용 | [MIT 6.831 User Interface Design and Implementation · 2011](https://ocw.mit.edu/courses/6-831-user-interface-design-and-implementation-spring-2011/) | 대학원 입문<br>프로그래밍 경험과 작은 UI 구현 경험을 권장합니다. | 사용자·과업 분석에서 프로토타입·사용성 평가·구현으로 이어집니다. 노트·과제·프로젝트를 제공합니다. |
| 컴퓨터그래픽스 | [MIT 6.837 Computer Graphics · 2012](https://ocw.mit.edu/courses/6-837-computer-graphics-fall-2012/) | 학부<br>선형대수·기초 미적분·프로그래밍을 권장합니다. | 변환·광선 추적·샘플링·조명·곡선·애니메이션을 구현 과제로 공부합니다. 노트·프로그래밍 과제·시험이 공개되어 있습니다. |
| 컴퓨터 애니메이션·물리 시뮬레이션 | [MIT 6.838 Algorithms for Computer Animation · 2002](https://ocw.mit.edu/courses/6-838-algorithms-for-computer-animation-fall-2002/) | 대학원<br>그래픽스·선형대수·미적분·기초 역학·수치계산을 권장합니다. | 키프레임·역기구학·물리 시뮬레이션·최적 제어·동작 데이터를 연결합니다. 읽을거리와 프로젝트를 제공합니다. |
| 컴퓨터비전·시각 딥러닝 | [Stanford CS231n · 2025 봄](https://cs231n.stanford.edu/2025/index.html) · [2025 공개 강의 영상](https://www.youtube.com/playlist?list=PLoROMvodv4rOmsNzYBMe0gJY2XS8AQg16) | 학부 심화·대학원 입문<br>Python·NumPy·미적분·선형대수·확률을 권장합니다. | 이미지 분류·탐지에서 트랜스포머·생성모형·시각 언어모형으로 이어집니다. 2025년 강의 영상·노트·과제를 함께 이용할 수 있습니다. |
| 3차원 비전·기하와 복원 | [Stanford CS231A · 2025 봄](https://web.stanford.edu/class/cs231a/) | 학부 심화·대학원 입문<br>선형대수·미적분·확률·Python과 기초 비전을 권장합니다. | 카메라·투영·스테레오·다중 시점 기하·깊이·움직임과 3차원 장면 복원을 공부합니다. 강의 노트·슬라이드·문제와 실습 코드가 공개되어 있습니다. |
| 로보틱스·운동학·동역학 | [Northwestern Modern Robotics](https://hades.mech.northwestern.edu/index.php/Modern_Robotics) | 학부 심화·대학원 입문<br>선형대수·미적분·기초 역학과 프로그래밍을 권장합니다. | 강체 운동·기구학·동역학·경로 계획·제어·파지를 공부합니다. 저자 공식 페이지에 교재 사전 공개본·영상·코드·연습 자료가 연결되어 있습니다. |

## AI 기초와 심화

| 과목 | 공개 강의·교재 | 수준·권장 선수지식 | 공부 범위·공개 조건 |
| --- | --- | --- | --- |
| AI 탐색·계획·추론 | [UC Berkeley CS188 Introduction to Artificial Intelligence · 2024](https://inst.eecs.berkeley.edu/~cs188/archive/sp24/) | 학부<br>Python·자료구조·이산수학·확률을 권장합니다. | 탐색·게임·논리·계획·불확실성 추론을 머신러닝과 구분해 공부합니다. 해당 학기 영상·슬라이드·노트·프로젝트가 공개되어 있습니다. |
| 머신러닝 | [Stanford CS229 · 2020 여름 노트](https://cs229.stanford.edu/summer2020/syllabus.html) | 학부 심화·대학원 입문<br>선형대수·미적분·확률·프로그래밍을 권장합니다. | 회귀·분류·커널·모형 선택·군집·차원 축소와 강화학습 기초를 공부합니다. 강의 노트·복습 노트·문제를 제공합니다. |
| 딥러닝 입문 | [MIT 6.S191 Introduction to Deep Learning · 2026](https://introtodeeplearning.com/) | 학부 심화·대학원 입문<br>Python·미분·행렬 계산의 기본을 권장합니다. | 신경망 기초에서 비전·언어·생성·강화학습 응용을 실습과 연결합니다. 공식 강의 페이지의 영상·슬라이드·소프트웨어 실습을 이용할 수 있습니다. |
| 자연어처리 | [Stanford CS224N](https://web.stanford.edu/class/cs224n/) | 학부 심화·대학원<br>Python·선형대수·확률·기초 머신러닝을 권장합니다. | 언어 표현·신경망·어텐션·트랜스포머를 언어 과제와 연결합니다. 공개 노트·과제와 2024년 강의 영상 경로를 이용합니다. |
| 강화학습 | [David Silver Reinforcement Learning · 2015](https://davidstarsilver.wordpress.com/teaching/) | 학부 심화·대학원 입문<br>확률·선형대수·기초 머신러닝을 권장합니다. | MDP·동적 계획법·모형 없는 학습·가치함수 근사·정책 기울기를 공부합니다. 저자 강의 페이지의 영상·슬라이드·Easy21 과제·시험 자료가 공개되어 있습니다. |
| 심층 강화학습·모방학습 | [UC Berkeley CS285 · 2023 가을](https://rail.eecs.berkeley.edu/deeprlcourse-fa23/) | 대학원<br>기초 강화학습·딥러닝·확률·선형대수·Python을 권장합니다. | 정책 기울기·가치 학습·모형 기반 학습·모방·오프라인 강화학습을 구현 과제와 연결합니다. 공개 영상·슬라이드·과제·코드를 이용하며 실습에는 GPU를 사용할 수 있습니다. |
| 확률 그래프 모형 | [Stanford CS228 Course Notes](https://ermongroup.github.io/cs228-notes/) | 대학원 입문<br>확률·통계·알고리즘·프로그래밍을 권장합니다. | 베이즈망·마르코프망·정확 및 근사 추론·변분 추론·잠재변수 학습을 공부합니다. 공개 강의 노트를 이용합니다. |
| 딥 생성모형 | [Stanford CS236 Course Notes](https://deepgenerativemodels.github.io/notes/index.html) | 대학원 입문<br>머신러닝·확률·미적분·Python을 권장합니다. | 공개 노트의 자기회귀·VAE·정규화 흐름·GAN을 먼저 공부하고 강의 일정의 후속 주제로 이어갑니다. |
| 최적화 | [Stanford EE364A Convex Optimization](https://web.stanford.edu/class/ee364a/) | 학부 심화·대학원 입문<br>선형대수·미적분·확률·기초 Python을 권장합니다. | 볼록 집합·함수·쌍대성·수치 알고리즘을 최적화 문제 작성과 연결합니다. 공개 슬라이드·교재·CVXPY 예제를 이용합니다. |
| 대규모 데이터 분석·추천 | [Stanford CS246 Mining Massive Data Sets](https://web.stanford.edu/class/cs246/) | 학부 심화·대학원 입문<br>프로그래밍·확률·선형대수·알고리즘 분석을 권장합니다. | Spark·유사도 검색·추천·PageRank·그래프·스트림 처리를 공부합니다. 공개 슬라이드·과제·교재와 이전 MOOC 영상을 이용합니다. |
| 음성 인식·합성·대화 시스템 | [Stanford CS224S · 2025 봄](https://web.stanford.edu/class/cs224s/index.html) | 학부 심화·대학원<br>머신러닝·확률·신호처리 기초와 Python을 권장합니다. | 오디오 분석·음성 인식·음성 합성·대화 모델을 공부합니다. 공개 슬라이드·읽을거리·코드 실습 안내를 이용합니다. |
| 멀티모달 머신러닝 | [CMU 11-777 · 2023 가을](https://multicomp.cs.cmu.edu/mmml-course/fall2023/) | 석·박사 전공<br>머신러닝·딥러닝·확률·선형대수와 Python을 권장합니다. | 언어·음성·영상의 표현·정렬·융합·추론과 모달리티 사이의 전이를 공부합니다. 공식 강의 일정에서 공개 영상·슬라이드·읽을거리를 연결합니다. |

## 학습 이론과 데이터 해석

| 과목 | 공개 강의·교재 | 수준·권장 선수지식 | 공부 범위·공개 조건 |
| --- | --- | --- | --- |
| 통계적 학습 이론·일반화 | [Stanford CS229M/STATS214 · 2021 가을](https://web.stanford.edu/class/stats214/) | 대학원<br>머신러닝·확률·통계·선형대수·최적화와 증명을 권장합니다. | 일반화 오차·균등 수렴·신경망 학습 이론·정규화·분포 적응을 공부합니다. 공식 수업이 연결하는 강의 필기와 이전 학기 강의 노트를 이용합니다. |
| 인과 추론 | [Brady Neal, Introduction to Causal Inference · 2020](https://www.bradyneal.com/causal-inference-course) | 학부 심화·대학원 입문<br>확률 기초와 기초 통계·머신러닝을 권장합니다. | 개입·잠재 결과·교란·인과 그래프·도구 변수로 상관과 인과의 차이를 공부합니다. 저자의 공개 영상·슬라이드·교재를 이용합니다. |
| 정보 검색·검색 순위 | [Stanford CS276 Information Retrieval and Web Search](https://web.stanford.edu/class/cs276/index.html) | 학부 심화·대학원 입문<br>자료구조·알고리즘·확률·통계·Python을 권장합니다. | 역색인·압축·벡터 공간 검색·검색 평가·학습 기반 순위를 공부합니다. 공개 슬라이드·저자 교재·프로그래밍 과제를 이용합니다. |
| 그래프 표현학습·GNN | [Stanford CS224W · 2024 가을](https://snap.stanford.edu/class/cs224w-2024/) | 학부 심화·대학원 입문<br>알고리즘·확률·선형대수·기초 머신러닝을 권장합니다. | 노드 임베딩·그래프 신경망·지식 그래프·링크 예측을 공부합니다. 공개 슬라이드·과제·Colab 실습을 이용합니다. |

## AI 시스템과 연구

| 과목 | 공개 강의·교재 | 수준·권장 선수지식 | 공부 범위·공개 조건 |
| --- | --- | --- | --- |
| ML 시스템·배포·모니터링 | [Stanford CS329S Machine Learning Systems Design · 2022](https://stanford-cs329s.github.io/syllabus.html) | 학부 심화·대학원 입문<br>머신러닝·프레임워크 하나·프로그래밍·확률을 권장합니다. | 데이터·특징·평가·배포·분포 변화·모니터링과 ML 기반 서비스 설계를 연결합니다. 공개 노트·슬라이드·실습을 제공합니다. |
| 언어 모델 구현·학습 시스템 | [Stanford CS336 Language Modeling from Scratch · 2025](https://cs336.stanford.edu/spring2025/) | 대학원·학부 심화<br>능숙한 Python·PyTorch·딥러닝·메모리 계층·선형대수·확률이 필요합니다. | 토크나이저·모델·최적화·GPU 성능·분산 학습·데이터·정렬을 코드 중심으로 공부합니다. 공개 과제 저장소·강의 코드·슬라이드가 있으며 학습을 위한 GPU 비용은 별도입니다. |
| 효율적 딥러닝·TinyML | [MIT 6.5940 · 2024 가을](https://hanlab.mit.edu/courses/2024-fall-65940) | 석·박사 전공<br>딥러닝·Python·컴퓨터구조와 성능 분석을 권장합니다. | 가지치기·양자화·신경망 구조 탐색·추론 최적화로 메모리와 연산량을 줄입니다. 공개 영상·슬라이드·Colab 실습을 제공하며 실습 실행에는 Google 계정을 사용합니다. |
| 딥러닝 가속기·하드웨어 구조 | [MIT 6.5930/1 Hardware Architecture for Deep Learning · 2026 봄](https://csg.csail.mit.edu/6.5930/) | 학부 심화·대학원<br>컴퓨터구조와 신호처리 또는 머신러닝 기초를 권장합니다. | 연산의 하드웨어 배치·데이터 흐름·메모리 이동·희소성·수치 정밀도를 설계와 연결합니다. 공개 강의 노트·읽을거리·실습 안내를 이용합니다. |
| AI 윤리·공정성·사회적 조건 | [Fairness and Machine Learning](https://fairmlbook.org/) | 학부 심화·대학원<br>기초 머신러닝·확률과 논증을 읽는 능력을 권장합니다. | 공정성 지표·인과·분류의 한계와 사회적 맥락을 비교합니다. 저자 공개 교재와 연습문제를 이용할 수 있습니다. |
| 계산생물학·AI 융합 | [MIT 6.047 Computational Biology · 2015](https://ocw.mit.edu/courses/6-047-computational-biology-fall-2015/) | 학부 심화<br>알고리즘·확률·머신러닝 기초와 생물학 용어 복습을 권장합니다. | 알고리즘과 머신러닝을 생물학 데이터 분석 문제에 적용하는 경로입니다. 공개 교재·슬라이드·과제·프로젝트를 제공합니다. |

## 대학원 전공과 연구로 이어가기

알고리즘·언어·시스템·AI 가운데 관심 분야를 고른 뒤, 고급 강의의 읽을거리와 연구실 세미나로 이어가실 수 있습니다. 고급 DB·보안·생성모형 자료에서는 논문의 문제 설정, 실험 조건과 다른 방법의 차이를 비교해 보시면 좋습니다. 석·박사 과정의 세미나·개별 연구·논문 연구는 아래 공식 교육과정의 연구 과목에 연결됩니다. 연구윤리와 논문 작성·발표 자료는 [국내 공개 강의](국내공개강의_korean-courses.md)와 [해외 공개 강의](해외공개강의_global-courses.md)에서 함께 보실 수 있습니다.

## 공식 교육과정과 전공 분류

학부 필수·선택 과목과 대학원 전공·연구 과목을 찾을 수 있는 공식 교육과정입니다.

- [KAIST 전산학부 학부 교과과정](https://cs.kaist.ac.kr/education/undergraduate)
- [KAIST 전산학부 대학원 교과과정](https://cs.kaist.ac.kr/education/graduate)
- [MIT Computer Science and Engineering 6-3](https://catalog.mit.edu/degree-charts/computer-science-engineering-course-6-3/)
- [MIT Artificial Intelligence and Decision Making 6-4](https://catalog.mit.edu/degree-charts/artifical-intelligence-decision-making-course-6-4/)
- [CMU 머신러닝 석사 교육과정](https://ml.cmu.edu/academics/machine-learning-masters-curriculum)
- [MIT EECS Technical Qualifying Evaluation · Spring 2026](https://www.eecs.mit.edu/wp-content/uploads/2026/01/TQE-Grid-effective-spring-2026.pdf)

자료 기준: 2026-10-23.
