# RAG와 도구 실행: 검색, 근거, 평가의 경계

## 검색된 문서는 답의 재료다

RAG는 요청과 관련된 자료를 검색해 생성 모델의 입력에 넣는 방식이다. 모델의 가중치를 다시 학습하는 과정과는 다르다. 문서를 수집하고, 검색 단위로 나누고, 색인을 만들고, 질의에 맞는 부분을 가져온 뒤 답변을 생성한다. 자료가 검색되었다는 사실만으로 내용이 참이거나 답변이 그 자료를 정확히 사용했다는 보장은 없다. Microsoft의 RAG 설명도 검색·분할·관련성 순위·출처 추적을 구분한다. [Microsoft RAG overview](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)

Chunk는 검색과 입력 길이를 위해 정한 단위다. 너무 짧으면 정의와 조건이 떨어지고, 너무 길면 관련 없는 내용이 함께 들어간다. 문서 ID, revision, 페이지·절 위치를 보관하면 인용을 원문으로 되돌릴 수 있다. 접근 권한이 다른 문서를 한 색인에 넣는 경우 검색 단계의 권한 필터도 데이터 계약에 포함된다.

## 작은 검색 기준선: TF-IDF와 cosine

단어 $`t`$가 문서 $`d`$에 나오는 횟수 $`tf_{t,d}`$, 전체 문서 수 $`N`$, 해당 단어가 있는 문서 수 $`df_t`$를 생각하자. 흔한 단어보다 구별력이 큰 단어에 더 가중치를 주는 TF-IDF가 한 기준선이다. [Stanford IR book](https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html)

예제는 다음의 smoothing 변형을 명시적으로 사용한다.

$$w_{t,d}=tf_{t,d}\left[1+\ln\frac{N+1}{df_t+1}\right],
\qquad s(q,d)=\frac{w_q\cdot w_d}{\Vert w_q\Vert _2\Vert w_d\Vert _2}.$$

질의에도 같은 문서 집합에서 만든 IDF를 쓴다. 빈 벡터의 유사도는 예제 정책상 0이다. 모든 성분이 음이 아니므로 이 모델의 cosine은 0~1이다. 벡터 길이로 나누면 문서가 길다는 이유만으로 점수가 계속 커지는 효과를 줄인다. 단어가 다르지만 의미가 같은 문장을 잘 찾는다는 보장은 없으며, 한국어 형태소 분석기나 모델 tokenizer를 구현한 예제도 아니다.

## 검색 성능과 답변 성능을 따로 본다

정답 관련 문서 집합 $`G`$, 상위 $`k`$개 집합 $`S_k`$라면 $`Recall@k=\vert G\cap S_k\vert /\vert G\vert `$다. 첫 관련 문서의 순위가 $`r`$이면 reciprocal rank는 $`1/r`$, 상위 $`k`$개에 없으면 여기서는 0으로 둔다. 여러 질의의 평균이 cutoff가 있는 MRR이다. $`G=\{1,2\}`$, 검색 순서가 `[3,2,1]`이면 $`k=2`$에서 recall은 0.5, reciprocal rank도 0.5다. 순위 평가에는 정답 관련성 판단과 cutoff 정의가 함께 필요하다. [Stanford ranked retrieval evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html)

검색 지표가 좋아도 생성 답변이 근거를 잘못 읽을 수 있다. 평가 항목을 다음처럼 나누면 어느 단계의 실패인지 드러난다.

| 단계 | 관찰할 오류 |
|---|---|
| 검색 | 필요한 근거가 상위 결과에 없는가 |
| 근거 사용 | 주장과 인용한 문장이 실제로 맞물리는가 |
| 답변 | 계산·조건·결론이 정답 기준에 맞는가 |
| 미답변 | 자료가 없을 때 답을 만들어내는가 |
| 도구 | 함수·인자·결과 사용이 계약을 따르는가 |

같은 문서나 평가 질문으로 설정을 반복 조정했다면 별도의 holdout 질의가 필요하다. 평가 데이터 수, 조건별 결과와 실패 사례도 함께 기록해야 평균 수치를 해석할 수 있다.

## 도구 호출 제안과 실행 권한은 다르다

모델이 함수 이름과 인자를 출력하는 것은 실행 요청의 표현이다. 실제 함수를 실행하는 주체는 애플리케이션이다. Google의 function calling 문서도 모델이 직접 함수를 실행하지 않는다고 구분한다. [Google function calling](https://ai.google.dev/gemini-api/docs/function-calling)

검색 문서의 문장을 실행 명령으로 취급하면 신뢰 경계를 넘는다. 실행부는 등록된 함수 목록, 인자 schema, 허용 범위, 사용자 권한과 부작용 정책을 적용한다. 예제의 `bounded_tool`은 로컬 합산 함수 하나만 허용하며 인자는 최대 100개의 유한한 숫자, 절댓값 $`10^6`$ 이하로 제한한다. Shell 문자열 해석이나 파일·네트워크 작업은 구현하지 않는다. 이 검사는 외부 시스템 전체의 보안을 증명하는 것이 아니라 작은 실행 계약을 보여 준다.

## 구현과 검증

[`tfidf_rank`, `retrieval_metrics`, `bounded_tool`](../../../예제_examples/확장기초_extended/ai_data/models.py)을 [테스트](../../../예제_examples/확장기초_extended/ai_data/test_models.py)와 함께 실행한다. 고유한 질의 단어를 가진 문서가 먼저 나오는지, 어휘 밖 질의의 점수가 모두 0인지, 직접 계산한 지표가 맞는지 확인한다. 등록되지 않은 함수, 추가 인자, Boolean을 숫자로 넣은 경우, NaN을 거부한다. 실제 모델 호출·문서 서비스·권한 시스템을 연결한 end-to-end 평가 결과는 아니다.

## English

### Retrieved material is evidence to inspect

RAG retrieves material and supplies it to a generation model; it is different from retraining weights. Collection, chunking, indexing, retrieval and answer generation are distinct stages. Finding a document does not establish its truth or prove that an answer used it correctly. Microsoft's overview separates retrieval, chunking, relevance and provenance. [RAG overview](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)

Chunks trade contextual completeness against irrelevant content and input length. Keeping document IDs, revisions and page or section locations allows citations to resolve to their originals. Permission-aware filtering belongs to the retrieval contract when documents have different access rights.

### An explicit lexical baseline

TF-IDF combines term frequency with a weight that discounts common terms. [Stanford TF-IDF](https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html) The implementation deliberately uses the smoothed formula above, not an assertion that every system uses that variant. Query weights share the corpus IDF. Cosine normalizes vector length, reducing the advantage of merely long documents. Empty vectors receive zero similarity by policy. Nonnegative components keep scores within 0–1. The baseline neither guarantees synonym matching nor implements a Korean morphological analyzer or a language-model tokenizer.

### Separate evaluation layers

Recall at $`k`$ divides the number of retrieved relevant IDs by all relevant IDs. Reciprocal rank is $`1/r`$ for the first relevant result; this implementation returns zero when none appears within $`k`$. Averaging across queries gives cutoff-based MRR. For relevant IDs $`\{1,2\}`$, ranking `[3,2,1]` has recall 0.5 and reciprocal rank 0.5 at two. Relevance labels and cutoffs must be defined with the metric. [Stanford ranking evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html)

Good retrieval can still lead to an incorrect answer. The table separates missing evidence, misuse of citations, incorrect conclusions, unsupported answers when evidence is absent and invalid tool use. Holdout queries are needed after repeated tuning on a development set. Dataset size, condition-specific results and failures give context to averages.

### A request is not execution authority

A model's function name and arguments describe a proposed invocation. The application executes it. Google's documentation makes that division explicit. [Function calling](https://ai.google.dev/gemini-api/docs/function-calling) Retrieved text must not gain authority to execute commands merely by being in context. The executor enforces registered functions, argument schemas, bounds, user authorization and side-effect policy.

The demonstration allows only a local summation function, with at most 100 finite numeric values bounded in magnitude by $`10^6`$. It does not interpret shell strings or implement file/network effects. This illustrates a bounded contract rather than proving security of an external system.

### Implementation and checks

The linked functions rank a small corpus, compute explicit metrics and enforce the local tool boundary. Tests use a unique query term to establish a known top result, an out-of-vocabulary query with all-zero scores and hand-calculated metrics. They reject unknown functions, extra arguments, Boolean numeric impostors and NaN. No live model, document service or authorization system is exercised; end-to-end evaluation is a separate layer.

## Sources

- [Microsoft, RAG overview](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview): retrieval, chunking and provenance.
- [Stanford IR book, TF-IDF](https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html) and [ranked evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html): lexical weighting and relevance-based metrics.
- [Google, function calling](https://ai.google.dev/gemini-api/docs/function-calling): application ownership of execution. Reference date: 2026-10-19.
