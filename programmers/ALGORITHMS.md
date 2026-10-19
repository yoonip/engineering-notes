# 알고리즘 길잡이 / Algorithm guide

입력 범위는 풀이 선택의 출발점입니다. 먼저 필요한 연산과 상태를 고른 뒤, 반복 횟수와 저장할 데이터가 제한 안에 들어오는지 확인합니다. 자료구조 이름만 바꾸는 것으로 효율이 좋아지는 것은 아니므로 실제 연산을 기준으로 비교합니다.

Input bounds guide algorithm choice. Identify the needed operations and states, then check total work and storage. Compare actual operations rather than assuming a named data structure is automatically faster.

| 주제 / Topic | 선택 이유 / Why use it | 예제 / Example |
|---|---|---|
| 최소 힙 / Min-heap | 가장 작은 값을 여러 번 꺼내고 새 값을 넣을 때, 매번 전체를 정렬하지 않는다.<br>Repeatedly extract minima and insert new values without sorting the whole collection each time. | [더 맵게](level2/079_42626_%EB%8D%94_%EB%A7%B5%EA%B2%8C/README.md) |
| 스택 / Stack | 아직 답을 못 찾은 위치를 쌓아 두고, 답이 확정되는 순간 한꺼번에 꺼낸다.<br>Retain unresolved positions and remove them when a later value resolves them. | [주식가격](level2/082_42584_%EC%A3%BC%EC%8B%9D%EA%B0%80%EA%B2%A9/README.md) |
| 큐와 시뮬레이션 / Queue and simulation | 시간과 처리 순서를 상태로 나타내고, 실제 규칙대로 한 단계씩 진행한다.<br>Represent time and processing order explicitly, advancing according to the rules. | [다리를 지나는 트럭](level2/083_42583_%EB%8B%A4%EB%A6%AC%EB%A5%BC_%EC%A7%80%EB%82%98%EB%8A%94_%ED%8A%B8%EB%9F%AD/README.md) |
| 그리디 / Greedy | 현재 선택을 바꿔도 최적해가 나빠지지 않는 근거가 있을 때 쓴다.<br>Use a local choice only when an exchange or dominance argument justifies it. | [구명보트](level2/072_42885_%EA%B5%AC%EB%AA%85%EB%B3%B4%ED%8A%B8/README.md) |
| 이진 탐색 / Binary search | 정답 후보가 커질수록 가능 여부가 한 방향으로만 바뀌면 경계를 찾는다.<br>Find a feasibility boundary when the predicate changes monotonically. | [징검다리](level4/extra_43236_%EC%A7%95%EA%B2%80%EB%8B%A4%EB%A6%AC/README.md) |
| 동적 계획법 / Dynamic programming | 앞으로 필요한 정보를 상태에 남기고, 같은 하위 문제의 답을 재사용한다.<br>Store the information needed by future decisions and reuse subproblem results. | [매출 하락 최소화](level4/extra_72416_%EB%A7%A4%EC%B6%9C_%ED%95%98%EB%9D%BD_%EC%B5%9C%EC%86%8C%ED%99%94/README.md) |
| 확장 상태 최단 경로 / Shortest paths with expanded states | 현재 위치만으로 미래가 정해지지 않으면 함정·방문 조건 등을 상태에 포함한다.<br>Include additional conditions when location alone does not determine future transitions. | [미로 탈출](level4/extra_81304_%EB%AF%B8%EB%A1%9C_%ED%83%88%EC%B6%9C/README.md) |
| 최소 신장 트리 / Minimum spanning tree | 모든 지점을 연결하는 비용의 합을 최소화한다. 출발점에서의 최단 거리와는 목적이 다르다.<br>Minimize total connection cost, a different objective from shortest distance from a source. | [지형 이동](level4/extra_62050_%EC%A7%80%ED%98%95_%EC%9D%B4%EB%8F%99/README.md) |
| 경로 압축 / Path compression | 이미 사용한 연속 구간을 건너뛰도록 다음 후보 연결을 짧게 만든다.<br>Shorten successor links to skip already occupied runs. | [호텔 방 배정](level4/extra_64063_%ED%98%B8%ED%85%94_%EB%B0%A9_%EB%B0%B0%EC%A0%95/README.md) |
| 위상 정렬 / Topological sorting | 선행 조건을 먼저 처리할 수 있는지, 의존 관계에 순환이 있는지 확인한다.<br>Check whether prerequisite dependencies can be processed without a cycle. | [동굴 탐험](level4/extra_67260_%EB%8F%99%EA%B5%B4_%ED%83%90%ED%97%98/README.md) |
| 트라이 / Trie | 공통 접두사를 따라가며 문자열 후보를 좁힌다. 노드 수와 메모리 비용도 함께 비교한다.<br>Narrow strings by shared prefixes while accounting for node and memory costs. | [[3차] 자동완성](level4/extra_17685_%5B3%EC%B0%A8%5D_%EC%9E%90%EB%8F%99%EC%99%84%EC%84%B1/README.md) |
| 행렬 거듭제곱 / Matrix exponentiation | 같은 선형 전이가 아주 많이 반복될 때 구간을 두 배씩 묶어 계산한다.<br>Combine repeated linear transitions by powers of two. | [경사로의 개수](level4/extra_214290_%EA%B2%BD%EC%82%AC%EB%A1%9C%EC%9D%98_%EA%B0%9C%EC%88%98/README.md) |
| 조합과 상태 압축 / Combinatorics and state compression | 서로 대칭인 경우를 묶되 선택 방법 수를 빠뜨리지 않는다.<br>Aggregate symmetric states without losing the multiplicity of choices. | [짝수 행 세기](level4/extra_68647_%EC%A7%9D%EC%88%98_%ED%96%89_%EC%84%B8%EA%B8%B0/README.md) |
| SQL 집계와 공동 순위 / SQL aggregation and ties | 집계 대상과 조인 후 행 수를 구별하고, 공동 최댓값을 빠뜨리지 않는다.<br>Distinguish aggregation units from joined row counts and retain tied maxima. | [그룹별 조건에 맞는 식당 목록 출력하기](level4/extra_131124_%EA%B7%B8%EB%A3%B9%EB%B3%84_%EC%A1%B0%EA%B1%B4%EC%97%90_%EB%A7%9E%EB%8A%94_%EC%8B%9D%EB%8B%B9_%EB%AA%A9%EB%A1%9D_%EC%B6%9C%EB%A0%A5%ED%95%98%EA%B8%B0/README.md) |

전수 탐색 대안은 작은 입력에서 정답을 직접 확인하는 데 유용합니다. 기본 풀이와 결과가 같다는 검사만으로 모든 입력에 대한 증명이 되는 것은 아니므로, 각 설명의 불변식·점화식·교환 논리와 함께 읽습니다.

Exhaustive alternatives establish reference answers on small inputs. Agreement alone is not a proof for every input; read the invariants, recurrences and exchange arguments alongside the executable checks.

[문제 목록 / Problem index](README.md)
