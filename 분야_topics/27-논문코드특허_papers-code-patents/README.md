# 논문·코드·특허 | Paper, Code & Patent Reviews

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

논문은 다루는 문제와 해결 방법, 이를 뒷받침하는 근거를 제시합니다. 코드는 그 방법을 실행 가능한 형태로 구현하고, 특허 문헌은 발명의 설명과 청구항을 포함합니다. 같은 기술을 다루더라도 문서의 목적과 읽는 기준이 다릅니다.

## 작은 재현 사례부터 읽기

논문에서 설명한 구조가 코드에 있다는 사실과 논문의 결과를 재현했다는 사실은 다릅니다. 먼저 계산 한 단계의 의미를 작은 입력으로 확인하고, 그다음 데이터·수치 정밀도·평가 조건을 대조하시면 됩니다. [부분곱 열 제거 실험 읽기](해설_notes/부분곱실험의주장과근거_partial-product-reproduction-case.md)는 이 저장소의 실제 구현에서 `3×3`이 9·8·4로 달라지는 이유와 정확도·회로 전력 결과의 해석 범위를 분석합니다.

## 논문과 코드의 연결

Abstract에는 논문의 주장과 범위가 담겨 있습니다. 방법의 수식은 가정·입력·출력과 함께 읽어야 하고, 실험의 수치는 데이터 분할·비교 대상·계산 자원·평가 지표의 영향을 받습니다. Ablation은 구성요소의 영향을 분리해 보는 분석입니다.

공개 코드에서는 entry point에서 데이터 로더·모델·손실·학습 루프·평가 코드로 실행 흐름을 따라갈 수 있습니다. 수식의 변수와 tensor shape, padding·normalization·mask 같은 구현 조건을 연결하면 문장만으로 생략된 세부사항이 드러납니다. commit과 release는 분석한 코드의 기준을 남깁니다.

## 특허와 문헌 관리

특허 문헌에는 공개번호·등록번호·출원인·발명자·우선일 같은 서지 정보가 있습니다. 청구항은 보호를 구하는 구성을 기술하고 명세서·도면은 그 내용을 설명합니다. 공개 문헌의 기술 설명과 개별 권리의 법적 판단은 다른 작업입니다.

arXiv·IEEE Xplore·ACM Digital Library는 논문을, KIPRIS·Google Patents는 특허 문헌을 찾는 경로입니다. NeurIPS·ICML·ICLR·CVPR은 AI, ISSCC는 회로, DAC·DATE는 설계·자동화 분야의 연구를 접할 수 있는 학회입니다. Zotero·BibTeX는 서지 정보와 인용을 관리합니다.

## 관련 기술

arXiv, IEEE, ACM, NeurIPS, ICML, ICLR, CVPR, ISSCC, DAC, DATE, KIPRIS, Google Patents, Zotero, BibTeX

## 참고 자료

- [WIPO — Patents](https://www.wipo.int/en/web/patents)
- [Hugging Face documentation](https://huggingface.co/docs)

## 기초 해설

- [논문·코드·특허 읽기: 주장과 재현 근거를 연결하기](해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md)

## English

The [worked partial-product case](해설_notes/부분곱실험의주장과근거_partial-product-reproduction-case.md#english) follows one arithmetic specification through two implementations and separates numerical agreement, classification accuracy and circuit supply power.

A paper presents claims through a problem, a method, and supporting evidence. Code implements the method in executable form. A patent document describes an invention and includes claims. These documents can concern the same technology while serving different purposes.

### Connecting papers and code

The abstract summarizes a paper's claims and scope. Equations are read with their assumptions, inputs, and outputs. Experimental values depend on data splits, baselines, computing resources, and evaluation metrics. Ablation studies isolate the effects of individual components.

In an open implementation, execution can be followed from the entry point through data loading, models, loss functions, training, and evaluation. Connecting equation variables to tensor shapes and details such as padding, normalization, and masking exposes choices that a paper may omit. A commit or release identifies the version being examined.

### Patents and references

Patent records include publication and registration numbers, applicants, inventors, and priority dates. Claims describe the protection sought, while the specification and drawings explain the invention. Reading the technical description and assessing a particular legal right are separate activities.

arXiv, IEEE Xplore, and ACM Digital Library provide research papers; KIPRIS and Google Patents provide patent records. NeurIPS, ICML, ICLR, and CVPR cover AI research, ISSCC covers circuits, and DAC and DATE cover design and automation. Zotero and BibTeX manage bibliographic records and citations.

### Foundation article

- [논문·코드·특허 읽기: 주장과 재현 근거를 연결하기](해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md#english)


## 심화 해설 | Advanced article

- [재현 실험 설계: 같은 조건에서 차이를 비교하기](해설_notes/쌍체비교와재현실험_paired-reproducible-experiments.md) · [English](해설_notes/쌍체비교와재현실험_paired-reproducible-experiments.md#english)
