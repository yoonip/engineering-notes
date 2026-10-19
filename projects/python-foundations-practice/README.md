# Python 기초 문법 연습

리스트·문자열·딕셔너리·반복문과 표준 라이브러리를 코드 실행과 빈칸 문제로 익히는 학습 예제다. 콘솔 예제는 메서드를 호출한 뒤 값이 어떻게 달라지는지 출력하고, HTML 연습기는 5단계 50문항을 제공한다.

## 구성

| 파일 | 내용 |
| --- | --- |
| `python_essential_practice.py` | append·pop·정렬·형 변환·반복·Counter 사용 예제 |
| `run_examples.py` | 콘솔 예제 실행 |
| `practice.html` | 단계별 빈칸 문제, 힌트, 해설, 복습 목록 |
| `tests/` | 예제 출력, 모든 정답 코드, 토큰 비교와 화면 상태 전환 검사 |

## 실행

```bash
python run_examples.py
```

`practice.html`은 브라우저에서 파일을 직접 열면 실행된다. 문제에 맞는 코드 조각을 입력하면 토큰을 비교해 답을 판정한다. Python 인터프리터를 실행하는 방식은 아니며, 각 문항에 지정된 여러 정답 표현을 허용한다. 학습 기록은 현재 페이지가 열려 있는 동안 유지된다.

## 검사

Python 검사는 표준 라이브러리만 사용한다. HTML 안의 모든 허용 정답을 Python 코드에 넣어 실행하고 `result`가 기댓값과 같은지 비교한다.

```bash
python -B -m unittest discover -s tests -v
node tests/test_practice_ui.cjs
```

Node.js 검사는 DOM 모형에서 답 판정, 문제 이동, 힌트·정답 보기, 복습 목록 전환을 확인한다. 브라우저 화면 렌더링 검사는 별도 범위다.

로컬 학습 대화에서 AI로 작성한 예제를 공개용으로 정리했다. 콘솔 계산 코드는 유지했고 HTML에는 독립 실행용 문서·스타일을 붙였다. 문항의 코드·정답·기댓값은 그대로 사용한다.

## English overview

Console examples and a standalone 50-question exercise cover Python collections, strings, loops, and standard-library tools. The browser exercise compares accepted code tokens, while the Python tests execute every accepted answer and check its result. Learner progress stays in memory during the current page session.
