# Parallel prefix scan: 누적합으로 위치를 배정하기

[실행 코드](../../../예제_examples/심화_advanced/ai_data/advanced_ai_models.py) · [CLI](../../../예제_examples/심화_advanced/ai_data/demo.py) · [독립 검증](../../../예제_examples/심화_advanced/ai_data/test_advanced_ai.py)

## 합 하나가 아니라 각 항목의 앞부분 합

Reduction이 전체 합 하나를 만든다면 scan은 각 위치까지의 누적 결과를 만듭니다. 배열 [3,1,7,0]의 inclusive sum은 [3,4,11,11]입니다. 자기 자신을 제외한 exclusive sum은 [0,3,4,11]입니다. Exclusive의 첫 값 0은 정수 덧셈의 항등원입니다.

앞 항목의 합이 있어야 다음 합을 만들 수 있어 순차 계산만 가능해 보입니다. 하지만 작은 구간들의 합을 트리로 계산한 뒤 각 구간 앞의 합을 내려보내면 여러 위치를 함께 처리할 수 있습니다. [Blelloch의 prefix sums](https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf)와 [NVIDIA GPU Gems의 scan](https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda)을 대조했습니다.

일반 scan은 결합법칙을 만족하는 이항 연산을 사용하며 순서 자체를 바꿀 필요는 없습니다. 교환법칙은 필수 조건이 아닙니다. 다만 여기 구현은 설명과 정확한 정수 검증을 위해 정수 덧셈만 받습니다. 부동소수점 합을 같은 순서 독립성으로 일반화하지 않습니다.

## 두 번의 트리 순회

길이 n을 다음 2의 거듭제곱 m으로 확장하고 끝을 0으로 채웁니다. n>0이면 $`n\le m\lt2n`$입니다. Up-sweep에서는 크기 2,4,8,...의 구간 합을 만들며 오른쪽 끝에 저장합니다. 최종 root에는 전체 합이 생깁니다.

Down-sweep을 시작하기 전에 root를 0으로 바꿉니다. 각 노드에서 부모가 가진 값 P는 “이 구간보다 앞에 있는 모든 원소의 합”입니다. 왼쪽 자식의 옛 구간 합을 L이라 하면

```math
P_{\mathrm{left}}=P,\qquad
P_{\mathrm{right}}=P+L.
```

왼쪽 구간의 앞 합은 부모와 같고 오른쪽 구간 앞에는 왼쪽 구간 전체가 추가되기 때문입니다. 마지막 leaf에서 이 값은 각 원소 바로 앞까지의 합이 됩니다. 왼쪽 합을 먼저 보관하지 않고 덮어쓰면 오른쪽 값이 틀리므로 swap의 순서도 알고리즘의 일부입니다.

## Work와 depth를 구분합니다

완전 이진 트리의 내부 노드는 m-1개입니다. Up-sweep에서 m-1번, down-sweep에서 m-1번 더하므로 총 덧셈 수는 $`2(m-1)=O(n)`$입니다. 병렬 자원이 충분하고 같은 층을 함께 실행할 수 있다면 두 순회의 의존 깊이는 $`2\log_2m`$입니다.

```math
W(n)=2(m-1),\qquad D(n)=2\log_2m.
```

이 Python 함수는 각 층을 for loop로 순차 실행합니다. 따라서 depth가 로그라는 수학적 성질이 Python 실행 시간이 로그라는 뜻은 아닙니다. 입력 하나마다 앞의 합을 처음부터 계산하는 검증용 oracle은 작은 입력에서는 편하지만 $`O(n^2)`$가 됩니다. 실행 구현과 독립 검증의 비용 목적이 다릅니다.

Hillis–Steele식으로 매 round 모든 원소가 이전 거리의 값을 더하는 방법은 depth가 로그여도 work가 $`O(n\log n)`$입니다. Work-efficient와 병렬 depth를 동시에 구분해야 “병렬이니까 빠르다”는 혼동을 피할 수 있습니다. 오래된 GPU Gems의 특정 GPU thread·bank 수는 그 시기의 장치 조건이며 현대 모든 GPU 사양으로 옮기지 않습니다.

## Scan으로 원소를 압축합니다

[8,3,4,7,2]에서 짝수만 남기고 원래 순서를 유지한다고 하겠습니다. Flag는 [1,0,1,0,1], exclusive scan은 [0,1,1,2,2]입니다. 남길 원소는 scan이 가리키는 위치에 씁니다.

| 입력 | flag | 앞의 선택 수 | 출력 위치 |
|---:|---:|---:|---|
| 8 | 1 | 0 | 0 |
| 3 | 0 | 1 | 없음 |
| 4 | 1 | 1 | 1 |
| 7 | 0 | 2 | 없음 |
| 2 | 1 | 2 | 2 |

각 선택 원소의 위치는 자신보다 앞선 선택 원소 수와 같으므로 중복되지 않습니다. 선택 수만큼 출력 공간을 확보하면 범위도 맞습니다. 이 관계는 sparse 연산의 offset, 가변 길이 데이터 배치, histogram에서 구간 시작 위치를 만드는 데도 쓰입니다.

## 실행과 검증

```bash
python "예제_examples/심화_advanced/ai_data/demo.py" scan
python -m unittest discover -s "예제_examples/심화_advanced/ai_data" -p "test_*.py" -v
```

CLI의 9개 입력은 16개 leaf로 확장되어 덧셈 30번, 트리 단계 8개를 보고합니다. 출력 exclusive는 [0,3,4,11,11,15,16,22,25], inclusive는 각 입력을 더한 [3,4,11,11,15,16,22,25,27]입니다. 빈 입력은 빈 배열과 0 work/depth, 길이 1은 [0]입니다.

테스트는 길이 0~79의 양·음 정수에서 각 prefix를 독립적인 순차 합으로 계산해 비교하고 stable compaction 결과 [8,4,2]를 확인합니다. 같은 알고리즘을 다른 함수 이름으로 복사한 기준이 아닙니다. 실제 GPU scan은 block별 부분합, block 간 offset 전달과 동기화, scratch 저장소가 더 필요합니다. 이 실행은 tree 계산을 재현하는 CPU 프로그램이며 GPU 속도나 multi-block protocol을 측정한 결과는 아닙니다.

## English

### Prefixes provide positions

Reduction produces one aggregate; scan produces one aggregate per prefix. Inclusive scan of [3,1,7,0] is [3,4,11,11], while exclusive scan is [0,3,4,11]. Zero is addition's identity.

A tree first forms segment totals, then distributes the amount preceding each segment. [Blelloch](https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf) and [GPU Gems](https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda) explain the construction. General scan requires associativity but not commutativity when operand order is preserved. This implementation intentionally accepts integer addition only; floating-point sums do not inherit exact reassociation.

### Derive the down-sweep

Pad n positive-length inputs with zero to a power-of-two m, where $`n\le m\lt2n`$. Up-sweep stores totals of segments sized 2,4,8,... at their right endpoints. Replace the root total by zero. A parent's value P now means the sum before its segment.

Its left child inherits P; its right child receives P plus the left segment's old total L. Preserve that old total before overwriting. At leaves, these preceding sums are the exclusive scan.

There are m-1 internal nodes. Each traversal performs m-1 additions, giving linear total work $`2(m-1)`$. With sufficient parallel resources, dependency depth is $`2\log_2m`$. The Python implementation executes every layer serially, so logarithmic dependency depth is not a logarithmic Python runtime claim.

An all-elements-per-round Hillis–Steele construction has logarithmic depth but $`O(n\log n)`$ work. Historical GPU Gems device limits are not current universal GPU specifications.

### Stable compaction

For [8,3,4,7,2], even-value flags [1,0,1,0,1] scan to [0,1,1,2,2]. Each selected value writes to the number of selected values preceding it. These positions are unique and preserve order, yielding [8,4,2]. Allocating the sum of flags gives the required output capacity. Similar offsets support sparse structures and variable-length layouts.

### Executed checks

The CLI's nine inputs pad to 16 leaves and report 30 additions and eight tree layers. Exclusive output is [0,3,4,11,11,15,16,22,25]; adding original values gives inclusive output [3,4,11,11,15,16,22,25,27]. Empty input returns no work or layers; a singleton returns [0].

Tests compare lengths 0–79, including negative values, against independent sequential prefix sums and verify stable compaction. The intentionally simple oracle is quadratic on small inputs; it is not the execution algorithm. Actual GPU scans additionally need block totals, inter-block offsets, synchronization and scratch storage. This CPU run reproduces tree arithmetic without establishing GPU speed or a multi-block protocol.

## 출처 / Sources

- [Guy E. Blelloch, Prefix Sums and Their Applications](https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf): associative scan, identity, up/down sweeps and applications.
- [NVIDIA GPU Gems 3, Chapter 39](https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda): work efficiency, compaction and hardware implementation boundaries. 확인 / checked: 2026-10-19.
