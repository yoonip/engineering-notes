# Python 기초 문법 연습

리스트·문자열·딕셔너리·반복문과 표준 라이브러리를 코드 실행과 빈칸 문제로 익히는 학습 예제입니다. 콘솔 예제는 메서드를 호출한 뒤 값이 어떻게 달라지는지 출력하고, HTML 연습기는 5단계 50문항을 제공합니다.

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

`practice.html`은 브라우저에서 파일을 직접 열면 실행됩니다. 문제에 맞는 코드 조각을 입력하면 토큰을 비교해 답을 판정합니다. Python 인터프리터를 실행하는 방식은 아니며, 각 문항에 지정된 여러 정답 표현을 허용합니다. 학습 기록은 현재 페이지가 열려 있는 동안 유지됩니다.

## 검사

Python 검사는 표준 라이브러리만 사용합니다. HTML 안의 모든 허용 정답을 Python 코드에 넣어 실행하고 `result`가 기댓값과 같은지 비교합니다.

```bash
python -B -m unittest discover -s tests -v
node tests/test_practice_ui.cjs
```

Node.js 검사는 DOM 모형에서 답 판정, 문제 이동, 힌트·정답 보기, 복습 목록 전환을 확인합니다. 브라우저 화면 렌더링 검사는 별도 범위입니다.

콘솔에서 메서드의 동작을 확인한 뒤 HTML 문제로 같은 개념을 연습할 수 있습니다. HTML은 외부 서비스 연결 없이 실행되며, 문제별 정답 코드와 기댓값을 함께 관리합니다.

## English

Console examples and fill-in exercises cover Python lists, strings, dictionaries, loops and standard-library tools. The console prints how values change after method calls; the standalone HTML exercise has fifty questions in five stages.

`python_essential_practice.py` demonstrates append, pop, sorting, conversion, iteration and Counter. `run_examples.py` launches the console examples. `practice.html` provides questions, hints, explanations and a review list; `tests/` checks output, accepted answers, token matching and UI state transitions.

Run `python run_examples.py` for the console or open `practice.html` directly in a browser. The HTML compares code tokens with accepted answers rather than running a Python interpreter. Questions can accept multiple expressions. Progress stays in memory while the current page is open.

The listed Python tests use the standard library, substitute every accepted answer into Python code and compare `result` against its expected value. The Node.js test uses a DOM model to check verdicts, navigation, hints/answers and review-list changes. Browser rendering is a separate check. The standalone exercise connects the same concepts as the console and needs no external service.
