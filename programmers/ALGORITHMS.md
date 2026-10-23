# 알고리즘 길잡이 / Algorithm guide

[풀이 전체 목차 / Solution index](README.md) · [보관 범위 / Archive scope](COVERAGE.md)

입력 범위는 풀이 선택의 출발점입니다. 먼저 필요한 연산과 상태를 고른 뒤, 반복 횟수와 저장할 데이터가 제한 안에 들어오는지 확인합니다. 자료구조 이름만 바꾸는 것으로 효율이 좋아지는 것은 아니므로 실제 연산을 기준으로 비교합니다.

Input bounds guide algorithm choice. Identify the needed operations and states, then check total work and storage. Compare actual operations rather than assuming a named data structure is automatically faster.

| 주제 / Topic | 선택 이유 / Why use it | 예제 / Example |
|---|---|---|
| 최소 힙 / Min-heap | 가장 작은 값을 여러 번 꺼내고 새 값을 넣을 때, 매번 전체를 정렬하지 않습니다.<br>Repeatedly extract minima and insert new values without sorting the whole collection each time. | [더 맵게](Python/level2/079_42626_더_맵게/README.md) |
| 스택 / Stack | 아직 답을 못 찾은 위치를 쌓아 두고, 답이 확정되는 순간 한꺼번에 꺼냅니다.<br>Retain unresolved positions and remove them when a later value resolves them. | [주식가격](Python/level2/082_42584_주식가격/README.md) |
| 큐와 시뮬레이션 / Queue and simulation | 시간과 처리 순서를 상태로 나타내고, 실제 규칙대로 한 단계씩 진행합니다.<br>Represent time and processing order explicitly, advancing according to the rules. | [다리를 지나는 트럭](Python/level2/083_42583_다리를_지나는_트럭/README.md) |
| 그리디 / Greedy | 현재 선택을 바꿔도 최적해가 나빠지지 않는 근거가 있을 때 씁니다.<br>Use a local choice only when an exchange or dominance argument justifies it. | [구명보트](Python/level2/072_42885_구명보트/README.md) |
| 이진 탐색 / Binary search | 정답 후보가 커질수록 가능 여부가 한 방향으로만 바뀌면 경계를 찾습니다.<br>Find a feasibility boundary when the predicate changes monotonically. | [징검다리](Python/level4/extra_43236_징검다리/README.md) |
| 동적 계획법 / Dynamic programming | 앞으로 필요한 정보를 상태에 남기고, 같은 하위 문제의 답을 재사용합니다.<br>Store the information needed by future decisions and reuse subproblem results. | [매출 하락 최소화](Python/level4/extra_72416_매출_하락_최소화/README.md) |
| 확장 상태 최단 경로 / Shortest paths with expanded states | 현재 위치만으로 미래가 정해지지 않으면 함정·방문 조건 등을 상태에 포함합니다.<br>Include additional conditions when location alone does not determine future transitions. | [미로 탈출](Python/level4/extra_81304_미로_탈출/README.md) |
| 최소 신장 트리 / Minimum spanning tree | 모든 지점을 연결하는 비용의 합을 최소화합니다. 출발점에서의 최단 거리와는 목적이 다릅니다.<br>Minimize total connection cost, a different objective from shortest distance from a source. | [지형 이동](Python/level4/extra_62050_지형_이동/README.md) |
| 경로 압축 / Path compression | 이미 사용한 연속 구간을 건너뛰도록 다음 후보 연결을 짧게 만듭니다.<br>Shorten successor links to skip already occupied runs. | [호텔 방 배정](Python/level4/extra_64063_호텔_방_배정/README.md) |
| 위상 정렬 / Topological sorting | 선행 조건을 먼저 처리할 수 있는지, 의존 관계에 순환이 있는지 확인합니다.<br>Check whether prerequisite dependencies can be processed without a cycle. | [동굴 탐험](Python/level4/extra_67260_동굴_탐험/README.md) |
| 트라이 / Trie | 공통 접두사를 따라가며 문자열 후보를 좁힙니다. 노드 수와 메모리 비용도 함께 비교합니다.<br>Narrow strings by shared prefixes while accounting for node and memory costs. | [[3차] 자동완성](Python/level4/extra_17685_[3차]_자동완성/README.md) |
| 행렬 거듭제곱 / Matrix exponentiation | 같은 선형 전이가 아주 많이 반복될 때 구간을 두 배씩 묶어 계산합니다.<br>Combine repeated linear transitions by powers of two. | [경사로의 개수](Python/level4/extra_214290_경사로의_개수/README.md) |
| 조합과 상태 압축 / Combinatorics and state compression | 서로 대칭인 경우를 묶되 선택 방법 수를 빠뜨리지 않습니다.<br>Aggregate symmetric states without losing the multiplicity of choices. | [짝수 행 세기](Python/level4/extra_68647_짝수_행_세기/README.md) |
| SQL 집계와 공동 순위 / SQL aggregation and ties | 집계 대상과 조인 후 행 수를 구별하고, 공동 최댓값을 빠뜨리지 않습니다.<br>Distinguish aggregation units from joined row counts and retain tied maxima. | [그룹별 조건에 맞는 식당 목록 출력하기](level4/extra_131124_그룹별_조건에_맞는_식당_목록_출력하기/README.md) |

전수 탐색 대안은 작은 입력에서 정답을 직접 확인하는 데 유용합니다. 기본 풀이와 결과가 같다는 검사만으로 모든 입력에 대한 증명이 되는 것은 아니므로, 각 설명의 불변식·점화식·교환 논리와 함께 읽습니다.

Exhaustive alternatives establish reference answers on small inputs. Agreement alone is not a proof for every input; read the invariants, recurrences and exchange arguments alongside the executable checks.

[문제 목록 / Problem index](README.md)
