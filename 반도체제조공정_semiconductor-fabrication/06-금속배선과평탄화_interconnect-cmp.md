# 금속 배선과 평탄화 | Interconnects and Chemical Mechanical Planarization

[공정 목차](README.md)

트랜지스터를 만들어도 서로 연결하지 않으면 회로가 되지 않습니다. 금속 배선은 신호와 전원을 전달하고, 절연막은 서로 다른 배선을 분리합니다. 칩 안의 배선은 평면에 그린 선 하나가 아니라 접촉부·수직 연결부·여러 높이의 금속선·절연막·확산 방지막이 함께 쌓인 구조입니다. 이 글에서는 이 구조를 만드는 과정과 저항·정전용량·신뢰성의 관계를 설명합니다.

금속 배선 공정은 ‘금속을 뿌린 뒤 회로 모양으로 깎는다’는 한 가지 순서로 설명할 수 없습니다. 알루미늄을 식각하여 남기는 방식과 구리용 홈을 먼저 만든 뒤 채우는 다마신 방식의 차이를 이해해야 합니다. 수치 예제는 별도 표시한 설명용 가정이며 실제 제품의 치수·성능·레시피가 아닙니다. 연구 시연, 장비 공급사의 제품 발표, 제조사의 양산 보고는 2026-10-26에 확인한 자료 범위에서 구분합니다.

## 1. 접촉부·비아·금속선과 MOL·BEOL

접촉부(contact)는 소자의 소스·드레인·게이트 같은 단자와 위쪽 배선망을 잇는 구조입니다. 비아(via)는 주로 서로 다른 높이의 금속층을 연결하는 구조입니다. 금속선(line)은 같은 층에서 옆 방향으로 전류를 운반합니다. 구조가 작아질수록 접촉부와 비아의 저항도 무시하기 어렵습니다. 긴 금속선의 저항만 줄였다고 전체 경로의 저항이 같은 비율로 줄지는 않습니다.

중간 공정(MOL, middle of line)은 트랜지스터와 배선 사이의 접촉·국소 연결을, 배선 공정(BEOL, back end of line)은 다층 금속 배선망을 가리킬 때 사용합니다. 업체와 기술에 따라 경계와 층 이름이 다르므로 어떤 금속층 번호를 보편적인 MOL의 끝으로 정할 수는 없습니다. imec은 FEOL의 소자, MOL의 접촉부, BEOL의 다층 연결을 구분합니다. [imec, A view on the logic technology roadmap의 Key parts of the logic chip](https://www.imec-int.com/en/articles/view-logic-technology-roadmap)

| 구성 | 맡는 역할 | 주로 보는 문제 |
|---|---|---|
| 소스/드레인 접촉 계면 | 반도체에서 금속으로 전류를 전달합니다. | 계면 장벽, 접촉 면적, 오염·산화막 |
| 접촉 플러그 | 소자 단자에서 배선층까지 통로를 채웁니다. | 빈틈·접합 저항·치수 분포 |
| 비아 | 배선층 사이를 연결합니다. | 바닥 잔사, 정렬, 전류 집중, 단선 |
| 국소 배선 | 가까운 소자와 셀을 연결합니다. | 작은 단면의 저항, 밀집한 배선의 정전용량 |
| 상부·전역 배선 | 긴 거리 신호·클록·전원을 전달합니다. | 지연·전압 강하·전류 용량·층간 연결 |
| 절연·캡·배리어 | 배선을 분리하고 원자 이동을 억제합니다. | 유전 파괴·누설·접착·확산 |

상부 배선이 하부 배선보다 넓고 두꺼운 구조가 흔한 이유는 긴 거리의 저항과 전원 전류를 감당하기 위해서입니다. 그러나 모든 제품이 같은 층 수·치수·방향 규칙을 사용하는 것은 아닙니다. 칩 내부 배선과 패키지의 재배선층(RDL), 실리콘 관통 비아(TSV)도 길이와 재료·공정 조건이 다르므로 하나의 치수 범위로 묶지 않습니다.

## 2. 알루미늄과 구리의 패터닝이 다른 이유

알루미늄 배선의 대표적인 설명 흐름은 금속막 형성 → 포토 패턴 → 금속 식각 → 마스크 제거 → 절연막 형성입니다. 이를 감산(subtractive) 방식이라고 합니다. 남길 선 외의 금속을 제거하여 무늬를 만듭니다. 알루미늄·알루미늄 합금은 여러 제품과 층에서 계속 쓰일 수 있으므로 구리 도입을 모든 알루미늄의 완전한 소멸로 이해하지 않습니다.

구리는 벌크 상태에서 낮은 저항률을 갖지만, 일반적인 미세 배선용 건식 식각 조건에서 휘발성이 충분한 반응 생성물을 만들고 안정적으로 배출하는 일이 어렵습니다. 이 때문에 절연막에 선과 비아의 공간을 먼저 만들고 구리로 채운 뒤 윗면의 불필요한 금속을 제거하는 다마신(damascene) 방식이 널리 사용되었습니다. 구리가 어떤 조건에서도 식각되지 않는다는 뜻은 아닙니다. 생산에 적합한 미세 패턴 공정으로 구현하기 어렵다는 구분이 필요합니다. [University of Texas at Austin, Etching 강의의 Etch summary, 슬라이드 25](https://weewave.mer.utexas.edu/DPN_files/courses/FabLab/lecture_ovrhds/440_etch.pdf)

구리는 주변 재료와 섞이거나 절연 특성을 해칠 수 있어 확산 억제 구조가 중요합니다. IBM의 구리 배선 역사 자료는 실리콘의 전기적 성질을 손상시키는 구리의 이동과 다마신 통합을 설명합니다. 1997년 발표와 실제 제품 출하 시점을 구분해야 하며, 당시 제품의 성능 향상률을 오늘날 모든 구리 배선의 효과로 옮겨서는 안 됩니다. [IBM, Copper interconnects의 Ensuring the safety of copper 및 Full-scale manufacturing](https://www.ibm.com/history/copper-interconnects)

## 3. 구리 배리어·라이너·시드의 역할

배리어(barrier)는 구리 원자가 주변 재료로 퍼지는 것을 억제하는 층입니다. 라이너(liner)는 구리가 잘 붙고 성장·이동하도록 계면을 만드는 층입니다. 시드(seed)는 후속 전기 도금을 시작할 연속적인 전도 경로를 제공합니다. 실제 막 하나가 두 역할을 겸할 수도 있고 공정에 따라 명칭의 경계가 달라질 수 있으므로, 이름보다 맡는 기능을 확인해야 합니다.

전통적인 예로 TaN·Ta 계열 막과 구리 시드를 들 수 있지만, 모든 기술이 같은 조합을 쓰지는 않습니다. 배리어가 연속적이지 않으면 확산 위험이 커지고, 너무 두꺼우면 정작 전류를 잘 흘리는 구리의 단면이 줄어듭니다. 시드가 끊기거나 바닥에 충분히 이어지지 않으면 도금이 불균일하게 시작할 수 있습니다. Applied Materials의 2005년 공식 발표는 TaN 배리어와 Cu 시드를 서로 다른 기능의 층으로 설명합니다. 이는 역사적인 공정 사례이며 최신의 모든 배선 재료를 뜻하지 않습니다. [Applied Materials, Endura CuBS 100th shipment, 2005-08-15](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-strengthens-leadership-300mm-copper)

작은 배선에서는 계면의 저항을 줄이기 위해 진공을 유지한 채 세정·표면 처리·선택 증착·금속 형성을 이어 가는 통합도 사용합니다. Applied의 IMS 설명은 여러 공정을 한 플랫폼에 결합하고 비아 바닥의 높은 저항 성분을 줄이는 접근을 제시합니다. 이는 그 공급사의 공정 해법이며, 모든 비아에 배리어가 없어도 된다는 일반 규칙은 아닙니다. [Applied Materials, Integrated Materials Solution의 Endura Copper Barrier Seed 사례](https://www.appliedmaterials.com/us/en/semiconductor/solutions-and-software/ims.html)

## 4. 듀얼 다마신의 전체 흐름

듀얼 다마신(dual damascene)은 선을 위한 트렌치(trench, 긴 홈)와 비아를 위한 구멍을 절연막에 형성한 뒤 금속으로 함께 채우는 통합 방식입니다. 듀얼이라는 이름이 포토 공정 한 번, 식각 한 번, 연마 한 번만 수행한다는 뜻은 아닙니다. 비아를 먼저 만드는 흐름과 트렌치를 먼저 만드는 흐름 등 여러 조합이 있습니다.

아래 순서는 개념을 이해하기 위한 대표 흐름입니다. 정지막·하드 마스크·캡의 구성과 제거 순서는 기술마다 다릅니다.

1. 아래 배선 위에 캡과 다음 층의 절연막을 형성합니다.
2. 포토와 식각으로 비아·트렌치 형상을 만듭니다.
3. 마스크·부산물을 제거하고 아래 금속과 만나는 바닥을 준비합니다.
4. 배리어·라이너·시드 등 필요한 계면층을 형성합니다.
5. 구리를 채워 홈과 구멍 위까지 과잉 금속층을 만듭니다.
6. 열처리 등 필요한 막 안정화 과정을 거칩니다.
7. CMP로 과잉 구리와 불필요한 윗면 계면층을 제거하여 이웃 배선을 분리합니다.
8. 세정·건조와 결함·두께·전기 확인 후 보호막과 다음 배선층을 형성합니다.

금속을 채운 직후에는 절연막 윗면에도 전도막이 이어져 이웃 선이 연결되어 있을 수 있습니다. CMP가 이 막을 제거해야 설계한 선들만 남습니다. 반대로 너무 많이 제거하면 선과 절연막의 높이, 구리 단면, 다음 층의 비아 연결에 영향을 줍니다. 따라서 CMP는 보기 좋게 표면을 다듬는 작업이 아니라 전기적 분리와 다층 적층을 동시에 만드는 공정입니다.

## 5. 구리 전기 도금과 빈틈 없는 채움

전기화학 증착(ECD, electrochemical deposition)은 전극에서 전자를 전달받은 금속 이온이 고체 금속으로 바뀌는 반응을 이용합니다. 구리의 단순화한 반쪽 반응은 Cu²⁺+2e⁻→Cu입니다. 용액이 공급하는 구리 이온, 전류 분포, 표면 상태, 첨가제의 흡착이 성장 위치와 속도에 영향을 줍니다.

컨포멀하게 모든 벽을 같은 두께로 덮기만 하면 입구가 먼저 닫혀 내부에 빈 공간이 갇힐 수 있습니다. 따라서 바닥에서 위쪽으로 잘 채워지도록 하는 슈퍼필링(superfilling) 원리가 중요합니다. 첨가제와 표면 형상에 따른 반응 차이를 활용하는 방식입니다. IBM 연구진의 원 논문 초록은 단순한 컨포멀 피복보다 유리한 채움과 도금 첨가제의 관계를 설명합니다. [Andricacos 외, Damascene copper electroplating for chip interconnections, IBM J. Res. Dev., 1998, Abstract](https://research.ibm.com/publications/damascene-copper-electroplating-for-chip-interconnections)

보이드(void)는 비어 있는 내부 공간이고, 심(seam)은 양쪽에서 자란 막이 만나는 자리에 생기는 선 모양의 틈 또는 경계입니다. 단면 한 장에서 큰 보이드가 보이지 않는다고 전체 비아에 문제가 없다고 할 수 없습니다. 전기 저항과 비아 체인 시험, 여러 위치의 단면, 결함 분석을 연결해야 합니다. Lam은 SABRE ECD 제품 설명에서 높은 종횡비 구조의 채움, 낮은 결함과 저항을 함께 과제로 제시합니다. [Lam Research, SABRE의 Industry Challenges](https://www.lamresearch.com/product/sabre/)

## 6. CMP의 화학과 기계 작용

화학 기계적 평탄화(CMP, chemical mechanical planarization)는 표면의 화학 반응과 패드·미세 입자의 기계적 작용을 결합해 재료를 제거합니다. 슬러리(slurry)는 미세 입자와 화학 성분이 들어 있는 연마액입니다. 웨이퍼를 잡는 헤드, 패드가 놓인 플래튼, 연마액 공급, 패드 상태를 유지하는 부분과 후속 세정이 결과에 관여합니다. EBARA는 회전하는 패드 위에 웨이퍼를 눌러 연마액과 함께 평탄화하고 세정·건조를 통합하는 구조를 설명합니다. [EBARA, Nano-level polishing technique that supports semiconductor](https://ebara.com/global-en/technology/information/polishing-technology-ex/)

금속 CMP에서는 표면을 반응시키는 성분과 과도한 부식을 억제하는 성분, 반응층을 제거하는 기계 작용의 균형이 중요합니다. 절연막 CMP와 금속 CMP에 같은 화학을 그대로 적용하지 않습니다. 구리의 벌크 제거, 배리어 제거, 표면 높이 조절 등 목적에 따라 단계가 나뉠 수 있습니다. 많이 누르거나 오래 연마하면 빨리 끝난다는 단순한 설명은 잔사·부식·디싱·스크래치의 조건을 놓칩니다.

평탄화는 제거량만이 아니라 높은 곳과 낮은 곳의 차이를 줄이는 일입니다. 웨이퍼 전체에서 평균 제거량이 맞아도 특정 패턴 영역의 높이 차이가 크면 다음 포토 공정의 초점과 막 두께, 연결에 문제가 생길 수 있습니다.

### 디싱과 에로전

디싱(dishing)은 금속선 표면이 주변 절연막보다 오목하게 내려간 상태를 말합니다. 에로전(erosion)은 패턴이 밀집한 영역에서 금속과 절연막을 포함한 영역의 높이가 주변 기준보다 낮아지는 현상을 뜻합니다. 하나는 선 내부 높이 차이에, 다른 하나는 패턴 영역의 높이 손실에 주목하므로 같은 말로 쓰지 않습니다.

패턴 밀도·선폭·패드 거동·연마 선택비·과연마가 영향을 줄 수 있습니다. 한국정밀공학회에 발표된 텅스텐 CMP 연구는 디싱·에로전으로 배선 단면이 줄고 저항이 증가하는 문제와 패턴 밀도·크기의 영향을 다룹니다. 이 연구의 특정 연마재 결과를 구리·Mo의 모든 CMP에 적용하지 않습니다. [박범영 외, 텅스텐 CMP에서 디싱 및 에로젼 결함 감소에 관한 연구, 2005, Abstract](https://jkspe.or.kr/journal/view.php?number=3234)

## 7. 배선의 저항과 정전용량

저항률 ρ는 재료가 전류 흐름을 방해하는 정도이고, 저항 R은 재료와 구조를 함께 반영합니다. 길이 L, 폭 w, 높이 h인 균일한 직사각형 도체를 가정하면 다음과 같습니다.

```text
R = ρL / A = ρL / (wh)
```

같은 재료를 사용해도 단면이 작아지면 저항이 커집니다. 아주 좁은 배선에서는 전자가 표면·계면·결정립 경계에서 산란하는 영향 때문에 유효 저항률도 달라질 수 있습니다. 벌크 구리의 낮은 저항률만 표에 넣고 나노 배선의 저항까지 결론 내릴 수 없는 이유입니다. 배리어·라이너가 차지하는 단면과 실제 구리의 유효 저항률을 동시에 봐야 합니다.

배선 간 정전용량 C는 전압 변화에 따라 전하를 저장하는 정도입니다. 정전용량이 크면 신호를 바꿀 때 더 많은 전하가 필요합니다. 배선과 다른 배선 또는 접지 사이의 거리·겹침 면적·절연막이 영향을 줍니다. 실제 배선은 위아래·옆 방향 전기장이 섞이므로 평행판 하나로 정확히 계산할 수는 없지만, 원리 모형은 다음과 같습니다.

```text
C ≈ ε0 k A_overlap / d
```

여기서 k는 진공에 대한 상대 유전율입니다. 다른 조건이 같다면 k를 낮추거나 거리를 늘리면 정전용량을 줄일 수 있습니다. 저항과 정전용량이 결합하면 신호 전파에 지연이 생깁니다. 긴 균일 배선에서는 단위 길이 저항 r와 정전용량 c가 있을 때 전체 배선 RC가 길이 제곱에 비례하는 모형이 나옵니다. 실제 타이밍에는 드라이버·수신기·비아·인접 신호·버퍼 배치가 들어가므로 RC 곱을 곧바로 제품의 지연 시간으로 쓰지는 않습니다.

### low-k와 gate high-k의 목적은 다릅니다

배선 사이 low-k 절연막은 원하지 않는 정전용량을 줄이는 데 쓰입니다. 게이트의 high-k 절연막은 게이트가 채널에 전기장을 전달하는 데 필요한 정전용량을 확보하면서 물리적 막 두께와 누설을 함께 관리하는 데 쓰입니다. 같은 k를 다루지만 위치와 목적이 다릅니다. ‘유전율은 낮을수록 언제나 좋다’는 규칙은 성립하지 않습니다.

low-k 막에 빈 공간을 도입하면 유효 유전율을 낮출 수 있지만 기계적 강도·흡습·플라스마 손상·금속 확산·세정과의 적합성을 함께 봐야 합니다. Applied의 2024년 기술 발표는 낮은 정전용량과 기계적 강도를 별도 요구로 제시합니다. 제품 발표의 개선율은 특정 비교 대상의 값이므로 이 글의 일반 계산에는 사용하지 않습니다. [Applied Materials, SEMICON West 2024, Black Diamond low-k 설명](https://ir.appliedmaterials.com/static-files/6950cee5-f84d-4b3e-a9f4-39901093ae67)

## 8. 전기 이동·전압 강하·열의 연결

전기 이동(EM, electromigration)은 전류가 흐를 때 금속 원자의 이동이 누적되어 빈 공간이나 돌출을 만드는 현상입니다. 단순히 전자가 흐르는 것과 금속 원자가 이동하는 것을 구분해야 합니다. 원자 이동이 어느 경로로 일어나는지는 결정립·계면·온도·응력·재료에 영향을 받습니다. 구리도 전기 이동에서 자유롭지 않습니다.

전류 밀도 J=I/A입니다. 같은 전류를 더 작은 단면으로 보내면 전류 밀도가 커집니다. 비아 바닥의 작은 접촉 면적이나 모서리에서는 전류가 몰리는 현상도 중요합니다. IBM의 원 연구는 배선 단면과 전기 이동 수명, 음극 쪽 보이드와 양극 쪽 돌출을 다룹니다. [Hu 외, Scaling effect on electromigration in on-chip Cu wiring, IITC 1999, Abstract](https://research.ibm.com/publications/scaling-effect-on-electromigration-in-on-chip-cu-wiring)

전원 배선의 저항은 IR 전압 강하를 만듭니다. 같은 전류에서 R이 커지면 소자에 도달하는 전압이 낮아집니다. 저항에서 발생하는 열은 P=I²R입니다. 국소 온도가 오르면 저항과 원자 이동이 함께 바뀔 수 있으므로 배선의 전기·열·신뢰성을 따로 볼 수 없습니다.

전기 이동 가속 시험은 높은 온도와 전류 밀도 등으로 실패를 관찰하고 사용 조건과의 관계를 모형화합니다. 가속 조건과 수명 분포, 실패 기준, 활성화 에너지의 적용 범위가 필요합니다. TSMC의 2000년 논문 소개는 특정 듀얼 다마신 시험에서 비아 바닥의 실패와 공정 의존성을 설명합니다. 그 자료의 외삽 수명을 오늘날 모든 칩의 수명으로 말할 수 없습니다. [TSMC Research, Reliability of dual damascene Cu metallization, 2000 요약](https://research.tsmc.com/page/on-chip-interconnect/20.html)

## 9. Co·Ru·Mo와 새로운 배선 통합

기존 재료를 바꾸는 판단은 벌크 저항률 순위만으로 할 수 없습니다. 좁은 단면의 유효 저항률, 필요한 배리어 두께, 채움과 식각 가능성, 계면 저항, 전기 이동, 비용·열 이력을 함께 비교해야 합니다. 한 재료가 모든 층에서 구리를 대체할 이유도 없습니다. 작은 접촉부와 긴 상부 배선은 요구가 다릅니다.

| 사례 | 공개 자료가 보여 주는 것 | 확대하면 안 되는 결론 |
|---|---|---|
| Co 국소 배선 | Intel의 IEDM 2017 논문은 10 nm 기술의 일부 국소 배선층에 Co를 사용한 구조를 보고합니다. | Co가 모든 구리층을 대체했다는 뜻은 아닙니다. |
| RuCo 라이너와 Cu | Applied는 얇은 RuCo 라이너 위 구리의 공간과 리플로를 다루는 제품을 소개합니다. | Ru가 라이너에 들어갔다는 사실을 배선 전체가 순수 Ru라는 뜻으로 읽지 않습니다. |
| Ru 직접 식각·세미 다마신 | imec은 연구 구조에서 Ru 선과 자가 정렬 비아를 포함한 통합을 시연합니다. | 연구 웨이퍼의 구조 수율을 상용 칩 다이 수율로 바꾸지 않습니다. |
| Mo 접촉부 | Applied의 2026년 글은 작은 접촉부의 Mo 채움·CMP·계측 개발 사례를 설명합니다. | 모든 논리·메모리 제조사가 Mo를 양산 채택했다는 근거는 아닙니다. |

Co 사례에서는 접촉부와 BEOL 배선층의 기준을 나누어야 합니다. 논문 본문은 W 접촉 금속을 Co로 바꾼 구조를 설명하고, INTERCONNECTS 절에서는 최하부 두 배선층 M0·M1에 Co를 도입했다고 설명합니다. 초록의 ‘세 개 국소 연결층’을 BEOL 금속선 세 층과 같은 기준으로 세지 않습니다. [Auth 외, IEDM 2017, PDF 1~2쪽의 접촉부와 INTERCONNECTS](https://people.eecs.berkeley.edu/~pister/147fa21/Resources/Intel%2010nm%20IEDM2017.pdf), [출판사 서지](https://doi.org/10.1109/IEDM.2017.8268472)

RuCo 라이너 제품은 벌크 구리를 유지하면서 계면층이 차지하는 공간과 구리의 재배치를 다루는 접근입니다. 반면 Ru 세미 다마신(semi-damascene)은 금속을 직접 식각하여 선을 만들고 절연막 채움과 비아 형성을 결합하는 통합 방향입니다. 이름이 비슷한 금속 변화라도 공정 순서와 목적은 다릅니다. [Applied Materials, Endura CuBS Volta Ruthenium CVD](https://www.appliedmaterials.com/us/en/product-library/endura-cubs-volta-ruthenium.html), [imec, 18 nm pitch semi-damascene의 공정 흐름](https://www.imec-int.com/en/articles/imec-demonstrates-semi-damascene-interconnects-fully-self-aligned-vias-18nm-metal-pitch)

imec은 2025년 6월 3일 16 nm 피치 Ru 선의 연구 결과를 발표했습니다. 여기서 피치는 선 하나의 폭이 아니라 반복 구조의 간격입니다. 발표의 평균 선 저항 656 Ω/μm와 16 nm 피치 구조에서 목표 저항을 만족한 비율 40%는 특정 시험 구조의 보고값입니다. 더 큰 피치에서 보고한 웨이퍼 수준 구조 수율과도 조건이 다릅니다. 이 글은 이를 상용 양산 완료나 전체 칩 수율로 표현하지 않습니다. [imec, 16 nm pitch Ru lines, 2025-06-03의 결과와 조건](https://www.imec-int.com/en/press/imec-demonstrates-16nm-pitch-ru-lines-record-low-resistance-obtained-using-semi-damascene)

Mo의 경우도 재료의 가능성과 양산 채택을 분리합니다. Applied의 2026년 1월 5일 글은 Mo 접촉부 개발에서 과채움·미채움·디싱·돌출을 공정별 계측으로 찾는 사례를 제시합니다. 이 자료가 직접 보여 주는 것은 공급사의 개발·계측 통합이며, 고객·층·제품별 양산 범위는 이 글에서 확인하지 않았습니다. [Applied Materials, Co-optimized Process and Metrology Accelerates Molybdenum Contact Development](https://www.appliedmaterials.com/us/en/newsroom/blogs/cooptimized-process-metrology-accelerates-molybdenum-contact-development.html)

## 10. 후면 전력 공급

후면 전력 공급(backside power delivery)은 전원 전달의 일부를 트랜지스터가 있는 웨이퍼의 뒤쪽 경로로 옮겨 앞면 신호 배선과 전원 배선의 공간 경쟁을 줄이는 접근입니다. 앞면의 신호 배선이 전부 없어지거나 모든 TSV가 후면 전력 공급이 되는 것은 아닙니다. 트랜지스터까지 전력을 내리는 연결, 웨이퍼 박막화·정렬·기계적 지지·열 관리가 함께 필요합니다.

Intel은 PowerVia를 자사의 후면 전력 공급 방식으로 설명합니다. 2025년 연차보고서는 Intel 18A가 2025년 말 대량생산에 들어갔으며 RibbonFET과 PowerVia를 도입했다고 보고합니다. 따라서 이 사례를 미래의 연구 개념으로만 쓰는 것도 정확하지 않습니다. 다만 Intel의 양산 보고를 모든 제조사의 채택, 고객별 수율, 모든 제품에서의 동일한 성능 향상으로 넓혀 쓰지 않습니다. [Intel 2025 Form 10-K, Our Business의 Process Technology](https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000011/intc-20251227.htm), [Intel 18A 공식 페이지, PowerVia](https://www.intel.com/content/www/us/en/foundry/process/18a.html)

후면 경로는 전류를 공급하는 선을 더 자유롭게 설계할 여지를 주지만 연결부의 저항·정렬 오차·신뢰성·추가 제조 단계도 평가해야 합니다. 유리한 한 항목만 비교해서 기존 배선 구조보다 언제나 더 싸거나 더 빠르다고 결론 내리지는 않습니다.

## 11. 결함과 계측으로 공정을 분리하기

| 관찰 | 가능한 원인 | 분리에 필요한 확인 |
|---|---|---|
| 비아 저항이 높음 | 바닥 잔사·산화막, 작은 접촉 면적, 두꺼운 계면층, 보이드 | 단면과 계면 조성, 비아 체인·접촉 저항 측정 |
| 이웃 선 단락 | CMP 후 윗면 금속 잔류, 식각·도금 브리지, 절연 파괴 | 연마 직후 표면·높이와 전기 누설 비교 |
| 선 저항이 높음 | 작은 CD·두께, 디싱, 불순물·결정립, 내부 빈 공간 | 단면·형상·저항을 같은 위치에서 비교 |
| 지연·전력 증가 | 저항 증가, 절연막 손상·흡습으로 C 증가, 배선 길이 증가 | R과 C를 나눈 구조 시험 및 배선 경로 분석 |
| 열·전류 스트레스 후 단선 | 전기 이동·응력 이동·초기 보이드 성장 | 시간별 저항·온도, 실패 단면·원자 이동 경로 |
| 스크래치·박리 | 입자·패드 상태, 접착 불량, 연마 하중·막 응력 | 표면 결함 지도, 계면 상태, 처리 순서 |

4단자 저항 측정은 측정선·접촉의 영향을 줄여 시험 구조의 저항을 보는 데 유용합니다. 비아 체인은 많은 비아를 직렬로 연결하여 연결 품질을 민감하게 볼 수 있지만, 높은 저항 하나만으로 모든 비아가 조금씩 나빠졌는지 일부만 크게 나빠졌는지 구분할 수는 없습니다. 분포와 개별 구조 분석을 함께 봐야 합니다.

AFM·프로파일 계측은 높이 차이를, 단면 SEM/TEM은 선·비아의 형상과 계면을, 조성 분석은 잔류 원소와 계면층을 보여 줍니다. 각각 공간 범위와 시료 준비의 영향이 다릅니다. 한 단면에서 보이드가 보이지 않는 결과와 전체 전기 시험에서 불량이 나온 결과는 동시에 가능하며, 먼저 표본 위치와 전기 경로가 일치하는지 확인해야 합니다.

배선 재료를 바꿀 때에는 저항만 비교하지 않습니다. 같은 설계 폭·높이·피치인지, 배리어·라이너를 포함한 전체 단면인지, 접촉 저항이 포함되는지, 단위 길이 Ω/μm인지 저항률 μΩ·cm인지 구분해야 합니다. 비교 조건이 다르면 더 낮은 숫자가 더 나은 공정을 뜻하지 않을 수 있습니다.

## 12. 자체 계산 예제

다음 값은 모두 설명용 가정입니다. 벌크 재료의 표준값 또는 특정 제품의 실제 치수·측정값으로 사용하지 않습니다.

### 예제 1: 배리어가 차지하는 단면

트렌치의 폭 24 nm, 높이 48 nm를 가정합니다. 양쪽 측벽과 바닥에 각각 3 nm 두께의 계면층이 있고, 윗면은 CMP로 열린 단면이라고 단순화합니다. 계면층의 전도 기여는 무시하고 구리만 전류를 전달한다고 둡니다.

1. 전체 트렌치 단면은 24×48=1,152 nm²입니다.
2. 구리의 폭은 24−2×3=18 nm이고 높이는 48−3=45 nm입니다.
3. 구리 단면은 18×45=810 nm²입니다.
4. 전체 중 구리 비율은 810/1,152=70.31%입니다.
5. 같은 구리 저항률이라면 계면층이 없는 이상적 단면에 비해 선 저항은 1,152/810≈1.422배입니다.

높이에서도 위아래 두께를 모두 빼려면 윗면에도 같은 두께의 비전도층이 있다는 가정이 필요합니다. 단면 그림 없이 막 두께를 일률적으로 두 번 빼면 잘못 계산할 수 있습니다. 실제 라이너는 전도성이 있으므로 정확한 계산에는 병렬 전도와 계면 효과를 반영해야 합니다.

### 예제 2: 유효 저항률과 선 저항

예제 1의 구리 단면, 길이 2 μm, 유효 저항률 4 μΩ·cm를 가정합니다. 이 저항률은 크기 효과를 포함했다고 둔 설명값입니다.

```text
ρ = 4×10⁻⁸ Ω·m
L = 2×10⁻⁶ m
A = 810×10⁻¹⁸ m²
R = ρL/A ≈ 98.77 Ω
```

계면층을 줄여 구리 단면이 966 nm²가 되고 저항률은 그대로라면 R≈82.82 Ω입니다. 다만 실제로 계면층을 줄였을 때 구리의 결정성과 신뢰성도 바뀔 수 있으므로, 단면 증가만으로 제품 저항 감소를 확정하지 않습니다.

### 예제 3: RC와 길이

균일 배선의 단위 길이 저항 r=40 Ω/μm, 단위 길이 정전용량 c=0.20 fF/μm, 길이 L=10 μm를 가정합니다. 드라이버와 수신기, 비아는 제외합니다.

1. 전체 R=rL=400 Ω입니다.
2. 전체 C=cL=2 fF입니다.
3. RC=400×2×10⁻¹⁵=0.8 ps입니다.
4. 이상적인 균일 분포 RC 선로의 한쪽 구동·끝단 관찰에 대한 Elmore 지연 모멘트는 r c L²/2=0.4 ps입니다. 이는 특정 임계 전압 도달 시간과 동일한 정의는 아닙니다.
5. 길이만 두 배이면 R과 C가 각각 두 배여서 RC와 이 지연 모멘트는 네 배가 됩니다.

단순한 RC 곱과 실제 신호의 임계값 도달 시간을 구분하려고 두 값을 함께 제시했습니다. 실제 타이밍 분석에는 송수신 회로와 다른 배선의 결합이 필요합니다.

### 예제 4: 전류 밀도와 디싱

유효 도체 단면이 1,000 nm², 전류가 10 μA라고 가정합니다. 1 nm²=10⁻¹⁴ cm²이므로 단면은 10⁻¹¹ cm²입니다. J=10⁻⁵/10⁻¹¹=10⁶ A/cm²입니다.

디싱으로 도체 단면이 800 nm²가 되고 전류가 같으면 전류 밀도는 1.25×10⁶ A/cm²로 25% 증가합니다. 저항률과 길이도 같다고 가정하면 저항 역시 25% 증가합니다. 이 값은 허용 전류 밀도 기준이 아닙니다. 수명 판단에는 재료·온도·형상·스트레스 조건이 더 필요합니다.

### 예제 5: low-k 변화의 한계

평행판 모형에서 k가 3.0에서 2.5로 줄고 모든 기하학적 조건이 같다면 정전용량은 2.5/3.0=0.8333배, 약 16.67% 감소합니다. 그런데 배선 간 거리가 동시에 20% 줄어 d_new=0.8d_old가 되면 C_new/C_old=(2.5/3.0)/0.8≈1.0417입니다. 유전율이 낮아져도 이 모형의 정전용량은 약 4.17% 증가합니다. 재료의 k만 보고 스케일링 후 배선 C의 방향을 정할 수 없는 이유입니다.

### 예제 6: 전압 강하와 발열

전원 경로 저항 0.2 Ω, 전류 0.5 A를 가정하면 전압 강하는 0.1 V이고 저항에서의 전력은 0.05 W입니다. 경로 저항을 0.1 Ω으로 줄이고 전류를 유지하면 각각 0.05 V와 0.025 W가 됩니다. 후면 전력 공급이 특정 제품에서 이 값을 달성했다는 뜻은 아니며, 전원 배선 저항을 줄이려는 물리적 이유를 보여 주는 계산입니다.

## 13. 연습문제와 해답

### 문제

1. 접촉부·비아·금속선의 역할을 구분하고, 긴 선의 저항만 측정해서는 놓치는 두 항목을 적어 보십시오.
2. 폭 30 nm, 높이 50 nm 트렌치에 측벽·바닥 2 nm의 계면층을 넣었습니다. 윗면은 열려 있고 계면층 전도는 무시할 때 구리 단면을 구해 보십시오.
3. 같은 재료·길이에서 도체 단면이 20% 감소하면 저항은 몇 % 증가하는지 계산해 보십시오.
4. 16 nm 피치라는 표현을 선폭 16 nm로 바꿔 써도 되는지 판단해 보십시오.
5. CMP 후 이웃 금속선이 단락되었습니다. 평균 막 두께만 확인하면 원인을 알 수 있는지 설명해 보십시오.
6. ‘구리보다 벌크 저항률이 높은 금속은 배선 후보가 될 수 없다’는 주장을 평가해 보십시오.

### 해답

1. 접촉부는 소자와 배선의 연결, 비아는 층간 연결, 금속선은 같은 층의 연결입니다. 접촉 계면 저항과 비아 저항을 놓칠 수 있습니다.
2. 구리 폭은 26 nm, 높이는 48 nm이므로 단면은 1,248 nm²입니다.
3. 새 저항은 1/0.8=1.25배로 25% 증가합니다. 저항률·온도·길이가 같다는 가정이 필요합니다.
4. 안 됩니다. 피치는 반복 간격이고 선폭과 공간 폭의 조합입니다.
5. 평균값만으로는 부족합니다. 국소 잔류 금속·브리지·절연 파괴·결함을 확인하고 연마 전후의 형상과 전기 결과를 연결해야 합니다.
6. 나노 크기의 유효 저항률, 배리어가 차지하는 단면, 접촉·계면 저항, 신뢰성과 공정 가능성이 달라질 수 있습니다. 벌크 순위만으로 최종 배선 저항 순위를 정할 수 없습니다.

## 14. 출처와 확인 범위

아래 절과 자료를 직접 확인했습니다. 연구 논문의 초록만 확인한 경우를 따로 표시합니다. 공개 문헌 조사이며 직접 제조·측정·수명 시험을 수행한 기록은 아닙니다. 확인일은 모두 2026-10-26입니다.

| 출처 | 읽은 부분과 사용 범위 | URL |
|---|---|---|
| imec, A view on the logic technology roadmap, 2020 | Key parts, MOL·BEOL 설명: 연결 구조와 공정 경계 | [공식 기술 설명](https://www.imec-int.com/en/articles/view-logic-technology-roadmap) |
| IBM, Copper interconnects | 구리 확산·다마신 통합, 1997 발표와 1998 제품 출하 | [공식 역사 자료](https://www.ibm.com/history/copper-interconnects) |
| Dean P. Neikirk, University of Texas at Austin, Etching 강의 | 슬라이드 25, Etch summary: 통상적 건식 식각에서 구리의 부산물 휘발성 문제입니다. 다른 반응 경로까지 불가능하다고 확대하지 않습니다. | [대학 공개 PDF](https://weewave.mer.utexas.edu/DPN_files/courses/FabLab/lecture_ovrhds/440_etch.pdf) |
| Applied Materials, CuBS 100th shipment, 2005-08-15 | TaN 배리어·Cu 시드 역할의 역사적 사례 | [공식 발표](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-strengthens-leadership-300mm-copper) |
| Applied Materials, Integrated Materials Solution | Endura CuBS 사례: 계면과 공정 통합 | [공식 설명](https://www.appliedmaterials.com/us/en/semiconductor/solutions-and-software/ims.html) |
| Andricacos 외, IBM J. Res. Dev., 1998 | Abstract: 첨가제와 superconformal fill입니다. 전문 전체를 검토한 것은 아닙니다. | [저자 소속 기관의 논문 소개](https://research.ibm.com/publications/damascene-copper-electroplating-for-chip-interconnections) |
| Lam Research, SABRE | Industry Challenges: ECD의 채움과 결함 요구 | [공식 제품 설명](https://www.lamresearch.com/product/sabre/) |
| EBARA, Nano-level polishing technique | 패드·미세 입자·약액의 결합과 세정·건조 통합 | [공식 원리 설명](https://ebara.com/global-en/technology/information/polishing-technology-ex/) |
| 박범영 외, JKSPE 22(2), 38–45, 2005 | Abstract: W CMP의 디싱·에로전, 패턴 밀도·크기입니다. 전문 전체를 검토한 것은 아닙니다. | [원 논문 소개](https://jkspe.or.kr/journal/view.php?number=3234) |
| Applied Materials, SEMICON West 2024 | Black Diamond low-k의 정전용량과 강도 요구 | [공식 발표 PDF](https://ir.appliedmaterials.com/static-files/6950cee5-f84d-4b3e-a9f4-39901093ae67) |
| Hu 외, IITC 1999 | Abstract: 단면·전류 밀도와 EM의 시험 결과입니다. 당시 구조의 수치 외삽은 하지 않습니다. | [저자 소속 기관 소개](https://research.ibm.com/publications/scaling-effect-on-electromigration-in-on-chip-cu-wiring) |
| TSMC Research, Reliability of dual damascene Cu metallization, 2000 | 해당 논문 초록: 비아 바닥의 EM 실패와 공정 의존성 | [공식 연구 목록의 해당 항목](https://research.tsmc.com/page/on-chip-interconnect/20.html) |
| Auth 외, IEDM 2017 | 출판사 서지와 대학 공개 PDF 1~2쪽: Co 접촉부와 INTERCONNECTS의 M0·M1을 구분했습니다. 해당 절을 확인한 범위이며 논문의 모든 실험을 재검증한 것은 아닙니다. | [원 논문 DOI](https://doi.org/10.1109/IEDM.2017.8268472) · [대학 공개 PDF](https://people.eecs.berkeley.edu/~pister/147fa21/Resources/Intel%2010nm%20IEDM2017.pdf) |
| Applied Materials, Endura CuBS Volta Ruthenium CVD | RuCo 라이너와 구리 리플로의 구분 | [공식 제품 설명](https://www.appliedmaterials.com/us/en/product-library/endura-cubs-volta-ruthenium.html) |
| imec, Semi-damascene at 18 nm pitch, 2022 | 공정 흐름과 Figure 1: Ru 직접 식각·갭필·비아 | [공식 연구 설명](https://www.imec-int.com/en/articles/imec-demonstrates-semi-damascene-interconnects-fully-self-aligned-vias-18nm-metal-pitch) |
| imec, Ru lines at 16 nm pitch, 2025-06-03 | 656 Ω/μm와 목표 저항 달성 비율, 피치별 조건 | [공식 연구 발표](https://www.imec-int.com/en/press/imec-demonstrates-16nm-pitch-ru-lines-record-low-resistance-obtained-using-semi-damascene) |
| Applied Materials, Mo contact development, 2026-01-05 | 개발·CMP·계측 사례: overfill, underfill, dishing, protrusion | [공식 개발 사례](https://www.appliedmaterials.com/us/en/newsroom/blogs/cooptimized-process-metrology-accelerates-molybdenum-contact-development.html) |
| Intel, 2025 Form 10-K | Our Business, Process Technology: 18A의 2025년 말 양산 보고와 PowerVia | [공식 공시 HTML](https://www.intc.com/filings-reports/all-sec-filings/content/0000050863-26-000011/intc-20251227.htm) |
| Intel 18A | PowerVia 설명: 후면 전력 경로, 앞면 배선 혼잡 완화 | [공식 기술 페이지](https://www.intel.com/content/www/us/en/foundry/process/18a.html) |

이전 글: [증착과 이온 주입](05-증착과이온주입_deposition-implantation.md)
