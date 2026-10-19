# 복제본의 교집합: quorum과 일관성의 조건

## 서버를 늘리면 무엇이 어려워지는가

같은 값을 여러 서버에 저장하면 한 서버의 장애를 견딜 가능성이 생긴다. 대신 복사본 사이의 차이를 처리해야 한다. 쓰기가 일부 서버에만 도착하거나, 응답이 늦거나, 네트워크가 두 부분으로 나뉠 수 있다. 요청 timeout은 “수행되지 않았다”의 증거가 아니다. 서버가 변경을 마친 뒤 응답만 사라졌을 수도 있다. 따라서 재시도와 중복 실행, 데이터 버전과 충돌 처리까지 연산 계약에 들어간다.

이 글의 작은 모델은 고정된 $`N`$개 복제본, crash 또는 통신 불가 장애, 하나의 key를 가정한다. 악의적으로 거짓 값을 보내는 Byzantine 장애는 다루지 않는다. 실제 시스템의 장애 모델과 membership 변경은 이 가정과 별도로 설계된다.

## 왜 $`R+W>N`$인가

쓰기 응답에 필요한 복제본 수를 $`W`$, 읽기 응답에 필요한 수를 $`R`$이라고 하자. 쓰기 집합 $`\mathcal W`$, 읽기 집합 $`\mathcal R`$가 같은 $`N`$개 안에서 선택되면

$$
\vert \mathcal R\cap\mathcal W\vert
=R+W-\vert \mathcal R\cup\mathcal W\vert
\ge R+W-N.
$$

그래서 $`R+W>N`$이면 적어도 하나가 겹친다. 이는 집합의 포함배제 원리이며 네트워크 구현과 무관한 사실이다. $`N=3,R=2,W=2`$에서는 최소 한 개, $`N=5,R=2,W=2`$에서는 0개가 가능하다. Dynamo 논문은 $`N,R,W`$와 quorum-like 설정을 설명하면서 가용성과 지연의 선택을 다룬다. [Amazon Dynamo, §4.5](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

| $`N,R,W`$ | 최소 교집합 | 읽기·쓰기 모두 가능한 최대 동시 미응답 수 |
|---|---:|---:|
| 3, 2, 2 | 1 | 1 |
| 5, 3, 3 | 1 | 2 |
| 5, 2, 2 | 0 | 3 |

마지막 열은 필요한 수만 응답하면 완료된다는 단순 가정에서 $`\min(N-R,N-W)`$다. 그 숫자가 일관성이나 데이터 내구성을 보장하는 것은 아니다.

## 교집합이 있다고 선형화 가능성이 저절로 생기지는 않는다

읽기가 완료된 쓰기의 값을 발견하려면 교집합 외에도 조건이 필요하다. 예를 들어 다음 제한된 상황에서는 설명이 단순하다. 쓰기는 순차적으로 하나씩 진행되고, 단조 증가 버전이 붙으며, 응답한 복제본은 해당 버전을 잃지 않는다. 읽기는 마지막 완료된 쓰기 뒤에 시작하고 $`R`$개의 응답 중 가장 큰 버전을 선택한다. 그러면 교집합의 복제본이 그 쓰기 또는 그 이후 버전을 가지고 있으므로 이전 버전만 반환하는 것을 막을 수 있다.

여기서 동시 쓰기, 쓰다 중단된 값, 재시작 시 상태 손실, 임의로 바뀐 복제본 집합을 허용하면 추가 프로토콜이 필요하다. 물리 시계의 timestamp가 언제나 실제 쓰기 순서를 정한다는 보장도 없다. Sloppy quorum처럼 원래 복제 집합 밖의 서버가 응답하면 위 집합 증명을 그대로 적용할 수 없다. Dynamo의 고가용성·충돌 조정 설계를 “쿼럼이면 항상 강한 일관성”으로 읽으면 안 된다. [Dynamo의 가용성·versioning 설계](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

선형화 가능성은 각 연산이 호출과 응답 사이의 한순간에 일어난 것처럼 보이며 실제 시간의 선후관계를 지키는 성질이다. 합의 프로토콜은 단순한 투표수보다 많은 상태와 규칙을 사용한다. Raft는 term, log의 최신성, leader 선출과 commit 규칙을 함께 둔다. 특히 이전 term의 항목을 단지 과반수 복제되었다는 이유만으로 직접 commit하지 않는다. [Raft §5.4](https://raft.github.io/raft.pdf)

## 지연, 장애, 검증을 분리한다

동일한 요청을 여러 서버에 보내고 $`R`$번째 응답을 기다린다면 읽기 지연은 응답 시간의 $`R`$번째 순서 통계량과 관련된다. $`R`$을 늘리면 필요한 응답이 많아지지만, 복제·큐잉·재시도 비용까지 고려하지 않은 모델만으로 실제 지연 수치를 예측할 수는 없다. 네트워크 분할 중에는 필요한 교집합을 유지하며 양쪽 모두에 독립적으로 성공 응답을 줄 수 없는 상황이 생긴다. 어떤 오류를 반환하고 재시도를 어떻게 처리할지도 동작의 일부다.

[`quorum_overlap`](../../../예제_examples/확장기초_extended/ai_data/models.py)은 수학적 최소 교집합만 계산한다. [테스트](../../../예제_examples/확장기초_extended/ai_data/test_models.py)는 $`N=1\ldots6`$의 모든 유효 $`R,W`$에 대해 가능한 읽기·쓰기 부분집합을 전수 열거하고 실제 최소 교집합과 공식을 비교한다. 이는 quorum 산술의 독립 검증이다. 분산 저장소의 선형화 가능성 시험, 장애 주입, 영속성 시험을 대신하지 않는다. 실제 이력 검증에는 호출·응답 시각, 반환 버전과 실패를 기록하고 허용 가능한 순차 이력이 있는지 확인하는 절차가 추가된다.

## English

### Replication introduces partial failure

Copies can allow service to survive a failed server, but writes may reach only some copies, replies may be delayed and networks can partition. A timeout does not prove an operation did not happen: the update may have completed before its response was lost. Retry and duplicate-execution semantics therefore belong to the contract.

The mathematical model here assumes a fixed set of $`N`$ replicas, one key, and crash or communication failures. It excludes Byzantine responses. Membership changes and different failure models require separate protocols.

### Deriving the intersection bound

If successful writes require $`W`$ replicas and reads require $`R`$, inclusion–exclusion gives the equation above: the intersection is at least (R+W-N), bounded below by zero. Thus $`R+W>N`$ forces overlap. With $`3,2,2`$, at least one replica overlaps; with $`5,2,2`$, disjoint sets exist. The table also gives $`\min(N-R,N-W)`$, the unavailable-replica count under which both operations can still collect enough responses. This count alone does not establish durability or consistency. [Dynamo quorum configuration](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

### Intersection is only one ingredient

Consider a restricted execution: writes are sequential, carry increasing versions, acknowledged copies retain their versions, and a read begins after the last completed write and returns the largest version among its $`R`$ replies. An overlapping replica then contains that write or a later version, preventing a read consisting solely of older versions.

Concurrent or incomplete writes, state loss after restart and changes to the replica set break this simple argument. Physical timestamps do not automatically order writes correctly. Sloppy quorums can use substitute servers outside the intended replica set, so the same set proof cannot be applied unchanged. Dynamo's availability and reconciliation mechanisms should not be equated with automatic strong consistency. [Dynamo design](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

Linearizability requires every operation to appear at one instant between its invocation and response while respecting real-time precedence. Consensus protocols need more than vote counts. Raft combines terms, log freshness, election and commit rules; an old-term log entry is not directly committed merely because it exists on a majority. [Raft §5.4](https://raft.github.io/raft.pdf)

### Cost and independent checks

Waiting for $`R`$ responses relates latency to the $`R`$-th ordered response time, but queues, retries and replication prevent this from being a complete latency predictor. During a partition, maintaining the required agreement may prevent both sides from independently returning success. Error and retry behavior are observable parts of the service.

The linked function computes only the minimum intersection. Tests enumerate every read and write subset for all valid $`R,W`$ with $`N=1\ldots6`$, then compare the actual minimum with the formula. This independently checks quorum arithmetic, not a storage system's linearizability, failure recovery or durability. Those require operation histories with invocation and response times, returned versions and failures, followed by checking whether an allowed sequential history explains the observations.

## Sources

- [Amazon, Dynamo: A Highly Available Key-value Store](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): $`N,R,W`$, sloppy quorums, versioning and reconciliation.
- [Ongaro and Ousterhout, Raft extended paper](https://raft.github.io/raft.pdf): majority intersection plus election and commit safety conditions. Reference date: 2026-10-19.
