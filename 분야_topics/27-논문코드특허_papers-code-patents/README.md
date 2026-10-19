# 논문·코드·특허 | Paper, Code & Patent Reviews

[전체 목차](../../분야별목차_CATALOG.md) · [처음으로](../../README.md)

논문은 다루는 문제와 해결 방법, 이를 뒷받침하는 근거를 제시한다. 코드는 그 방법을 실행 가능한 형태로 구현하고, 특허 문헌은 발명의 설명과 청구항을 포함한다. 같은 기술을 다루더라도 문서의 목적과 읽는 기준이 다르다.

## 논문과 코드의 연결

Abstract에는 논문의 주장과 범위가 담겨 있다. 방법의 수식은 가정·입력·출력과 함께 읽어야 하고, 실험의 수치는 데이터 분할·비교 대상·계산 자원·평가 지표의 영향을 받는다. Ablation은 구성요소의 영향을 분리해 보는 분석이다.

공개 코드에서는 entry point에서 데이터 로더·모델·손실·학습 루프·평가 코드로 실행 흐름을 따라갈 수 있다. 수식의 변수와 tensor shape, padding·normalization·mask 같은 구현 조건을 연결하면 문장만으로 생략된 세부사항이 드러난다. commit과 release는 분석한 코드의 기준을 남긴다.

## 특허와 문헌 관리

특허 문헌에는 공개번호·등록번호·출원인·발명자·우선일 같은 서지 정보가 있다. 청구항은 보호를 구하는 구성을 기술하고 명세서·도면은 그 내용을 설명한다. 공개 문헌의 기술 설명과 개별 권리의 법적 판단은 다른 작업이다.

arXiv·IEEE Xplore·ACM Digital Library는 논문을, KIPRIS·Google Patents는 특허 문헌을 찾는 경로다. NeurIPS·ICML·ICLR·CVPR은 AI, ISSCC는 회로, DAC·DATE는 설계·자동화 분야의 연구를 접할 수 있는 학회다. Zotero·BibTeX는 서지 정보와 인용을 관리한다.

## 관련 기술

arXiv, IEEE, ACM, NeurIPS, ICML, ICLR, CVPR, ISSCC, DAC, DATE, KIPRIS, Google Patents, Zotero, BibTeX

## 참고 자료

- [WIPO — Patents](https://www.wipo.int/en/web/patents)
- [Hugging Face documentation](https://huggingface.co/docs)

## 기초 해설

- [논문·코드·특허 읽기: 주장과 재현 근거를 연결하기](해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md)

## English

A paper presents claims through a problem, a method, and supporting evidence. Code implements the method in executable form. A patent document describes an invention and includes claims. These documents can concern the same technology while serving different purposes.

### Connecting papers and code

The abstract summarizes a paper's claims and scope. Equations are read with their assumptions, inputs, and outputs. Experimental values depend on data splits, baselines, computing resources, and evaluation metrics. Ablation studies isolate the effects of individual components.

In an open implementation, execution can be followed from the entry point through data loading, models, loss functions, training, and evaluation. Connecting equation variables to tensor shapes and details such as padding, normalization, and masking exposes choices that a paper may omit. A commit or release identifies the version being examined.

### Patents and references

Patent records include publication and registration numbers, applicants, inventors, and priority dates. Claims describe the protection sought, while the specification and drawings explain the invention. Reading the technical description and assessing a particular legal right are separate activities.

arXiv, IEEE Xplore, and ACM Digital Library provide research papers; KIPRIS and Google Patents provide patent records. NeurIPS, ICML, ICLR, and CVPR cover AI research, ISSCC covers circuits, and DAC and DATE cover design and automation. Zotero and BibTeX manage bibliographic records and citations.

### Foundation article

- [논문·코드·특허 읽기: 주장과 재현 근거를 연결하기](해설_notes/논문코드특허읽기_claims-evidence-reproduction-licenses.md#english)
