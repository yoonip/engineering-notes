# GDP와 물가 읽기: 명목 금액, 실질 변화, 지수의 차이

[경제학](../README.md) · [희소성과 선택](scarcity-opportunity-cost-incentives.md)

## 한국어

### 금액이 커졌다고 생산이 그만큼 늘었을까

작년에 1만 원이던 제품이 올해 1만 2천 원이고 판매량은 같다면 매출은 20% 늘어난다. 그러나 같은 개수의 제품을 만든 것이다. 경제 전체에서도 금액 변화와 생산량 변화를 나누어야 한다. GDP는 일정 기간 한 경제의 국내 생산에 따른 부가가치를 나타내는 지표다. 재산의 총액이나 국민 개개인의 소득을 뜻하지 않는다.

부가가치는 산출에서 생산에 사용한 중간투입을 뺀 값이다. 중간재와 최종재의 판매액을 모두 단순 합산하면 같은 가치를 중복 계산할 수 있다. 시장가격 GDP는 기초가격으로 평가한 부가가치 합계에 생산물세를 더하고 생산물보조금을 뺀 값이다. 정부의 비시장 서비스 등은 별도의 국민계정 평가 규칙도 사용하므로 GDP를 현금 거래만의 합계로 설명하면 부족하다. [BEA의 GDP 설명](https://www.bea.gov/resources/learning-center/what-to-know-gdp), [BEA 부가가치 정의](https://bea.gov/help/faq/184), [OECD 국민계정 FAQ](https://www.oecd.org/en/data/insights/data-explainers/2024/03/annual-national-accounts-frequently-asked-questions.html)

지출 측면의 기본 관계는 $Y=C+G+I+X-M$이다. 여기서는 $C$를 가계와 가계에 봉사하는 비영리단체의 최종소비, $G$를 정부 최종소비, $I$를 재고 증감과 귀중품 순취득을 포함한 총자본형성, $X,M$을 수출·수입으로 정한다. 정부 투자도 이 정의의 $I$에 포함한다. 수입을 빼는 것은 앞 항목에 포함될 수 있는 국외 생산분을 제외하기 위해서이지, 수입이 언제나 국민에게 손해라는 가치 판단이 아니다. 미국 BEA 설명처럼 정부 소비와 투자를 $G$로 묶는 표기도 있으므로 글자를 외우기보다 구성 항목을 확인한다. [OECD 국민계정 FAQ](https://www.oecd.org/en/data/insights/data-explainers/2024/03/annual-national-accounts-frequently-asked-questions.html), [BEA 지출 측정 설명](https://www.bea.gov/news/blog/2025-06-03/expenditures-approach-measuring-gdp)

### 가격과 수량을 분리하는 작은 계산

다음은 한 종류의 최종재만 있는 가상 예다. 실제 국가 통계가 아니다.

| 기간 | 수량 $q$ | 단가 $p$ | 당기 가격의 금액 $pq$ |
| --- | ---: | ---: | ---: |
| 0 | 100 | 10,000원 | 1,000,000원 |
| 1 | 110 | 12,000원 | 1,320,000원 |

명목 금액은 32% 늘었다. 기간 0의 가격을 고정하면 기간 1의 생산은 1,100,000원이므로 수량 변화는 10%다. 일반적인 고정기준년 설명식은

$$Y_t^{nom}=\sum_i p_{it}q_{it},\qquad
Y_t^{real,0}=\sum_i p_{i0}q_{it}.$$

이는 명목과 실질의 차이를 이해하기 위한 단순식이다. 한국은행이 설명하는 실제 실질 GDP는 상대가격과 가중치 변화를 반영하는 연쇄 물량측정치다. 구성 항목의 실질 금액을 단순히 더해 전체와 같아야 한다고 판단하면 안 된다. [한국은행 경제통계 FAQ의 명목·실질 GDP 및 기여도 설명](https://www.bok.or.kr/portal/bbs/P0001949/list.do?menuNo=200658&searchOptn2=7)

대응하는 명목·실질 계열로 계산한 암묵적 GDP 디플레이터는

$$D_t=100\frac{Y_t^{nom}}{Y_t^{real}}.$$

가상 예에서는 120이다. 동일한 계열 정의로 보면 성장 배율은 $(1+g_{nom})=(1+g_{real})(1+g_D)$로 분해된다. 32%에서 20%를 빼 12%를 실질 증가율이라고 하면 틀린다. 정확한 계산은 $1.32/1.20-1=10\%$다.

### 소비자물가지수와 GDP 디플레이터는 무엇이 다를까

CPI는 가계가 소비하는 상품과 서비스의 가격 변화를 지출 비중으로 종합한다. 단순한 고정 basket 설명에서

$$P_t=100\frac{\sum_i p_{it}q_{i0}}{\sum_i p_{i0}q_{i0}}$$

로 나타낼 수 있다. 실제 지수에는 대표 품목 선정, 가격 조사, 품질 조정과 가중치 개편이 있다. 특정 가구의 지출 구성은 전체 가중치와 다를 수 있다. [소비자물가지수 공식 계산 설명](https://mods.go.kr/menu.es?mid=b70101050000)

| 구분 | CPI | GDP 디플레이터 |
| --- | --- | --- |
| 중심 질문 | 소비 지출 가격이 얼마나 변했나 | 국내 생산의 명목·실질 평가가 어떻게 달라졌나 |
| 포괄 범위 | 소비 basket에 포함된 수입 소비재도 포함 가능 | 국내 생산 기준이며 수출도 관련 |
| 가중치 관점 | 소비지출 비중과 공식 개편 방법 | 생산 구성·물량측정과 연결 |

따라서 명목 GDP를 CPI로 나누기만 하면 공식 실질 GDP가 된다고 할 수 없다. 수입 가격이 GDP 디플레이터와 전혀 무관하다는 결론도 성립하지 않는다. 수입 중간재 비용과 국내 부가가치·가격의 관계를 통해 간접적으로 영향을 줄 수 있다. 지표별 포괄 범위를 비교해야 한다. [BLS의 CPI·GDP 가격지표 비교](https://www.bls.gov/opub/mlr/2016/article/comparing-the-cpi-with-the-gdp-price-index-and-gdp-implicit-price-deflator.htm)

### 상승률이 낮아져도 가격은 오를 수 있다

같은 기준의 가상 CPI가 100, 110, 112.2라면 상승률은 10%에서 2%로 낮아지지만 가격 수준은 계속 높아졌다. 물가상승률 둔화와 물가 하락은 다르다. 상승률은 $(P_t/P_{t-k}-1)\times100$이며, 월별 자료에서 $k=1$이면 전월비, $k=12$이면 전년동월비다. 서로 다른 비교 기간을 섞지 않는다. [공식 등락률 설명](https://mods.go.kr/menu.es?mid=b70202020000)

개인의 구매력을 볼 때는 목적에 맞는 물가지수를 선택한다. 명목 임금이 3%, 해당 소비 가격지수가 5% 올랐다면 그 기준의 실질 임금 변화는 $1.03/1.05-1\approx-1.90\%$다. 이는 모든 가구의 체감 변화를 동일하게 뜻하지 않는다.

### 통계를 읽을 때 남겨야 할 조건

자료의 단위, 기간, 명목·실질 구분, 계절조정 여부, 비교 기준과 공표 시점을 확인한다. 속보·잠정·확정과 기준 개편으로 수치가 수정될 수도 있다. 국가 간 비교에서는 통화 환산과 인구도 구분한다. 또한 GDP가 늘어도 건강, 분배, 여가, 환경과 다음 세대의 자원 상태가 모두 좋아졌다고 결론 내릴 수 없다. OECD는 생산 지표와 함께 삶의 질과 지속가능성의 여러 지표를 살핀다. [OECD well-being framework](https://www.oecd.org/en/topics/sub-issues/measuring-well-being-and-progress.html)

## English

### More money does not necessarily mean proportionally more output

If a product's price rises from 10,000 to 12,000 won with unchanged quantity, revenue rises 20% without additional units. Aggregate analysis also separates value and volume changes. GDP measures domestic production's value added over a period, not total wealth or each resident's income.

Value added subtracts intermediate inputs from output. Simply adding intermediate and final sales can double-count value. GDP at market prices adds taxes on products and subtracts subsidies on products from value added at basic prices. National accounts also use valuation rules for nonmarket government services, so GDP is more than a sum of cash transactions. [BEA GDP guide](https://www.bea.gov/resources/learning-center/what-to-know-gdp), [value-added definition](https://bea.gov/help/faq/184), [OECD national accounts FAQ](https://www.oecd.org/en/data/insights/data-explainers/2024/03/annual-national-accounts-frequently-asked-questions.html)

The expenditure identity is $Y=C+G+I+X-M$. Here $C$ means household and nonprofit-institution-serving-households final consumption, $G$ government final consumption, $I$ total capital formation including inventory changes, net acquisitions of valuables, and government investment, and $X,M$ exports and imports. Imports remove foreign production potentially included in other components; subtraction does not establish that imports harm residents. Other conventions, including the BEA presentation, combine government consumption and investment in $G$. Check the component definitions rather than memorizing the letters alone. [OECD national accounts FAQ](https://www.oecd.org/en/data/insights/data-explainers/2024/03/annual-national-accounts-frequently-asked-questions.html), [BEA expenditure explanation](https://www.bea.gov/news/blog/2025-06-03/expenditures-approach-measuring-gdp)

### Separate prices and quantities

The table is a hypothetical one-final-good example, not national statistics. Quantity rises from 100 to 110 and price from 10,000 to 12,000 won. Nominal value rises from 1,000,000 to 1,320,000 won, or 32%. At period-zero prices, output becomes 1,100,000 won, a 10% volume increase.

The teaching expressions are $Y_t^{nom}=\sum_i p_{it}q_{it}$ and $Y_t^{real,0}=\sum_i p_{i0}q_{it}$. Actual Korean real GDP uses chain volume measures reflecting changing relative prices and weights. Its component levels need not add directly to the total. [Bank of Korea GDP and contribution FAQ](https://www.bok.or.kr/portal/bbs/P0001949/list.do?menuNo=200658&searchOptn2=7)

The corresponding implicit deflator is $D_t=100Y_t^{nom}/Y_t^{real}$, or 120 in the example. For consistently defined series, $(1+g_{nom})=(1+g_{real})(1+g_D)$. Subtracting 20% from 32% is not exact: $1.32/1.20-1$ gives 10%.

### CPI and the GDP deflator answer different questions

CPI aggregates consumer prices using expenditure weights. A simple fixed-basket representation is $P_t=100\sum_i p_{it}q_{i0}/\sum_i p_{i0}q_{i0}$. Official construction also involves representative products, price collection, quality adjustment, and weight updates. An individual household can have different expenditure shares. [Official Korean CPI calculation guide](https://mods.go.kr/menu.es?mid=b70101050000)

CPI can include imported consumer goods in its basket. The GDP deflator concerns domestic production and also relates to exports; its weights connect to production composition and volume measurement. Dividing nominal GDP by CPI does not generally produce official real GDP. Nor are import prices necessarily irrelevant to the deflator: imported-input costs can affect domestic value added and prices indirectly. [BLS comparison](https://www.bls.gov/opub/mlr/2016/article/comparing-the-cpi-with-the-gdp-price-index-and-gdp-implicit-price-deflator.htm)

### Slower inflation can still mean rising prices

A hypothetical CPI path of 100, 110, and 112.2 has inflation falling from 10% to 2% while the price level continues rising. Disinflation differs from falling prices. Percentage change is $(P_t/P_{t-k}-1)\times100$: for monthly data, $k=1$ compares with the preceding month and $k=12$ with the same month a year earlier. [Official rate-of-change guide](https://mods.go.kr/menu.es?mid=b70202020000)

Choose a price index appropriate to the purchasing-power question. If nominal wages rise 3% and the chosen consumption-price index rises 5%, real wage growth on that basis is $1.03/1.05-1\approx-1.90\%$. This does not imply identical experiences across households.

### Preserve the statistical context

Record units, period, nominal or real status, seasonal adjustment, comparison basis, and release date. Preliminary estimates and benchmark updates can revise values. Cross-country comparisons also distinguish currency conversion and population. GDP growth alone does not establish improvements in health, distribution, leisure, the environment, or resources for future generations. OECD examines multiple well-being and sustainability measures alongside production. [OECD framework](https://www.oecd.org/en/topics/sub-issues/measuring-well-being-and-progress.html)

## 출처와 대조 / Sources and cross-check

- 한국은행 경제통계 FAQ: 명목·실질, 연쇄 물량, 통계 수정 / nominal versus real, chain volumes, and revisions.
- BEA: 국내 생산·부가가치·지출 항등식 / domestic production, value added, and expenditure identity.
- 한국 CPI 공식 설명·BLS: 소비 basket, 계산 기준과 GDP 가격지표의 범위 차이 / basket, calculation basis, and coverage differences.
- OECD: 시장가격 평가·지출 항목, GDP와 후생·지속가능성의 구분 / market-price valuation, expenditure components, and output versus well-being and sustainability.

한국과 미국의 세부 작성 방식이 같다고 가정하지 않고 정의와 포괄 범위를 대조했다. 모든 수치 예는 계산을 설명하기 위해 구성했다. / Definitions and coverage are compared without assuming identical Korean and US compilation details. All numerical examples are constructed for explanation. 확인 / checked: 2026-10-19.
