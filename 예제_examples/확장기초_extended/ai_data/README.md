# 계산 모델과 독립 검증 / Computational models and independent checks

Python 표준 라이브러리만 사용하는 교육용 모델이다. 실행 위치는 저장소 루트다.

```bash
python -m unittest discover -s 예제_examples/확장기초_extended/ai_data -p 'test_*.py' -v
```

| 범위 | 함수 | 검증 기준 |
|---|---|---|
| GPU 메모리·자원 | `memory_sectors`, `occupancy_bound` | 정렬·비정렬·stride·자원 한계 |
| 모델 출력 | `token_probabilities`, `sample_token` | 해석적 확률·상수 이동 불변·구간 빈도 |
| DB | `sales_totals`, `transfer` | Python 집계와 비교·실패 롤백·총액 보존 |
| 분산·병렬 | `quorum_overlap`, `balanced_partitions`, `pairwise_sum` | 부분집합 전수 열거·중복 없는 분할·정수 합 |
| CV·학습 | `pinhole`, `correlate_valid`, `linear_loss_gradient`, `cosine_learning_rate` | 닮음·상수 영상·유한차분·해석적 최적점 |
| 검색·도구 | `tfidf_rank`, `retrieval_metrics`, `bounded_tool` | 알려진 순위·직접 계산한 지표·허용 범위 |
| 양자화·그래픽 | `quantize`, `dequantize`, `transform_point`, `barycentric` | 정수 격자·반올림·오차 한계·역변환 |
| 수치해석 | `poisson_sine`, `decay_euler` | 이산 고유모드·격자/시간 수렴·플럭스 보존 |
| HTTP 계약 | `IdempotencyStore`, `page_after` | 재시도·본문 충돌·페이지 누락/중복 |

GPU 함수는 주소와 자원 계산이며 CUDA를 실행하지 않는다. 분산·HTTP 예제는 단일 프로세스 계약 모델이고 네트워크 장애·동시성·영속 저장을 구현하지 않는다. 학습·검색·양자화 검증은 작은 수학적 사례에 한정되며 실제 모델의 정확도나 배포 성능을 측정하지 않는다.

## English

These educational models use only the Python standard library. Run the command above from the repository root. The table maps each domain to its functions and independent checks: known memory patterns and resource limits; analytic probabilities and shift invariance; SQL aggregation and transaction rollback; exhaustive quorum subsets and complete partitions; similar triangles, constant images, finite differences and an analytic optimum; known rankings and exact metrics; integer grids, error bounds and inverse transforms; discrete eigenmodes, convergence and flux balance; and retry, conflict and pagination contracts.

The GPU functions calculate addresses and resource bounds without executing CUDA. Distributed and HTTP examples are single-process contract models without network failures, concurrency or persistent storage. Training, retrieval and quantization checks cover small mathematical cases and do not measure production model accuracy or deployment performance.
