# 병렬 계산의 분할, reduction, 통신 비용

## 일을 나누는 것과 시간을 줄이는 것은 다릅니다

백만 개의 측정값 합을 구할 때 여러 작업자에게 나누어 맡길 수 있습니다. 하지만 데이터를 전달하고, 느린 작업자를 기다리고, 부분 결과를 합치는 시간도 필요합니다. 병렬화는 작업량을 없애는 것이 아니라 의존관계를 유지하면서 여러 작업을 겹치는 방법입니다. LLNL은 load balancing을 작업자 간 일의 균형으로 설명하며, barrier가 있으면 가장 느린 작업자가 전체 완료 시간을 결정한다고 지적합니다. [LLNL parallel computing](https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial)

문제 크기 $`N`$을 고정하고 작업자 수 $`P`$를 늘리는 것은 strong scaling입니다. 작업자당 문제 크기를 유지하며 전체 문제를 늘리는 것은 weak scaling입니다. 두 실험의 speedup을 같은 뜻으로 해석하면 안 됩니다. 직렬 비율 $`s`$가 변하지 않고 병렬 부분에 추가 비용이 없다는 Amdahl 모델은 $`S(P)=1/[s+(1-s)/P]`$를 줍니다. 통신·불균형이 있으면 이 값도 낙관적인 상한이 됩니다.

## 남는 원소까지 정확히 분할하기

각 원소의 비용이 비슷하다면 $`N=qP+r`$, $`0\le r<P`$로 나눕니다. 앞의 $`r`$개 작업자는 (q+1)개, 나머지는 $`q`$개를 맡습니다. 이때 최대·최소 원소 수 차이는 1 이하이고 총합은 $`r(q+1)+(P-r)q=N`$입니다. 반열린 구간 `[start, stop)`을 쓰면 인접 구간의 끝과 시작을 같게 두면서 중복을 피하기 쉽습니다.

예를 들어 $`N=10,P=3`$이면 `[0,4)`, `[4,7)`, `[7,10)`입니다. $`P>N`$이면 빈 구간도 생깁니다. 같은 개수의 원소라도 한 원소의 계산 비용이 다르면 시간 균형까지 보장하지 않습니다. 동적 작업 배분은 이를 줄일 수 있지만 작업 관리와 통신 비용이 늘어납니다.

## Reduction은 부분 결과를 결합합니다

합, 최댓값처럼 여러 입력을 하나의 결과로 결합하는 연산을 reduction이라고 합니다. MPI의 `Reduce`는 결과를 한 rank에, `Allreduce`는 결과를 모든 참여 rank에 제공합니다. 이름이 비슷한 `Gather`는 값을 모으지만 연산으로 결합하지 않습니다. [LLNL MPI collectives](https://hpc-tutorials.llnl.gov/mpi/collective_communication_routines/)

두 개씩 합치는 트리에서 $`N=2^k`$라면 첫 층에 $`N/2`$, 다음 층에 $`N/4`$개의 덧셈이 있습니다. 총 일은 $`N-1=O(N)`$, 충분한 실행 자원이 있을 때 의존관계의 길이는 $`k=O(\log N)`$입니다. Python 예제의 `pairwise_sum`은 그 순서를 직렬로 재현하므로 실제 병렬 속도 향상을 만들지는 않습니다.

수학적 실수의 합은 결합법칙을 만족하지만 부동소수점 덧셈은 중간 반올림 때문에 순서에 따라 달라질 수 있습니다. 정수 입력에 대한 정확한 합 검증과 실수의 오차 검증은 구분합니다. 실수 비교에서는 `math.fsum` 같은 정밀 누산 기준과 절대·상대 오차를 사용할 수 있으며, 상쇄가 큰 데이터에서는 상대 오차만으로 판단하기 어렵습니다.

## 통신량과 통신 횟수

메시지 크기 $`m`$ byte, 시작 지연 $`\alpha`$ s, byte당 비용 $`\beta`$ s/byte인 단순 모델은 $`T_{msg}=\alpha+\beta m`$입니다. $`P=2^k`$ 작업자가 같은 크기 결과를 이진 트리로 결합하고 각 round의 통신이 겹쳐 실행된다고 가정하면 통신의 임계 경로는

$$T_{tree}=\log_2P\,(\alpha+\beta m).$$

여기에는 reduction 연산 비용, 혼잡, 네트워크 topology, protocol 전환, 큰 메시지의 분할, `Allreduce`의 추가 전달을 넣지 않았습니다. 예를 들어 $`P=8,m=1000`$, $`\alpha=1\,\mu s`$, $`\beta=1\,ns/byte`$이면 모델값은 $`6\,\mu s`$입니다. 이는 측정값이 아닙니다. 작은 메시지를 너무 자주 보내면 $`\alpha`$가 누적되고, 큰 묶음으로 보내면 메모리와 지연 요구가 달라집니다.

## 구현과 독립 검증

[`balanced_partitions`, `pairwise_sum`, `tree_reduction_time`](../../../예제_examples/확장기초_extended/ai_data/models.py)은 각각 분할, 트리 순서, 통신 모델을 구현합니다. [테스트](../../../예제_examples/확장기초_extended/ai_data/test_models.py)는 다양한 $`N,P`$에서 모든 인덱스가 한 번씩 포함되는지, 구간 크기 차이가 1 이하인지 검사합니다. 트리 합은 별도의 Python 정수 합과 비교하고, 통신 식은 손으로 계산한 8-worker 사례와 $`P=1`$의 0회 통신을 확인합니다. 실제 병렬 실행의 정확성에는 race, collective 호출 순서, datatype·count 일치, 경계 데이터 교환 검증이 추가됩니다.

## English

### Parallel work still has overhead

A sum can be split across workers, but sending data, waiting and combining results also take time. Parallelization overlaps independent work while preserving dependencies. Equal work matters because the slowest participant can determine completion at a barrier. [LLNL introduction](https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial)

Strong scaling fixes the total problem while increasing workers; weak scaling holds per-worker size fixed while increasing the total problem. Their speedups describe different experiments. For a fixed serial fraction $`s`$ and no additional parallel overhead, Amdahl's model gives $`S(P)=1/[s+(1-s)/P]`$. Communication and imbalance make this an optimistic bound.

### Complete balanced partitions

Write $`N=qP+r`$, with $`0\le r<P`$. Give (q+1) items to the first $`r`$ workers and $`q`$ to the rest. The total is exactly $`N`$, and sizes differ by at most one. Adjacent half-open ranges avoid duplicate endpoints. Ten items across three workers become `[0,4)`, `[4,7)`, `[7,10)`. More workers than items produce empty ranges. Equal item counts imply balanced time only when per-item costs are comparable. Dynamic assignment can reduce imbalance at the expense of management and communication.

### Combining partial results

A reduction combines inputs into a sum, maximum or another aggregate. MPI `Reduce` places the result at one rank; `Allreduce` makes it available to all participants. `Gather` collects values without reducing them. [LLNL MPI collectives](https://hpc-tutorials.llnl.gov/mpi/collective_communication_routines/)

For $`N=2^k`$, a pairwise tree performs $`N/2+N/4+\cdots+1=N-1`$ additions. Total work is (O(N)), while dependency depth is $`O(\log N)`$ with sufficient execution resources. The Python implementation reproduces this ordering serially and claims no parallel speedup.

Real addition is associative, but floating-point addition can change with rounding order. Exact integer checks and numerical-error checks serve different purposes. `math.fsum` can provide a more accurate floating-point reference. Absolute error remains important when cancellation makes the true result close to zero.

### Communication model

The illustrative message model is $`T_{msg}=\alpha+\beta m`$, with latency in seconds, payload in bytes and per-byte cost in seconds/byte. A binary tree with $`P=2^k`$, equal-size partial results and overlapping communication within each round has critical-path communication $`\log_2P(\alpha+\beta m)`$.

This excludes computation, contention, topology, protocol transitions, message segmentation and the extra distribution needed by all-reduce. Eight workers, a 1000-byte payload, $`1\,\mu s`$ startup and $`1\,ns/byte`$ produce the model value $`6\,\mu s`$, not a measurement. Small frequent messages accumulate startup cost; batching changes latency and memory demands.

### Independent verification

The linked models implement balanced intervals, tree ordering and the stated cost formula. Tests enumerate many problem and worker sizes, checking complete nonoverlapping coverage and a maximum size difference of one. Tree sums are checked against an independent exact integer sum. Communication checks use the hand-calculated eight-worker case and the no-communication single-worker limit. Actual parallel implementations additionally need checks for races, collective ordering, matching datatypes/counts and correct boundary exchange.

## Sources

- [Lawrence Livermore National Laboratory, Introduction to Parallel Computing](https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial): decomposition, load balance, communication and scaling.
- [LLNL, MPI Collective Communication](https://hpc-tutorials.llnl.gov/mpi/collective_communication_routines/): scatter/gather/reduce/all-reduce semantics. Reference date: 2026-10-19.
