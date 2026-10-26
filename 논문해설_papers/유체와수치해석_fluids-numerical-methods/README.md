# 유체의 방정식과 수치 계산 / Fluid dynamics and numerical methods

연속적인 물리 방정식을 컴퓨터의 유한한 계산으로 옮기는 방법을 읽습니다. 계산이 발산하지 않는 성질, 실제 해에 가까운 정도, 물리 제약을 만족하는 정도를 구별합니다.

| 논문 | 해설 | 직접 따라갈 예제 |
|---|---|---|
| Chorin, 1968, Numerical Solution of the Navier-Stokes Equations | [비압축 유동의 압력 투영](비압축유동의압력투영_chorin1968-projection.md) | 임시 속도의 발산을 압력 기울기로 제거하고, 격자 간격을 줄일 때 점성 확산의 시간 간격 한계가 달라지는 이유를 계산합니다. |

본문은 원문의 격자 계산과 직접 만든 주기 영역의 연속함수 예제를 구분합니다. 압력 방정식을 풀었다는 사실만으로 모든 경계·시간 간격·난류에서 정확성이 보장되는 것은 아닙니다. 장치의 열 제거 문제는 [액체 냉각 리뷰](../../제품기술분석_product-technology/제조와인프라_manufacturing-infrastructure/데이터센터의액체냉각_liquid-cooling2026.md)에서도 살펴보실 수 있습니다.

[논문 전체 목록](../README.md)
