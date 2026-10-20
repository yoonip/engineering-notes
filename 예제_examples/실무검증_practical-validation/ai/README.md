# AI 입력 계약과 평가 단위의 재현 | Replaying AI input and evaluation faults

두 실행기는 CPU에서 작은 합성 모델을 실제로 학습하고, 잘못된 조건과 해결한 조건을 비교합니다. 각 실행은 새 출력 폴더를 요구하며 기존 결과를 덮어쓰지 않습니다. 실제 공정 데이터와 설비 제어는 사용하지 않습니다.

| 실행기 | 재현하는 오류와 해결 | 해설 |
| --- | --- | --- |
| [feature_contract.py](feature_contract.py) | 열 순서·전처리 누락·요청별 scaler 재학습과, 이름·단위·저장 통계로 계산하는 배포 코드 | [전처리와 특성 순서](../../../설계와검증사례_engineering-cases/AI배포의전처리와특성순서_ai-preprocessing-contract.md) |
| [group_evaluation.py](group_evaluation.py) | 같은 묶음이 섞인 행 분할, group 분리, 평가값이 scaler 평균에 들어오는 경로 | [생산 묶음 단위 분할](../../../설계와검증사례_engineering-cases/생산묶음단위분할과평가누출_ai-group-evaluation.md) |

## 실행 환경

Python 3.12, NumPy·SciPy·scikit-learn 등을 사용합니다. [requirements.txt](requirements.txt)는 2026-10-21에 실행한 패키지 버전입니다. 외부 자료나 모델을 다운로드하는 학습 코드가 아니며 PyTorch·GPU·원격 API는 필요하지 않습니다.

다음 PowerShell 명령은 저장소 루트에서 실행합니다. 새 가상환경과 결과는 운영체제 임시 폴더에 둡니다. 기존 프로젝트의 가상환경·학습 결과를 바꾸지 않습니다.

```powershell
$studyEnv = Join-Path $env:TEMP ('practical-ai-env-' + [guid]::NewGuid().ToString('N'))
python -m venv $studyEnv
$studyPython = Join-Path $studyEnv 'Scripts/python.exe'
& $studyPython -m pip install -r 예제_examples/실무검증_practical-validation/ai/requirements.txt
$runRoot = Join-Path $env:TEMP ('practical-ai-run-' + [guid]::NewGuid().ToString('N'))
& $studyPython -B 예제_examples/실무검증_practical-validation/ai/feature_contract.py --out (Join-Path $runRoot 'serving')
& $studyPython -B 예제_examples/실무검증_practical-validation/ai/group_evaluation.py --out (Join-Path $runRoot 'group-evaluation')
```

## 결과 파일과 판정

`input.json`에는 실제 생성 입력과 분할 인덱스가, `report.json`에는 환경·예측·거부 결과·대조 조건·입력/소스 해시가 남습니다. 첫 실행기는 학습한 선형 모델의 특성·단위·scaler·계수를 `model.json`으로 함께 저장합니다. 표준 라이브러리 함수 `safe_probability()`가 이 형식을 읽어 추론하며 scikit-learn Pipeline과 수치를 비교합니다.

정상 종료 0은 교육용 오류가 예상대로 드러나고 해결 경로의 검사도 통과했다는 뜻입니다. 잘못된 모델이 유효한 제품 성능을 보였다는 뜻은 아닙니다. 단위가 다르다고 선언한 요청은 거절하지만, 실제 단위를 거짓으로 표시한 요청까지 식별하지는 못합니다. 같은 경로를 재사용하면 예외로 거절하므로 새로운 실행 이름을 정합니다.

이 JSON 모델 형식은 scaler와 이진 LogisticRegression에 한정한 참조 구현입니다. 모델과 함께 기록한 SHA-256은 실행 입력을 대조하기 위한 것이며 서명·출처 인증 기능은 아닙니다.

## 결과 기록

[2026-10-21 실행 기록](../../../설계와검증사례_engineering-cases/검증기록_evidence/AI배포와그룹평가검증_20261021.md)에 환경, 점수, 분모와 재현 범위를 정리했습니다.

## English

Two CPU examples train synthetic models and replay deployment or evaluation faults. Every run writes to a new directory, records inputs and hashes, and checks both the faulty control and the intended fix. The JSON inference adapter supports only the exported scaler plus binary linear classifier. No industrial data, GPU or remote model service is used.
