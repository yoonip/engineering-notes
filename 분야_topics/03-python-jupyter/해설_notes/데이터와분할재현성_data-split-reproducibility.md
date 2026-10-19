# 노트북 결과를 다시 얻으려면: 데이터와 분할의 재현성

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### seed 하나로 실험 전체가 고정되지는 않습니다

같은 노트북과 같은 random seed를 사용해도 입력 CSV의 행 순서가 바뀌면 학습·평가 대상이 달라질 수 있습니다. 숨은 kernel 변수만 없앤다고 충분하지 않습니다. 어떤 데이터 bytes를 읽었는지, 각 행이 무엇을 나타내는지, 분할과 전처리를 어떤 규칙으로 했는지까지 연결해야 결과 차이를 설명할 수 있습니다.

Python `random`은 의사난수 상태를 가집니다. 전역 generator를 여러 기능이 공유하면 앞에서 난수를 한 번 더 뽑은 변경이 뒤의 분할에도 영향을 줍니다. 독립 `Random(seed)`를 쓰면 이 결합을 줄일 수 있지만 모든 보조 함수가 Python 버전 사이에서 같은 sequence를 보장하는 것은 아닙니다. 환경 기록과 결과 비교가 여전히 필요합니다. [Python random의 재현성](https://docs.python.org/3/library/random.html#notes-on-reproducibility)

### 원본 동일성과 의미 동일성을 구분합니다

예제 CSV는 열을 정확히 `id,value`로 정합니다. `id`는 비어 있지 않고 유일해야 하며 `value`는 유한한 실수여야 합니다. 열이 모자라거나 남는 행, 중복 ID와 NaN을 거부합니다. CSV는 단순히 쉼표로 문자열을 나누는 형식이 아닙니다. 따옴표 속 쉼표·줄바꿈을 처리해야 하므로 표준 `csv` parser를 사용합니다. 텍스트 파일로 읽을 때 `newline=''` 규약도 이 parser에 줄바꿈 처리를 맡기는 의미입니다. [Python csv](https://docs.python.org/3/library/csv.html)

원본 bytes의 SHA-256은 완전히 같은 파일인지 판정합니다. 행 순서나 줄바꿈이 달라지면 의미가 같아도 digest는 바뀝니다. 반면 parser가 만든 `(id,value)`를 ID순으로 정렬한 표현은 행 순서 변화에 덜 민감합니다. 둘을 한 digest로 뭉개지 않고 원본 digest와 변환 규칙을 별도로 남기면 어떤 동일성을 주장하는지 분명해집니다. 부동소수점 값의 textual encoding도 semantic hash를 설계할 때 정해야 합니다.

### 순서에 흔들리지 않는 작은 분할

`split_ids()`는 각 ID와 정수 seed를 canonical JSON 배열로 묶어 SHA-256을 계산합니다. digest순으로 정렬하고 앞의 정확히 $`k`$개 ID를 test로 둡니다. 이 절차는 동일한 ID 집합·seed·직렬화 규칙에서는 입력 행 순서에 영향을 받지 않습니다. 분할의 불변식은 train과 test가 겹치지 않고 합집합이 전체 ID 집합이며 test 크기가 $`k`$라는 것입니다.

이 방식은 전역 난수 상태를 소비하지 않습니다. 다만 ID 추가 시 고정 개수 상위 $`k`$의 경계가 이동할 수 있고, 계층 비율을 보장하지도 않습니다. 같은 사람의 여러 측정값이나 같은 wafer의 여러 die를 독립 ID로 나누면 정보가 새어 나갈 수 있습니다. 이 경우 샘플이 아니라 사람·wafer 같은 group을 분할 단위로 정해야 합니다. 시간 예측에서는 미래 정보가 훈련에 들어가지 않도록 시간 경계를 사용합니다.

### 전처리와 검증의 경계

평균·표준편차로 정규화한다면 그 통계는 training subset으로 계산하고 validation/test에는 고정한 값을 적용합니다. 평가 자료로 평균을 추정한 뒤 나누면 평가 정보가 학습 과정에 유입됩니다. seed는 이 누수를 막지 못합니다. 분할 ID, 전처리 계수, 코드 버전, 환경과 원본 digest가 함께 있어야 재현 단위가 됩니다.

테스트는 행 순서를 뒤집어도 같은 train/test가 나오는지, 집합 분리와 크기 조건을 만족하는지 확인합니다. 별도 hashlib 계산으로 ranking을 비교하고 잘못된 CSV를 거부합니다. ID 정렬 비용은 $`O(N\log N)`$이고 저장 공간은 $`O(N)`$입니다. demo는 세 행의 구성 예시이며 모델 정확도 실험이 아닙니다. 이 확인은 데이터 계약과 분할 규칙에 한정되고 GPU의 비결정적 연산이나 Jupyter kernel 실행까지 검증하지 않습니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" data
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### A seed does not freeze an entire experiment

The same notebook and random seed can select different training and test examples when CSV rows arrive in a different order. Removing hidden kernel variables is only part of reproducibility. Results must also connect to the exact input bytes, row identity, splitting rule, and preprocessing procedure.

Python's `random` has pseudorandom state. Sharing a global generator means an extra draw in one feature changes a later split. A separate `Random(seed)` reduces that coupling, but not every helper algorithm is guaranteed to preserve its sequence across Python versions. Environment records and output comparison remain necessary. [Python reproducibility notes](https://docs.python.org/3/library/random.html#notes-on-reproducibility)

### Separate byte identity from semantic identity

The CSV contract is exactly two columns, `id,value`. IDs must be nonempty and unique, and values finite real numbers. Missing or extra fields, duplicate IDs, and NaN are rejected. CSV is not simply string splitting at commas: quoted delimiters and newlines need a parser. The standard `csv` module handles those rules, and `newline=''` delegates newline handling to it when reading text files. [Python csv](https://docs.python.org/3/library/csv.html)

A SHA-256 digest of raw bytes tests exact file identity. Reordered rows or different line endings change it even when interpreted data are equivalent. Sorting parsed `(id,value)` pairs by ID defines an order-insensitive representation instead. Keeping raw digests and transformation rules separate makes the claimed equivalence explicit. A semantic digest also needs a defined textual encoding for floating-point values.

### A small order-independent split

`split_ids()` serializes each integer seed and ID as a canonical JSON array, hashes it with SHA-256, sorts by digest, and selects exactly the first $`k`$ IDs for testing. For the same ID set, seed, and serialization, input row order does not affect membership. Train and test must be disjoint, their union must equal the full ID set, and test size must equal $`k`$.

This method does not consume global random state. Adding IDs can move the boundary of the fixed top $`k`$, and class proportions are not guaranteed. Treating measurements from one person or dies from one wafer as unrelated IDs can leak information between subsets. Such data need group-level splitting. Forecasting requires time boundaries that prevent future information entering training.

### Preprocessing and verification boundaries

For mean/standard-deviation normalization, estimate those statistics on training data and apply the fixed values to validation and test data. Estimating them on evaluation data before splitting leaks information; a seed cannot prevent it. Reproduction therefore needs split IDs, preprocessing parameters, source revision, environment, and raw-data digest together.

Tests reverse row order, check partition membership and sizes, compare ranking with a separate hashlib calculation, and reject malformed CSV fixtures. Sorting costs $`O(N\log N)`$ time and storage is $`O(N)`$. The demo contains three constructed rows, not an accuracy experiment. Verification covers data contracts and splitting rules; it does not execute a Jupyter kernel or establish deterministic GPU computation.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" data
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [Python: random](https://docs.python.org/3/library/random.html#notes-on-reproducibility): generator 상태·버전별 재현 조건 / generator state and version conditions
- [Python: csv](https://docs.python.org/3/library/csv.html): CSV parsing·줄바꿈 / CSV parsing and newlines
